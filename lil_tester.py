# import requests
from minio import Minio


def start_minio_server(host_port, access_key, secret_key):
    try:
        minio_server = Minio(host_port,
                             access_key=access_key,
                             secret_key=secret_key, secure=False)
        print("MinIO server is successfully hosted.")
    except Exception as err:
        print("MinIO server hosting failed. Error:", err)

    # minio_server.make_bucket("test")
    return minio_server


host_port = "minio:9000"
access_key = "minioadmin"
secret_key = "minioadmin"

start_minio_server(host_port, access_key, secret_key)
