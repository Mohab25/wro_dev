import ckan.logic as logic
import ckan.plugins.toolkit as toolkit

@toolkit.chained_action
def package_update(original_action, context, data_dict):
    raise RuntimeError(data_dict)
    # data_dict["type"] = "metadata-form"
    access = toolkit.check_access("package_update", context, data_dict)
    result = original_action(context, data_dict) if access else None
    return result
