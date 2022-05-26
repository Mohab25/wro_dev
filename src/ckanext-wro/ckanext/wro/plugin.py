import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from . import helpers
from .logic import converters


class WroPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    #IDatasetForm can be added
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'wro')
        toolkit.add_resource('assets','template_change_assets')

    # IHelpers
    def get_helpers(self):
        return {
            "default_map_extent":helpers.get_parsed_geojson,
        }

    def get_validators(self) -> dict:
        return {
            "convert_raw_input_to_geojson": converters.convert_raw_input_to_geojson,
        }
