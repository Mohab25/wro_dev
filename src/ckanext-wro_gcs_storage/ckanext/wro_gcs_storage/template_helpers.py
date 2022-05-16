import os
import pathlib
import ckan.plugins.toolkit as toolkit

def resource_read_helper(data_dict:dict):
    # the problem with the current view is that is the resource
    # provided is not the last updated one, get the resouce and pass it
    id = data_dict['id']
    resource = toolkit.get_action('resource_show')(data_dict={'id':id})
    pkg_dict = toolkit.get_action('package_show')(data_dict={'id':resource['package_id']})
    wro_theme = pkg_dict['wro_theme'] 
    data_structure_category = pkg_dict['data_structure_category']
    uploader_estimation_of_extent = pkg_dict['uploader_estimation_of_extent']
    data_classification = pkg_dict['data_classification']
    cloud_path = os.path.join(wro_theme,data_structure_category,uploader_estimation_of_extent,data_classification)
    full_url = 'https://storage.cloud.google.com/mohabtester/'+ cloud_path+ '/'+ pathlib.Path(resource['name']).stem + '_id_' + id + pathlib.Path(resource['name']).suffix
    
    return {'resource':resource, 'cloud_url':full_url}