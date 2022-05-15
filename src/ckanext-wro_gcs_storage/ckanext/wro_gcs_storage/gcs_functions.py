from google.cloud import storage

def initialize_google_client():
    service_account_path = 'home/mohab/Main/development/googleAuthKeys/psyched-battery-346820-bde80b8fa056.json'
    storage_client = storage.Client.from_service_account_json(service_account_path)
    return storage_client


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = initialize_google_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file_name)


def delete_blob(res_path, res_id):
    client = initialize_google_client()
    bucket = client.bucket("mohabtester")
    blob = bucket.blob(f"homab.png")
    blob.delete()