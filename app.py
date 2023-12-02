if file:
        image = _read_image(Image.open(file))
        model_path = "models/best_model_C-1_gamma-0.001.joblib"
        model_path = "./model/best_model_C-1_gamma-10.joblib"
        model = joblib.load(model_path)
        prediction = model.predict(image)
        return jsonify({"prediction": str(prediction[0])})
    else:
        return jsonify({"error": "Invalid file format"})


@app.route("/prediction", methods=["POST"])
def prediction():
@app.route("/prediction/<model_type>", methods=["POST"])
def prediction(model_type):
    if model_type not in ["svm", "tree", "lr"]:
        return jsonify({"error": "Invalid model type"})
    else:
        model = load_model(model_type)
    data_json = request.json
    if data_json:
        data_dict = json.loads(data_json)
        image = np.array([data_dict["image"]])
        model_path = "models/best_model_C-1_gamma-0.001.joblib"
        model = joblib.load(model_path)
        # model_path = "models/best_model_C-1_gamma-0.001.joblib"
        # model = joblib.load(model_path)
        try:
            prediction = model.predict(image)
            return jsonify({"prediction": str(prediction[0])})
@@ -123,7 +127,18 @@ def prediction():
        return jsonify({"error": "Invalid data format"})


def load_model(model_type="svm"):
    if model_type == "svm":
        model_path = "./models/best_model_C-1_gamma-10.joblib"
    elif model_type == "tree":
        model_path = "./models/best_model_max_depth-15.joblib"
    elif model_type == "lr":
        model_path = "./models/best_model_solver-lbfgs.joblib"
    model = joblib.load(model_path)
    return model


if __name__ == "__main__":
    print("server is running")
    #check
    # check
    app.run(host="0.0.0.0", port=8000)
