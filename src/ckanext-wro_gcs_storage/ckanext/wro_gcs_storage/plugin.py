import os
import ckan
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from . import gcs_uploader
from . import template_helpers as h
from .logic.action.delete import resource_delete as resourceDelete
from .logic.action.create import resource_create

global_pkg_dict = None

@toolkit.chained_action
def resource_delete(resource_delete,context, data_dict):
    resourceDelete(context, data_dict=data_dict)


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
            'resource_read_helper':h.resource_read_helper
        }

    def get_uploader(self, upload_to, old_filename):
        # using the default uploader
        return None
    
    def get_resource_uploader(self, data_dict):
        # data_dict is coming from resource_create action
        global res_dict
        res_dict = data_dict
        return gcs_uploader.ResourceCloudStorage(data_dict)