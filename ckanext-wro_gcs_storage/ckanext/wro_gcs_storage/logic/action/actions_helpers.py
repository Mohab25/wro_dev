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
    
def is_resource_bigquery_table(data_dict: dict):
    """
        check if the resource is a bigquery file,
        with the wro the bigquery files don't have
        neither a url nor an upload file.
    """
    if data_dict['is_link'] == False:
        bigquery_formats = ["bq", "bigquery", "big query", "big_query"]
        incoming_format = data_dict['format'].lower()
        if any(string in incoming_format for string in bigquery_formats):
            data_dict["is_bigquery_table"] = True
            # when making a resource create from the api
            # resource_name might not be given but the url
            # might, or might not.
            data_dict["name"] = data_dict["resource_name"]
        else:
            data_dict["is_bigquery_table"] = False
    
    else:
        data_dict["is_bigquery_table"] = False        
    
    return data_dict