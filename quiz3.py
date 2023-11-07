from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the two images from the request
    image1 = request.files['image1']
    image2 = request.files['image2']

    # Convert the images to numpy arrays
    image1_array = np.array(Image.open(image1))
    image2_array = np.array(Image.open(image2))

    # Preprocess the images
    image1_array = image1_array / 255.0
    image1_array = image1_array.reshape(1, 28, 28, 1)
    image2_array = image2_array / 255.0
    image2_array = image2_array.reshape(1, 28, 28, 1)

    # Load the trained model
    model = tf.keras.models.load_model('model.h5')

    # Make predictions on the images
    prediction1 = model.predict(image1_array)
    prediction2 = model.predict(image2_array)

    # Check if the predictions are the same
    if np.argmax(prediction1) == np.argmax(prediction2):
        return jsonify({'is_same_digit': True})
    else:
        return jsonify({'is_same_digit': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
