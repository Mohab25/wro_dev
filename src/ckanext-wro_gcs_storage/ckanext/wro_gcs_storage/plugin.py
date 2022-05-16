import os
import ckan
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import pathlib
from . import gcs_uploader
from .gcs_functions import delete_blob

from .logic.action.delete import resource_delete as resourceDelete
from .logic.action.create import resource_create


_get_or_bust = ckan.logic.get_or_bust
global_pkg_dict = None

@toolkit.chained_action
def resource_delete(resource_delete,context, data_dict):
    resourceDelete(context, data_dict=data_dict)
    res_id = _get_or_bust(data_dict,"id")
    #delete_blob('',res_id)

# def global_updated_dict(pkg_data_dict):
#     global res_dict
#     data_dict = pkg_data_dict
#     return data_dict


class WroGcsStoragePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True) # temp testing 
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'wro_gcs_storage')


    def get_actions(self):
        return {
            "resource_delete":resource_delete,
            'resource_create':resource_create,
        }


    def get_uploader(self, upload_to, old_filename):
        # using the default uploader
        return None
    
    def get_resource_uploader(self, data_dict):
        # data_dict is coming from resource_create action
        global res_dict
        res_dict = data_dict
        return gcs_uploader.ResourceCloudStorage(data_dict)

        # IResourceController

    def before_view(self, pkg_dict):
        if pkg_dict:
            global global_pkg_dict
            global_pkg_dict = pkg_dict
        return pkg_dict

    def before_show(self,resource_dict):
        """
            overriding the display to show google cloud
            GCS url, instead of the default local mapping,
            this method param "resource_dict" is not the 
            upadted resouce with the correct url rahter
            it's one step back and needs to be updated 
            for the resouce to show up in the preview,
            you can't use actions here ('package_show',
            'resource_show') as they will give a
            recursion error, rather the following 
            approach is used and needs refactor.  
        """
        # pkg = toolkit.get_action('package_show')(data_dict={'id':res_dict['package_id']})['wro_theme']
        res_id = resource_dict['id']
        if global_pkg_dict:
            for res in global_pkg_dict['resources']:
                if res['id'] == res_id:
                    wro_theme = global_pkg_dict['wro_theme'] 
                    data_structure_category = global_pkg_dict['data_structure_category']
                    uploader_estimation_of_extent = global_pkg_dict['uploader_estimation_of_extent']
                    data_classification = global_pkg_dict['data_classification']
                    cloud_path = os.path.join(wro_theme,data_structure_category,uploader_estimation_of_extent,data_classification)
                    full_url = 'https://storage.cloud.google.com/mohabtester/'+ cloud_path+ '/'+ pathlib.Path(resource_dict['name']).stem + '_id_' + res_id + pathlib.Path(resource_dict['name']).suffix
                    resource_dict['url'] = full_url
        else:
            pass