# encoding: utf-8

'''API functions for deleting data from CKAN.'''

import logging
import ckan.logic
import ckan.logic.action
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import _
from ...gcs_functions import delete_blob


log = logging.getLogger('ckan.logic')

validate = ckan.lib.navl.dictization_functions.validate

# Define some shortcuts
# Ensure they are module-private so that they don't get loaded as available
# actions in the action API.
ValidationError = ckan.logic.ValidationError
NotFound = ckan.logic.NotFound
_check_access = ckan.logic.check_access
_get_or_bust = ckan.logic.get_or_bust
_get_action = ckan.logic.get_action


def resource_delete(context, data_dict):
    '''Delete a resource from a dataset.

    You must be a sysadmin or the owner of the resource to delete it.

    :param id: the id of the resource
    :type id: string

    '''
    model = context['model']
    id = _get_or_bust(data_dict, 'id')

    entity = model.Resource.get(id)

    if entity is None:
        raise NotFound

    _check_access('resource_delete',context, data_dict)

    package_id = entity.get_package_id()

    pkg_dict = _get_action('package_show')(context, {'id': package_id})
    
    res = toolkit.get_action('resource_show')(data_dict={'id':data_dict['id']})
    resource_cloud_path = toolkit.get_action('resource_show')(data_dict={'id':data_dict['id']})['cloud_path']
    resource_cloud_path = resource_cloud_path + "/" + pkg_dict['name'] 
    
    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.before_delete(context, data_dict,
                             pkg_dict.get('resources', []))

    pkg_dict = _get_action('package_show')(context, {'id': package_id})

    if pkg_dict.get('resources'):
        pkg_dict['resources'] = [r for r in pkg_dict['resources'] if not
                r['id'] == id]
    try:
        pkg_dict = _get_action('package_update')(context, pkg_dict)
    except ValidationError as e:
        errors = e.error_dict['resources'][-1]
        raise ValidationError(errors)

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.after_delete(context, pkg_dict.get('resources', []))

    model.repo.commit()
    if res['is_link'] is False:
        delete_blob(resource_cloud_path,{'id':res['id'],'name':res['name']})

def resource_view_delete(context, data_dict):
    '''Delete a resource_view.

    :param id: the id of the resource_view
    :type id: string

    '''
    model = context['model']
    id = _get_or_bust(data_dict, 'id')

    resource_view = model.ResourceView.get(id)
    if not resource_view:
        raise NotFound

    context["resource_view"] = resource_view
    context['resource'] = model.Resource.get(resource_view.resource_id)
    _check_access('resource_view_delete', context, data_dict)

    resource_view.delete()
    model.repo.commit()


def resource_view_clear(context, data_dict):
    '''Delete all resource views, or all of a particular type.

    :param view_types: specific types to delete (optional)
    :type view_types: list

    '''
    model = context['model']

    _check_access('resource_view_clear', context, data_dict)

    view_types = data_dict.get('view_types')
    model.ResourceView.delete_all(view_types)
    model.repo.commit()