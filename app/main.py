from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from functions import (
    model_fit,
    model_refit,
    model_remove,
    predict,
    show,
)

app = FastAPI()


class DataParams(BaseModel):
    model_type: str
    params: dict = None
    model_name: str = None
    train_data: list
    train_target: list


class ModelParams(BaseModel):
    model_type: str
    params: dict = None
    model_name: str = None


class getModelParams(BaseModel):
    model_name: str = None


class PredictParams(BaseModel):
    model_name: str
    data: list


@app.post("/model/fit/")
def post_model_fit(data: DataParams):
    model_fit(data.model_type, data.model_name, data.params, data.train_data, data.train_target)
    return {"status": "success"}


@app.post("/model/refit/")
def post_model_refit(data: DataParams):
    model_refit(data.model_name, data.params, data.train_data, data.train_target)
    return {"status": "success"}


@app.post("/model/remove/")
def post_model_remove(data: getModelParams):
    model_remove(data.model_name)
    return {"status": "success"}


@app.post("/predict/")
def post_predict(data: PredictParams):
    return {"predictions": predict(data.model_name, data.data)}


@app.post("/show/")
def post_show(data: getModelParams):
    return show(data.model_name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
