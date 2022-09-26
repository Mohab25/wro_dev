import ckan.plugins.toolkit as toolkit
from ckan.common import config
import ckan.logic as logic
import os
import pathlib
from .actions_helpers import is_resource_link, is_resource_bigquery_table
import ckan.lib.uploader as uploader
from ...gcs_functions import delete_blob

_get_or_bust = logic.get_or_bust

@toolkit.chained_action
def package_create(original_action,context:dict, data_dict:dict) -> dict:
    """
    uploading to the cloud requires
    few pathes to be modified,
    intercepting the package create
    action here
    """
    wro_theme = data_dict.get('wro_theme') 
    data_structure_category = data_dict.get('data_structure_category')
    uploader_estimation_of_extent = data_dict.get('uploader_estimation_of_extent_of_processing')
    data_classification = data_dict.get('data_classification')
    cloud_path = os.path.join(wro_theme,data_structure_category,uploader_estimation_of_extent,data_classification)
    cloud_path = cloud_path.title()
    extras = data_dict.get("extras")
    if extras is None:
        data_dict["extras"] = []
    data_dict['extras'].append({"key":"cloud_path", "value":cloud_path})
    access = toolkit.check_access("package_create", context, data_dict)
    result = original_action(context, data_dict) if access else None
    return result

@toolkit.chained_action
def resource_create(original_action,context:dict, data_dict:dict) -> dict:
    """
    adding cloud path to the resource
    """
    data_dict = is_resource_link(data_dict)
    data_dict= is_resource_bigquery_table(data_dict)
    package_id = _get_or_bust(data_dict, 'package_id')
    access = toolkit.check_access("resource_create", context, data_dict)
    package = toolkit.get_action("package_show")(dict(context, return_type='dict'),{'id': package_id})
    # handle the bigquery and url cases here
    if data_dict.get("is_link") is True or data_dict.get("is_bigquery_table") is True:
        updated_resource = original_action(context, data_dict) if access else None
        add_view_to_model(context, package, updated_resource)
        return updated_resource

    package_extras = package.get("extras")
    pkg_name = package.get('name')
    resource_cloud_path = ""
    for item in package_extras:
        if item.get("key") == "cloud_path":
            resource_cloud_path = item.get("value")
    
    updated_resource = original_action(context, data_dict) if access else None
    
    resource_name = data_dict.get("name")    # this name is file name not the name of the resource provided in the form
    name = pathlib.Path(resource_name).stem
    ext = pathlib.Path(resource_name).suffix
    res_id = updated_resource.get("id")
    full_name = name + '_id_'+ res_id + ext
    container_name = config.get('container_name')
    model = context["model"]
    full_url = 'https://storage.cloud.google.com/'+container_name+'/'+resource_cloud_path+'/'+ pkg_name + "/" + full_name
    if data_dict.get("is_link") is None or data_dict.get("is_link") is False:
        if data_dict.get("is_bigquery_table") is None or data_dict.get("is_bigquery_table") is False:
            updated_resource.update({"url":full_url})
            q = f""" update resource set url='{full_url}' where id='{res_id}' """
            model.Session.execute(q)
            model.repo.commit()

    handle_upload(updated_resource)
    add_view_to_model(context, package, updated_resource)    
    
    return updated_resource

def handle_upload(updated_resource):
    """
    handle the uploading part of
    the resource creation
    """
    upload = uploader.get_resource_uploader(updated_resource)
    if 'mimetype' not in updated_resource:
        if hasattr(upload, 'mimetype'):
            updated_resource['mimetype'] = upload.mimetype

    if 'size' not in updated_resource:
        if hasattr(upload, 'filesize'):
            updated_resource['size'] = upload.filesize

    upload.upload(updated_resource, uploader.get_max_resource_size())


def add_view_to_model(context, package, updated_resource):
    toolkit.get_action('resource_create_default_resource_views')(
    {'model': context['model'], 'user': context['user'],
    'ignore_auth': True},
    {'package': package,
    'resource': updated_resource})

@toolkit.chained_action
def resource_delete(original_action, context:dict, data_dict:dict) -> dict:
    """
    intercepting resource delete action,
    we are using cloud delete.
    """
    toolkit.check_access('resource_delete', context, data_dict)
    resource = toolkit.get_action("resource_show")(data_dict={"id":data_dict.get("id")})
    package = toolkit.get_action("package_show")(data_dict={"id":resource.get("package_id")})
    package_name = package.get("name")
    package_extras = package.get("extras")
    cloud_path = ""
    for item in package_extras:
        if item.get("key") == "cloud_path":
            cloud_path = item.get("value")
    if resource.get("is_link") is None or resource.get("is_link") is False:
        if resource.get("is_bigquery_table") is None or resource.get("is_bigquery_table") is False:
            delete_blob(package_name,cloud_path,resource)
    
    original_action(context, data_dict)