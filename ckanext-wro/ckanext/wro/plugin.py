import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from . import helpers
from .logic import converters, validators
from .logic.action import create, update
from .blueprints.map import map_blueprint
from .blueprints.xml_parser import xml_parser_blueprint

class WroPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IResourceView, inherit=True)
    # plugins.implements(plugins.IActions)
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
            "author_or_contact_collected_data": validators.author_or_contact_collected_data,
        }


    # IActions
    # def get_actions(self):
    #     return {
    #         "package_create": create.package_create,
    #         "package_update": update.package_update,
    #     }


    # IBlueprint
    def get_blueprint(self):
        return [ map_blueprint, xml_parser_blueprint]

    # helpers
    def get_helpers(self):
        return {
            "get_bigquery_table_name": helpers.get_bigquery_table_name,
            "get_package_name":helpers.get_package_name,
            "convert_geojson_to_bbox":helpers.convert_geojson_to_bbox,
            "get_default_bounding_box":helpers.get_default_bounding_box,
        }


    # IResourceView

    def info(self):
        """
        setup the view configuration
        """
        return {
            'name': 'bigquery_map_view',
            'title': toolkit._('Bigquery Map View'),
            'icon': 'map-marker',
            'always_available': True,
            'iframed': False,
            }

    
    def setup_template_variables(self, context, data_dict):
        pass

    def view_template(self, context, data_dict):
        """
        setup the view template
        """
        return 'views/bigquery_map_view.html'
