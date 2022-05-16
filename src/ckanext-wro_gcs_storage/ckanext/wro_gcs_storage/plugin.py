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


def resource_read_helper(data_dict:dict):
    # the problem with the current view is that is the resource
    # provided is not the last updated one, get the resouce and pass it
    id = data_dict['id']
    resource = toolkit.get_action('resource_show')(data_dict={'id':id})
    return resource

class WroGcsStoragePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True) # temp testing 
    plugins.implements(plugins.ITemplateHelpers) # temp testing 
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


    def get_helpers(self):
        return{
            'resource_read_helper':resource_read_helper
        }

    def get_uploader(self, upload_to, old_filename):
        # using the default uploader
        return None
    
    def get_resource_uploader(self, data_dict):
        # data_dict is coming from resource_create action
        global res_dict
        res_dict = data_dict
        return gcs_uploader.ResourceCloudStorage(data_dict)