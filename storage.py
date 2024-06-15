'''
All these methods belong to google storage python client repo.
'''

# Imports the Google Cloud client library
from google.cloud import storage
from google.oauth2 import service_account
# Instantiates a client

# Added service account
storage_client = storage.Client.from_service_account_json('batikpedia-sa.json')


def upload_blob(source_file_name, destination_blob_name, bucket_name = "batikpedia"):
    """Uploads a file to the bucket."""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        print('source_file_name', source_file_name)
        blob.upload_from_file(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))
        return True
    except Exception as e:
        print(e)
        return False


def delete_blob(blob_name, bucket_name = "checkma"):
    """Deletes a blob from the bucket."""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()

        print('Blob {} deleted.'.format(blob_name))
    except:
        return False

