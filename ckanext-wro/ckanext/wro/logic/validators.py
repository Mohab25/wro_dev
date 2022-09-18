from json import tool
import logging
import ckan.plugins.toolkit as toolkit
from ckantoolkit import get_validator

logger = logging.getLogger(__name__)
ignore_missing = get_validator('ignore_missing')
not_empty = get_validator('not_empty')

def conditional_date_reference_validator(key, flattened_data, errors, context):
    """
        changes the "required" value of some fields
        according to some conditional logic (e.g. 
        changes with other fields making the field
        not required anymore).
    """
    logger.debug('======================== iniside validator' , flattened_data)
    missing_str = "missing value, set data classification to static if there is no time frame"
    from_date_value = flattened_data[('data_reference_date', 0, 'data_reference_date_from')]
    to_date_value = flattened_data[('data_reference_date', 0, 'data_reference_date_to')] 
    
    try:
        data_classification = flattened_data[('data_classification',)]
        if data_classification == "static":
            return ignore_missing(key, flattened_data, errors, context)
        elif from_date_value == "" or to_date_value == "":
            raise toolkit.Invalid(missing_str)
            
    except KeyError:
        raise toolkit.Invalid(missing_str)


def author_same_as_contact(key, flattened_data, errors, context):
    """
        if the checkbox "contact_same_as_author"
        is checked ignore missing values with 
        the contact subfields, otherwises
        it should be required.
    """
    logger.debug("======= from author_same_as_contact validator, data=",flattened_data)
    try:
        # sometimes there field won't be found (when it's not set to required true with scheming)
        contact_same_as_author =  flattened_data[('authors', 0, 'contact_same_as_author')]
    except KeyError:
        return not_empty(key, flattened_data, errors, context)
    if contact_same_as_author == False or contact_same_as_author == toolkit.missing:
        return not_empty(key, flattened_data, errors, context)
    else:
        return ignore_missing(key, flattened_data, errors, context)


def author_or_contact_collected_data(key, flattened_data, errors, context):
    """
        checking if the contact or author
        collected the data, if not, the
        name of the collecting org should
        be provided.
    """
    author_or_contact_collected_data_checkbox = flattened_data[('did_author_or_contact_organization_collect_the_data',)]
    if author_or_contact_collected_data_checkbox == toolkit.missing or author_or_contact_collected_data_checkbox == False:
        return not_empty(key, flattened_data, errors, context)
    else:
        return ignore_missing(key, flattened_data, errors, context)

def agreement(value):
    """
        users must agree to continue form submission
    """
    if value == toolkit.missing:
        raise toolkit.Invalid("must be checked")
    else:
        return value