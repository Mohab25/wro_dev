import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from .bigquery_functions import make_query, make_spatial_query #get_package_name

class WroBigqueryPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceView, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'wro_bigquery')
        toolkit.add_resource('assets', 'wro-bigquery_assets')

    # helpers
    
    def get_helpers(self):
        """
        returns data from bigquery
        """
        
        return {
            "get_data":make_query,
            "get_spatial_data":make_spatial_query,
            #"get_package_name": get_package_name            
            }

    # IResourceView

    def info(self):
        """
        setup the view configuration
        """
        return {
            'name': 'wro_bigquery_view',
            'title': toolkit._('Bigquery Dataset'),
            'icon': 'google',
            'always_available': True,
            'iframed': False,
            }
    
    def setup_template_variables(self, context, data_dict):
        pass

    def view_template(self, context, data_dict):
        """
        setup the view template
        """
        return 'views/wro_bigquery_view.html'
