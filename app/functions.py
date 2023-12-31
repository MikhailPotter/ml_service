import os
import pickle
from fastapi import HTTPException

MODEL_LOCATION = "data/saved_models/"


def model_get(model_type: str, params: dict):
    if model_type == "LogisticRegression":
        from sklearn.linear_model import LogisticRegression

        return LogisticRegression(**params)

    elif model_type == "LightGBM":
        from lightgbm import LGBMClassifier

        return LGBMClassifier(**params)

    elif model_type == "Catboost":
        from catboost import CatBoostClassifier

        return CatBoostClassifier(**params)

    else:
        raise NotImplementedError(
            "Can work only with LogisticRegression, LightGBM, Catboost"
        )


def model_fit(
    model_type: str,
    model_name: str,
    params: dict,
    train_data: list[list],
    train_target: list[list]
) -> None:
    if len(train_data) != len(train_target):
        err = "'train_data' and 'train_target' must have the same length"
        raise HTTPException(status_code=400, detail=err)

    if params is None:
        params = {}
    model = model_get(model_type, params)
    models = os.listdir(MODEL_LOCATION)

    if f"{model_name}.pkl" in models:
        err = f"Model '{model_name}' already exist!"
        raise HTTPException(status_code=409, detail=err)

    elif model_name is None:
        i = 1
        while True:
            model_name = f"unnamed_model_{i}"
            if f"{model_name}.pkl" in models:
                i += 1
                continue
            break

    model.fit(train_data, train_target)
    pickle.dump(model, open(f"data/saved_models/{model_name}.pkl", "wb"))

    return None


def model_refit(
    model_name: str,
    params: dict,
    train_data: list,
    train_target: list
) -> None:
    if len(train_data) != len(train_target):
        err = "'train_data' and 'train_target' must have the same length"
        raise HTTPException(status_code=400, detail=err)

    models = os.listdir(MODEL_LOCATION)
    if f"{model_name}.pkl" not in models:
        err = f"'{model_name}' don't exist"
        raise HTTPException(status_code=404, detail=err)

    fname = f"{MODEL_LOCATION}{model_name}.pkl"
    model = pickle.load(open(fname, "rb"))

    if params is not None:
        model.set_params(**params)
    model.fit(train_data, train_target)
    pickle.dump(model, open(fname, "wb"))

    return None


def model_remove(model_name: str) -> None:
    models = os.listdir(MODEL_LOCATION)
    file = f"{model_name}.pkl"

    if file not in models:
        err = "You must point off existing 'model_name'"
        raise HTTPException(status_code=404, detail=err)
    else:
        os.remove(os.path.join(MODEL_LOCATION, file))
    return None


def predict(model_name: str, data: list) -> list:
    models = os.listdir(MODEL_LOCATION)

    if f"{model_name}.pkl" not in models:
        err = "You must point off existing 'model_name'"
        raise HTTPException(status_code=404, detail=err)

    fname = f"{MODEL_LOCATION}{model_name}.pkl"
    model = pickle.load(open(fname, "rb"))
    pred = model.predict_proba(data)[:, 1]

    return list(pred)


def show(model_name: str) -> dict:
    models = [file for file in os.listdir(MODEL_LOCATION) if file.endswith(".pkl")]

    if model_name == "All":
        return {"Models": models}

    if f"{model_name}.pkl" not in models:
        err = f"'{model_name}' don't exist"
        raise HTTPException(status_code=404, detail=err)

    fname = f"{MODEL_LOCATION}{model_name}.pkl"
    model = pickle.load(open(fname, "rb"))
    model_params = model.get_params()

    return {model_name: model_params}
