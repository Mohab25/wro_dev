import os
import ckan
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from . import gcs_uploader
from . import template_helpers as h
#from .logic.action.delete import resource_delete as resourceDelete
# from .logic.action.create import resource_create
# from .logic.action.update import resource_update

from .logic.action import ckan_custom_actions

global_pkg_dict = None

# @toolkit.chained_action
# def resource_delete(resource_delete,context, data_dict):
#     resourceDelete(context, data_dict=data_dict)


class WroGcsStoragePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceView, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'wro_gcs_storage')


    def get_actions(self):
        return {
            "resource_delete":ckan_custom_actions.resource_delete, 
            'resource_create':ckan_custom_actions.resource_create,
            # "resource_update":resource_update,
            "package_create": ckan_custom_actions.package_create
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

    # IResourceView

    def info(self):
        """
        setup the view configuration
        """
        return {
            'name': 'bigquery_mashup_view',
            'title': toolkit._('Bigquery Mash View'),
            'icon': 'mix',
            'always_available': True,
            'iframed': False,
            }

    
    def setup_template_variables(self, context, data_dict):
        pass

    def view_template(self, context, data_dict):
        """
        setup the view template
        """
        return 'views/bigquery_mash_view.html'
