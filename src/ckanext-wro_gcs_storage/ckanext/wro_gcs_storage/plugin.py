import ckan
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from . import gcs_uploader
from .gcs_functions import delete_blob

from logic.action.delete import resource_delete as resourceDelete

_get_or_bust = ckan.logic.get_or_bust

@toolkit.chained_action
def resource_delete(resource_delete,context, data_dict):
    resourceDelete(context, data_dict=data_dict)
    res_id = _get_or_bust(data_dict,"id")
    delete_blob('',res_id)

class WroGcsStoragePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader)
    plugins.implements(plugins.IActions)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'wro_gcs_storage')

    def get_uploader(self, upload_to, old_filename):
        # using the default uploader
        return None
    
    def get_resource_uploader(self, data_dict):
        return gcs_uploader.ResourceCloudStorage(data_dict)

    def get_actions(self):
        return {
            "resource_delete":resource_delete
        }
