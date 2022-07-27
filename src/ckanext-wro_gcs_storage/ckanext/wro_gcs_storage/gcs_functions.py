from google.cloud import storage
import pathlib
from ckan.common import config
import os

def initialize_google_client():
    service_account_path = config.get('service_account_path')
    storage_client = storage.Client.from_service_account_json(service_account_path)
    return storage_client


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = initialize_google_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    # ========== resumable upload params
    content_type = 'application/octet-stream'
    num_retries = 10
    size = os.fstat(source_file_name.fileno()).st_size
    predefined_acl = None
    if_generation_match= None
    if_generation_not_match = None
    if_metageneration_match = None
    if_metageneration_not_match = None
    # ==========
    blob._do_resumable_upload(client=storage_client, stream = source_file_name,
        content_type=content_type, size = size, num_retries=num_retries,
        predefined_acl = predefined_acl, if_generation_match= if_generation_match,
        if_generation_not_match= if_generation_not_match, if_metageneration_match=if_metageneration_match
        , if_metageneration_not_match= if_metageneration_not_match
    )


def delete_blob(resource_cloud_path, resource_dict):

    client = initialize_google_client()
    bucket_name = config.get('container_name')
    resource_name = resource_dict['name']
    name = pathlib.Path(resource_name).stem
    ext = pathlib.Path(resource_name).suffix
    resource_id = resource_dict['id']
    resource_cloud_name = resource_cloud_path+ '/' + name + '_id_'+ resource_id + ext

    blobs = client.list_blobs(bucket_name,prefix=f"{resource_cloud_path}/")
    for blob in blobs:
        if blob.name == resource_cloud_name:
            blob.delete()