import utils
from joblib import load
import os
import json
from app import app
from sklearn import datasets
import numpy as np


def create_dummy_dataset():
    X, y = utils.read_digits()
    X_train = X[:100, :, :]
    y_train = y[:100]
    X_dev = X[:50, :, :]
    y_dev = y[:50]
    X_train = utils.preprocess_data(X_train)
    X_dev = utils.preprocess_data(X_dev)
    return X_train, y_train, X_dev, y_dev


def create_dummy_hparams():
    return {
        "gamma": [0.001, 0.01, 0.1, 1, 10, 100],
        "C": [0.1, 1, 2, 5, 10],
    }


def create_dummy_lr_hparams():
    return {
        "solver": ["newton-cg"],
    }


def test_hparams_combinations():
    # a test case to check all possible combinations of hyper parameters
    h_params_grid = create_dummy_hparams()
    h_param_combinations = utils.get_combinations_with_keys(h_params_grid)

    assert len(h_param_combinations) == len(h_params_grid["gamma"]) * len(
        h_params_grid["C"]
    )


def test_hparams_combinations_values():
    # a test case to check all possible combinations of hyper parameters values
    h_params_grid = create_dummy_hparams()
    h_param_combinations = utils.get_combinations_with_keys(h_params_grid)

    assert len(h_param_combinations) == len(h_params_grid["gamma"]) * len(
        h_params_grid["C"]
    )
    expected_parma_combo_1 = {"gamma": 0.001, "C": 1}
    expected_parma_combo_2 = {"gamma": 0.01, "C": 1}

    assert expected_parma_combo_1 in h_param_combinations
    assert expected_parma_combo_2 in h_param_combinations


def test_data_splitting():
    X, y = utils.read_digits()
    X = X[:100, :, :]
    y = y[:100]
    test_size = 0.1
    dev_size = 0.6
    train_size = 1 - (test_size + dev_size)
    print(train_size)
    (
        X_train,
        X_dev,
        X_test,
        y_train,
        y_dev,
        y_test,
    ) = utils.split_train_dev_test(X, y, test_size=test_size, dev_size=dev_size)
    print(f"{len(X_train)},{len(X_dev)},{len(X_test)}")
    assert len(X_train) + len(X_dev) + len(X_test) == 100
    assert len(y_train) + len(y_dev) + len(y_test) == 100
    assert 29 <= (len(X_train)) <= 31
    assert 29 <= (len(y_train)) <= 31
    assert 59 <= (len(X_dev)) <= 61
    assert 59 <= (len(y_dev)) <= 61
    assert 9 <= (len(X_test)) <= 11
    assert 9 <= (len(y_test)) <= 11


def test_is_model_saved():
    X_train, y_train, X_dev, y_dev = create_dummy_dataset()
    h_params_grid = create_dummy_hparams()
    best_model_path, _, accuracy = utils.tune_hparams(
        X_train, X_dev, y_train, y_dev, h_params_grid, "svm"
    )
    assert os.path.exists(best_model_path)
    assert os.path.getsize(best_model_path) > 0
    assert best_model_path.endswith(".joblib")
    best_model = load(best_model_path)
    assert best_model is not None
    assert accuracy == utils.predict_and_eval(best_model, X_dev, y_dev)


def test_get_root():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_prediction():
    digits = datasets.load_digits()

    image_digits = {i: [] for i in range(10)}

    for image, label in zip(digits.images, digits.target):
        image_digits[label].append(image)
        assert len(image_digits) == 10
    for key in image_digits.keys():
        image_array = utils.preprocess_data(np.array([(image_digits[key][1])]))
        image_dict = {"image": image_array[0].tolist()}
        response = app.test_client().post("/prediction/svm", json=json.dumps(image_dict))
        assert "[200 OK]" in str(response)
        response = app.test_client().post("/prediction/tree", json=json.dumps(image_dict))
        assert "[200 OK]" in str(response)
        response = app.test_client().post("/prediction/lr", json=json.dumps(image_dict))
        assert "[200 OK]" in str(response)
        # this assert is running for 10 times with different images
        # assert int(json.loads(response.data)["prediction"]) == key


def test_lr_model_saved():
    X_train, y_train, X_dev, y_dev = create_dummy_dataset()
    h_params_grid = create_dummy_lr_hparams()
    best_model_path, _, accuracy = utils.tune_hparams(
        X_train, X_dev, y_train, y_dev, h_params_grid, "lr"
    )
    assert os.path.exists(best_model_path)
    assert os.path.getsize(best_model_path) > 0
    assert best_model_path.endswith(".joblib")
    best_model = load(best_model_path)
    assert best_model is not None
    assert "LogisticRegression" in str(type(best_model))
    assert best_model.get_params()["solver"] in best_model_path
    assert accuracy == utils.predict_and_eval(best_model, X_dev, y_dev)
