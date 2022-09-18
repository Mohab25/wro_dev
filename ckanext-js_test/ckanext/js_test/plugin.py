import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class JsTestPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        # toolkit.add_resource('fanstatic',
        #     'js_test')
        toolkit.add_resource('assets','js_test')
