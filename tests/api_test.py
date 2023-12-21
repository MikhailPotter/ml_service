import requests
from app.main import (
    DataParams,
    ModelParams,
    getModelParams,
    PredictParams,
)

# Set up test data
test_data_params = DataParams(
    model_type="LogisticRegression",
    model_name="test_model",
    params={"fit_intercept": True},
    train_data=[[0], [1], [2], [3]],
    train_target=[0, 1, 2, 3],
)

test_model_params = ModelParams(
    model_type="LogisticRegression",
    model_name="test_model",
    params={"fit_intercept": True},
)

test_get_model_params = getModelParams(model_name="test_model")

test_predict_params = PredictParams(
    model_name="test_model",
    data=[[4], [5], [6], [7]],
)


def test_api_connection():
    response = requests.get("http://localhost:8000/docs")
    assert response.status_code == 200, "API connection failed"


def test_model_fit():
    response = requests.post("http://localhost:8000/model/fit/", json=test_data_params.model_dump())
    assert response.status_code == 200, "Model fit failed"


def test_model_refit():
    response = requests.post("http://localhost:8000/model/refit/", json=test_data_params.model_dump())
    assert response.status_code == 200, "Model refit failed"


def test_predict():
    response = requests.post("http://localhost:8000/predict/", json=test_predict_params.model_dump())
    assert response.status_code == 200, "Predict failed"


def test_show():
    response = requests.post("http://localhost:8000/show/", json=test_get_model_params.model_dump())
    assert response.status_code == 200, "Show failed"


def test_model_remove():
    response = requests.post("http://localhost:8000/model/remove/", json=test_get_model_params.model_dump())
    assert response.status_code == 200, "Model remove failed"


def test_all():
    test_api_connection()
    test_model_fit()
    test_model_refit()
    test_predict()
    test_show()
    test_model_remove()
    print("All tests passed")


if __name__ == "__main__":
    test_all()
