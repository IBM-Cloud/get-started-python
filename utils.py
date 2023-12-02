from sklearn.model_selection import train_test_split
from sklearn import svm, tree, datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import normalize
from joblib import dump
import itertools

""" 
Common functions:
"""


# flatten the images
def preprocess_data(data):
    n = len(data)
    reshaped_data = data.reshape((n, -1))
    return normalize(reshaped_data)


def split_data(X, y, test_size, random_state=1):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=True
    )
    return X_train, X_test, y_train, y_test


def split_train_dev_test(X, y, test_size, dev_size, random_state=1):
    test_dev_size = test_size + dev_size
    if test_dev_size >= 0.9:
        raise ValueError(
            "Total test and Dev data cannot be more than 90% of entire data"
        )

    X_train, X_test_dev, y_train, y_test_dev = train_test_split(
        X, y, test_size=test_dev_size, random_state=random_state
    )
    X_test, X_dev, y_test, y_dev = train_test_split(
        X_test_dev,
        y_test_dev,
        test_size=dev_size / test_dev_size,
        random_state=random_state,
    )

    return X_train, X_dev, X_test, y_train, y_dev, y_test


def train_model(x, y, model_params, model_type="svm"):
    if model_type == "svm":
        clf = svm.SVC
    elif model_type == "tree":
        clf = tree.DecisionTreeClassifier
    elif model_type == "lr":
        clf = LogisticRegression
    model = clf(**model_params)
    model.fit(x, y)
    return model


def read_digits():
    digits = datasets.load_digits()
    return digits.images, digits.target


def predict_and_eval(model, X_test, y_test):
    predicted = model.predict(X_test)
    # cm = metrics.confusion_matrix(y_test, predicted)
    # print(f"Confusion matrix:\n{cm}")
    # print(
    #     f"Classification report for classifier {model}:\n"
    #     f"{metrics.classification_report(y_test, predicted)}\n"
    # )
    return metrics.accuracy_score(y_test, predicted)


def get_combinations_with_keys(grid):
    lists = grid.values()
    keys = grid.keys()
    combinations = list(itertools.product(*lists))
    return [dict(zip(keys, combination)) for combination in combinations]


def tune_hparams(X_train, X_dev, y_train, y_dev, h_params_grid, model_type):
    best_accuracy = -1
    best_model = None
    best_params = {}

    for h_params in ParameterGrid(h_params_grid):
        cur_model = train_model(X_train, y_train, h_params, model_type)
        cur_accuracy = predict_and_eval(cur_model, X_dev, y_dev)
        train_accuracy = predict_and_eval(cur_model, X_train, y_train)

        if model_type == "lr":
            solver = h_params.get("solver", None)
            print(
                f"model_type = {model_type} solver = {solver} train_acc={train_accuracy} dev_acc={cur_accuracy}"  # noqa
            )
            model_path = f"./models/m22aie215_{model_type}_{solver}.joblib"
            dump(cur_model, model_path)

        if cur_accuracy > best_accuracy:
            best_accuracy = cur_accuracy
            best_params = h_params
            best_model = cur_model
    best_model_path = f'./models/best_model_{"_".join([f"{k}-{v}" for k, v in best_params.items()])}.joblib'  # noqa

    dump(best_model, best_model_path)

    return best_model_path, best_params, best_accuracy
