try:
    from google.cloud import storage
    import google.cloud.storage
    import json
    import os
    import sys
    import datetime

    from google.cloud import storage

    # import google.datalab.storage as storage
except Exception as e:
    print("Error : {} ".format(e))

PATH = os.path.join(os.getcwd(), 'watch-dog-key.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH
storage_client = storage.Client(PATH)
bucket = storage_client.get_bucket('watch-dog-samples')

filename = [filename.name for filename in list(bucket.list_blobs(prefix=''))]
blob = bucket.get_blob('watch-dog-samples')
print(filename)

stats = storage.Blob(bucket=bucket, name='abs.pdf').exists(storage_client)
print(stats)


#
# blobs = bucket.list_blobs(prefix='')
# for blob in blobs:
#     blob.download_to_filename(blob.name)


