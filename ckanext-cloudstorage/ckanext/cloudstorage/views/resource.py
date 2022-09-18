import ckan.lib.base as base
import ckan.model as model
from ckan.common import _, g, request

# this doesn't do anything at the moment, but it should override the following 
# read method.


def read(package_type, id, resource_id):
    pass


# def read(package_type, id, resource_id):
#     context = {
#         u'model': model,
#         u'session': model.Session,
#         u'user': g.user,
#         u'auth_user_obj': g.userobj,
#         u'for_view': True
#     }

#     try:
#         package = get_action(u'package_show')(context, {u'id': id})
#     except (NotFound, NotAuthorized):
#         return base.abort(404, _(u'Dataset not found'))
#     activity_id = request.params.get(u'activity_id')
#     if activity_id:
#         # view an 'old' version of the package, as recorded in the
#         # activity stream
#         current_pkg = package
#         try:
#             package = context['session'].query(model.Activity).get(
#                 activity_id
#             ).data['package']
#         except AttributeError:
#             base.abort(404, _(u'Dataset not found'))

#         if package['id'] != current_pkg['id']:
#             log.info(u'Mismatch between pkg id in activity and URL {} {}'
#                      .format(package['id'], current_pkg['id']))
#             # the activity is not for the package in the URL - don't allow
#             # misleading URLs as could be malicious
#             base.abort(404, _(u'Activity not found'))
#         # The name is used lots in the template for links, so fix it to be
#         # the current one. It's not displayed to the user anyway.
#         package['name'] = current_pkg['name']

#         # Don't crash on old (unmigrated) activity records, which do not
#         # include resources or extras.
#         package.setdefault(u'resources', [])

#     resource = None
#     for res in package.get(u'resources', []):
#         if res[u'id'] == resource_id:
#             resource = res
#             break
#     if not resource:
#         return base.abort(404, _(u'Resource not found'))
#     # mohab acted here
#     mohab_resource_name = resource['name']
#     mohab_resource_format = resource['format'].lower()
#     raise RuntimeError('that one binga')
#     resource['url'] = f'https://storage.cloud.google.com/mohabtester/{mohab_resource_name}.{mohab_resource_format}'
#     # get package license info
#     license_id = package.get(u'license_id')
#     try:
#         package[u'isopen'] = model.Package.get_license_register()[license_id
#                                                                   ].isopen()
#     except KeyError:
#         package[u'isopen'] = False

#     resource_views = get_action(u'resource_view_list')(
#         context, {
#             u'id': resource_id
#         }
#     )
#     resource[u'has_views'] = len(resource_views) > 0

#     current_resource_view = None
#     view_id = request.args.get(u'view_id')
#     if resource[u'has_views']:
#         if view_id:
#             current_resource_view = [
#                 rv for rv in resource_views if rv[u'id'] == view_id
#             ]
#             if len(current_resource_view) == 1:
#                 current_resource_view = current_resource_view[0]
#             else:
#                 return base.abort(404, _(u'Resource view not found'))
#         else:
#             current_resource_view = resource_views[0]

#     # required for nav menu
#     pkg = context[u'package']
#     dataset_type = pkg.type or package_type

#     # TODO: remove
#     g.package = package
#     g.resource = resource
#     g.pkg = pkg
#     g.pkg_dict = package

#     extra_vars = {
#         u'resource_views': resource_views,
#         u'current_resource_view': current_resource_view,
#         u'dataset_type': dataset_type,
#         u'pkg_dict': package,
#         u'package': package,
#         u'resource': resource,
#         u'pkg': pkg,  # NB it is the current version of the dataset, so ignores
#                       # activity_id. Still used though in resource views for
#                       # backward compatibility
#         u'is_activity_archive': bool(activity_id),
#     }

#     template = _get_pkg_template(u'resource_template', dataset_type)
#     return base.render(template, extra_vars)
