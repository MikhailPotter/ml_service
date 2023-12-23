import pickle
import io
from minio import Minio
from minio.error import NoSuchKey, MinioException


MINIO_HOST = 'minio:9000'
YOUR_ACCESS_KEY, YOUR_SECRET_KEY = "minioadmin", "minioadmin"
BUCKET_NAME = 'data'


def minio_init():
    try:
        minio_client = Minio(
            MINIO_HOST,
            access_key=YOUR_ACCESS_KEY,
            secret_key=YOUR_SECRET_KEY,
            secure=False
        )

        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)

        return minio_client
    except MinioException as e:
        print(f"Error initializing MinIO: {e}")
        return None


def minio_save_model(minio_client, model_type, model_name, params):
    try:
        model_info = {"model": model_type, "params": params}
        model_dump = pickle.dumps(model_info)
        model_data = io.BytesIO(model_dump)
        minio_client.put_object(BUCKET_NAME, f"{model_name}.pkl", model_data, len(model_dump))
        print(f"Successfully saved model {model_name} to MinIO")
    except MinioException as e:
        print(f"Error saving model to MinIO: {e}")


def minio_save_fit_model(minio_client, model_name, model):
    try:
        model_dump = pickle.dumps(model)
        model_data = io.BytesIO(model_dump)
        minio_client.put_object(BUCKET_NAME, f"{model_name}.pkl", model_data, len(model_dump))
        print(f"Successfully saved model {model_name} to MinIO")
    except MinioException as e:
        print(f"Error saving model to MinIO: {e}")


def minio_load_model(minio_client, model_name):
    try:
        model_data = minio_client.get_object(BUCKET_NAME, f"{model_name}.pkl")
        loaded_model = pickle.loads(model_data.read())
        print(f"Successfully loaded model '{model_name}' from MinIO")
        return loaded_model
    except NoSuchKey:
        print(f"Model '{model_name}' does not exist in MinIO")
        return None
    except MinioException as e:
        print(f"Error loading model from MinIO: {e}")
        return None


def minio_delete_model(minio_client, model_name):
    try:
        minio_client.remove_object(BUCKET_NAME, f"{model_name}.pkl")
        print(f"Successfully deleted model '{model_name}' from MinIO")
    except NoSuchKey:
        print(f"Model '{model_name}' does not exist in MinIO")
    except MinioException as e:
        print(f"Error deleting model from MinIO: {e}")
