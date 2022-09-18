import ckan.logic as logic
_get_action = logic.get_action
import ckan.plugins.toolkit as toolkit


@toolkit.chained_action
def package_create(original_action, context, data_dict):
    data_dict["type"] = "metadata-form"
    access = toolkit.check_access("package_create", context, data_dict)
    result = original_action(context, data_dict) if access else None
    return result
