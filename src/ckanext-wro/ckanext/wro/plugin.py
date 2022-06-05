import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from . import helpers
from .logic import converters, validators
from .blueprints.map import map_blueprint

class WroPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    #plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)
    #IDatasetForm can be added
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'wro')
        toolkit.add_resource('assets','wro_assets')

    def get_validators(self) -> dict:
        return {
            "convert_raw_input_to_geojson": converters.convert_raw_input_to_geojson,
            "conditional_date_reference_validator": validators.conditional_date_reference_validator,
            "author_same_as_contact": validators.author_same_as_contact,
            "agreement": validators.agreement,
            "author_or_contact_collected_data": validators.author_or_contact_collected_data

        }

    # IBlueprint
    def get_blueprint(self):
        return [ map_blueprint,]