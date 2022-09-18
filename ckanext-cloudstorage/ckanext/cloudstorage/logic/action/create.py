import ckan.logic as logic 
import ckan.plugins as plugins
import ckan.lib.uploader as uploader

_check_access = logic.check_access
_get_action = logic.get_action
ValidationError = logic.ValidationError
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
_get_or_bust = logic.get_or_bust

def resource_create(context, data_dict):
    '''Appends a new resource to a datasets list of resources.
    :param package_id: id of package that the resource should be added to.
    :type package_id: string
    :param url: url of resource
    :type url: string
    :param description: (optional)
    :type description: string
    :param format: (optional)
    :type format: string
    :param hash: (optional)
    :type hash: string
    :param name: (optional)
    :type name: string
    :param resource_type: (optional)
    :type resource_type: string
    :param mimetype: (optional)
    :type mimetype: string
    :param mimetype_inner: (optional)
    :type mimetype_inner: string
    :param cache_url: (optional)
    :type cache_url: string
    :param size: (optional)
    :type size: int
    :param created: (optional)
    :type created: iso date string
    :param last_modified: (optional)
    :type last_modified: iso date string
    :param cache_last_updated: (optional)
    :type cache_last_updated: iso date string
    :param upload: (optional)
    :type upload: FieldStorage (optional) needs multipart/form-data
    :returns: the newly created resource
    :rtype: dictionary
    '''
    model = context['model']
    user = context['user']

    package_id = _get_or_bust(data_dict, 'package_id')
    if not data_dict.get('url'):
        data_dict['url'] = ''

    pkg_dict = _get_action('package_show')(
        dict(context, return_type='dict'),
        {'id': package_id})

    _check_access('resource_create', context, data_dict)

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.before_create(context, data_dict)

    if 'resources' not in pkg_dict:
        pkg_dict['resources'] = []

    upload = uploader.get_resource_uploader(data_dict)

    if 'mimetype' not in data_dict:
        if hasattr(upload, 'mimetype'):
            data_dict['mimetype'] = upload.mimetype

    if 'size' not in data_dict:
        if hasattr(upload, 'filesize'):
            data_dict['size'] = upload.filesize

    pkg_dict['resources'].append(data_dict)
    try:
        context['defer_commit'] = True
        context['use_cache'] = False
        _get_action('package_update')(context, pkg_dict)
        context.pop('defer_commit')
    except ValidationError as e:
        try:
            raise ValidationError(e.error_dict['resources'][-1])
        except (KeyError, IndexError):
            raise ValidationError(e.error_dict)

    # Get out resource_id resource from model as it will not appear in
    # package_show until after commit
    upload.upload(context['package'].resources[-1].id,
                  uploader.get_max_resource_size())

    model.repo.commit()

    #  Run package show again to get out actual last_resource
    updated_pkg_dict = _get_action('package_show')(context, {'id': package_id})
    resource = updated_pkg_dict['resources'][-1]
    #  Add the default views to the new resource
    logic.get_action('resource_create_default_resource_views')(
        {'model': context['model'],
         'user': context['user'],
         'ignore_auth': True
         },
        {'resource': resource,
         'package': updated_pkg_dict
         })

    for plugin in plugins.PluginImplementations(plugins.IResourceController):
        plugin.after_create(context, resource)