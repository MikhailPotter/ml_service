import pickle
import io
from minio import Minio


def minio_init(minio_host, access_key, secret_key, secure=False):
    try:
        minio_client = Minio(
            minio_host, access_key=access_key, secret_key=secret_key, secure=secure
        )
        bucket_name = "data"

        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        return minio_client, bucket_name
    except Exception as e:
        print(f"Error initializing MinIO: {e}")
        return None, None


def minio_save_model(minio_client, bucket_name, model_type, model_name, params):
    try:
        model_info = {"model": model_type, "params": params}
        model_bytes = pickle.dumps(model_info)
        model_data = io.BytesIO(model_bytes)
        minio_client.put_object(bucket_name, f"{model_name}.pkl", model_data, len(model_bytes))
    except Exception as e:
        print(f"Error saving model to MinIO: {e}")


def minio_load_model(minio_client, bucket_name, model_name):
    try:
        model_data = minio_client.get_object(bucket_name, f"{model_name}.pkl")
        loaded_model_info = pickle.loads(model_data.read())
        return loaded_model_info["model"], loaded_model_info["params"]
    except Exception as e:
        print(f"Error loading model from MinIO: {e}")
        return None, None


def minio_get_models(minio_client, bucket_name):
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        model_names = [
            obj.object_name.replace(".pkl", "")
            for obj in objects
            if isinstance(obj.object_name, str) and obj.object_name
        ]
        return model_names
    except Exception as e:
        print(f"Error listing models in MinIO: {e}")
        return []


def delete_model_from_minio(minio_client, bucket_name, model_name):
    try:
        minio_client.remove_object(bucket_name, f"{model_name}.pkl")
    except Exception as e:
        print(f"Error deleting model from MinIO: {e}")
