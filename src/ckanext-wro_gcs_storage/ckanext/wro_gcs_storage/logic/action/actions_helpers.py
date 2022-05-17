def is_resource_link(data_dict: dict):
    """
        defines if the resource is an uploaded file or an external link
        and adds is_link attribute to the data dictionary.
        follows the same ckan logic differentiating links and uploaded
        files (https://github.com/ckan/ckan/blob/master/ckan/lib/uploader.py#L167).

        args:
        -----
            data_dict[dict]: holds the resource data.
    
    """
    name = data_dict['name']
    starts_with_http = name.startswith('http')
    data_dict['is_link'] = starts_with_http
    return data_dict
    
