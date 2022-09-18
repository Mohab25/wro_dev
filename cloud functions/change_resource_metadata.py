import pathlib
from google.cloud import storage

def initialize_google_storage_client():
    service_account_path = "/home/mohab/Main/development/googleAuthKeys/wro project/wrc-wro-0fb140f089db.json"
    storage_client = storage.Client.from_service_account_json(service_account_path)
    return storage_client


def update_blob_download_name(bucket_name):
    """ update the download name of blobs and remove
    the path. 
    :returns: None
    :rtype: None
    """
    # Storage client, not added to the code for brevity 
    client = initialize_google_storage_client()
    bucket = client.bucket(bucket_name)
    for blob in bucket.list_blobs():
        if "/" in blob.name:
            remove_path = blob.name[blob.name.rfind("/") + 1:] # rfind gives that last occurence of the char
            ext = pathlib.Path(remove_path).suffix
            remove_id = remove_path[:remove_path.rfind("_id_")]
            new_name = remove_id + ext
            blob.content_disposition = f'attachment; filename="{new_name}"'
            blob.patch()
    
update_blob_download_name("wrc_wro_datasets")
