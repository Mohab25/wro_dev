import os
import pathlib
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
from ckan import model



_get_or_bust = logic.get_or_bust

def resource_read_helper(data_dict:dict):
    # the problem with the current view is that is the resource
    # provided is not the last updated one, get the resouce and pass it
    q = f""" select url from resource where id='{data_dict["id"]}' """
    session_res = []
    query_res = model.Session.execute(q)
    for item in query_res:
        session_res.append(item)
    cloud_path = session_res[0][0]
    return cloud_path
    # return {'resource':session_res[0], 'cloud_url':'full_url'}
    # id = data_dict['id']
    # resource = toolkit.get_action('resource_show')(data_dict={'id':id})
    # pkg_dict = toolkit.get_action('package_show')(data_dict={'id':resource['package_id']})
    # raise RuntimeError(pkg_dict)
    # package_name= pkg_dict['name']  # further investigation needed why this called packag_id with the upload and here name
    # wro_theme = pkg_dict['wro_theme'] 
    # data_structure_category = pkg_dict['data_structure_category']
    # uploader_estimation_of_extent = pkg_dict['uploader_estimation_of_extent_of_processing']
    # data_classification = pkg_dict['data_classification']
    # cloud_path = os.path.join(wro_theme,data_structure_category,uploader_estimation_of_extent,data_classification)
    # cloud_path = cloud_path.title()
    # bucket_name = toolkit.config.get('container_name') 
    # full_url = f'https://storage.cloud.google.com/{bucket_name}/'+ cloud_path+ '/'+ package_name + "/" +  pathlib.Path(resource['name']).stem.lower() + '_id_' + id + pathlib.Path(resource['name']).suffix
    
    # return {'resource':resource, 'cloud_url':full_url}
