from google.cloud import storage
import pathlib
from ckan.common import config

def initialize_google_client():
    service_account_path = config.get('service_account_path')
    storage_client = storage.Client.from_service_account_json(service_account_path)
    return storage_client


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = initialize_google_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file_name)


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