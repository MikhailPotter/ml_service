import pickle
import io
from minio import Minio
from minio.error import NoSuchKey, MinioException


def minio_init(minio_host, access_key, secret_key, secure=False):
    try:
        minio_client = Minio(
            minio_host, access_key=access_key, secret_key=secret_key, secure=secure
        )
        bucket_name = "data"

        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        return minio_client, bucket_name
    except MinioException as e:
        print(f"Error initializing MinIO: {e}")
        return None, None


def minio_save_model(minio_client, bucket_name, model_type, model_name, params):
    try:
        model_info = {"model": model_type, "params": params}
        model_bytes = pickle.dumps(model_info)
        model_data = io.BytesIO(model_bytes)
        minio_client.put_object(bucket_name, f"{model_name}.pkl", model_data, len(model_bytes))
        print(f"Successfully saved model {model_name} to MinIO")
    except MinioException as e:
        print(f"Error saving model to MinIO: {e}")


def minio_load_model(minio_client, bucket_name, model_name):
    try:
        model_data = minio_client.get_object(bucket_name, f"{model_name}.pkl")
        loaded_model_info = pickle.loads(model_data.read())
        print(f"Successfully loaded model {model_name} from MinIO")
        return loaded_model_info["model"], loaded_model_info["params"]
    except NoSuchKey:
        print(f"Model {model_name} does not exist in MinIO")
        return None, None
    except MinioException as e:
        print(f"Error loading model from MinIO: {e}")
        return None, None


def minio_delete_model(minio_client, bucket_name, model_name):
    try:
        minio_client.remove_object(bucket_name, f"{model_name}.pkl")
        print(f"Successfully deleted model {model_name} from MinIO")
    except NoSuchKey:
        print(f"Model {model_name} does not exist in MinIO")
    except MinioException as e:
        print(f"Error deleting model from MinIO: {e}")
