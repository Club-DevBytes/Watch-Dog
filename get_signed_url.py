def generate_download_signed_url_v4(bucket_name, blob_name):

    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    # storage_client = storage.Client()
    bucket = cors_configuration(bucket_name)
    # bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )


    return url
