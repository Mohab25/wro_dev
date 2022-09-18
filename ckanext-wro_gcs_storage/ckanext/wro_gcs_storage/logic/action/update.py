# # encoding: utf-8

# '''API functions for updating existing data in CKAN.'''

# import logging

# from six import text_type
# import ckan.plugins as plugins
# import ckan.logic as logic
# import ckan.lib.navl.dictization_functions as dfunc


# from ckan.common import _, request

# log = logging.getLogger(__name__)

# # Define some shortcuts
# # Ensure they are module-private so that they don't get loaded as available
# # actions in the action API.
# _get_action = logic.get_action
# _check_access = logic.check_access
# NotFound = logic.NotFound
# ValidationError = logic.ValidationError
# _get_or_bust = logic.get_or_bust


# def resource_update(context, data_dict):
#     '''Update a resource.

#     To update a resource you must be authorized to update the dataset that the
#     resource belongs to.

#     .. note:: Update methods may delete parameters not explicitly provided in the
#         data_dict. If you want to edit only a specific attribute use `resource_patch`
#         instead.

#     For further parameters see
#     :py:func:`~ckan.logic.action.create.resource_create`.

#     :param id: the id of the resource to update
#     :type id: string

#     :returns: the updated resource
#     :rtype: string

#     '''
#     model = context['model']
#     id = _get_or_bust(data_dict, "id")

#     if not data_dict.get('url'):
#         data_dict['url'] = ''

#     resource = model.Resource.get(id)
#     context["resource"] = resource
#     old_resource_format = resource.format

#     if not resource:
#         log.debug('Could not find resource %s', id)
#         raise NotFound(_('Resource was not found.'))

#     _check_access('resource_update', context, data_dict)
#     del context["resource"]
#     package_id = resource.package.id
#     pkg_dict = _get_action('package_show')(dict(context, return_type='dict'),
#         {'id': package_id})

#     for n, p in enumerate(pkg_dict['resources']):
#         if p['id'] == id:
#             break
#     else:
#         log.error('Could not find resource %s after all', id)
#         raise NotFound(_('Resource was not found.'))

#     # Persist the datastore_active extra if already present and not provided
#     if ('datastore_active' in resource.extras and
#             'datastore_active' not in data_dict):
#         data_dict['datastore_active'] = resource.extras['datastore_active']

#     for plugin in plugins.PluginImplementations(plugins.IResourceController):
#         plugin.before_update(context, pkg_dict['resources'][n], data_dict)
#     # pack resources list [index] = data_dict
#     pkg_dict['resources'][n] = data_dict
    
#     # handling bigquery resources, just set the name to resource_name
#     # it's handled here because this needs to happen before the update
#     # action
#     if old_resource_format == pkg_dict['resources'][n]["format"]:
#         if old_resource_format in ["bq", "bigquery", "big query", "big_query"]:
#             if pkg_dict['resources'][n]["name"] == "":
#                 # this is the case where we have a bigquery table
#                 # with it's name (link identifier) removed,
#                 # set the name to resource name
#                 pkg_dict['resources'][n]["name"] = pkg_dict['resources'][n]["resource_name"] 
#     try:
#         context['use_cache'] = False
#         # this is the update action
#         updated_pkg_dict = _get_action('package_update')(context, pkg_dict)
        
#     except ValidationError as e:
#         try:
#             raise ValidationError(e.error_dict['resources'][n])
#         except (KeyError, IndexError):
#             raise ValidationError(e.error_dict)
#     # the updated resource
#     resource = _get_action('resource_show')(context, {'id': id})
    
#     if old_resource_format != resource['format']:
#         _get_action('resource_create_default_resource_views')(
#             {'model': context['model'], 'user': context['user'],
#              'ignore_auth': True},
#             {'package': updated_pkg_dict,
#              'resource': resource})

#     for plugin in plugins.PluginImplementations(plugins.IResourceController):
#         plugin.after_update(context, resource)

#     return resource
