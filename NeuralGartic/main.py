from flask import Flask
from flask import render_template, request, redirect, url_for, session
import tensorflow as tf
import numpy as np


app = Flask(__name__)

NET_MODEL_PATH = "modelv1.h5"

@app.route('/')
def index():
    """Main endpoint of NeuralGartic app."""

    return render_template('index.html')


@app.route('/game', methods=['POST'])
def game():
    """Endpoint that uses neural net to predict what user has drawn."""
    img = request.files['file'].read()

    return predict_class(img)


def predict_class(image) -> str:
    """Function that predicts what user has drawn.
    :param image an image of user's drawing.
    :return str -> prediction
    """
    model = tf.keras.models.load_model(NET_MODEL_PATH)
    if model != None:
        #image = tf.io.read_file(file_path)
        image = tf.image.decode_jpeg(image, channels=1)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize(image, [200, 200])
        prediction = model.predict(image[np.newaxis, ...], batch_size=1)
        class_desc = ['jabłko', 'banan', 'marchewka', 'ogórek', 'stokrotka', 'bakłażan', 'hortensja', 'pomarańcza', 'storczyk',
                      'róża', 'pomidor', 'arbuz']
        return class_desc[np.argmax(prediction[0], axis=-1)]

    return 'wolę_równania_stanu_niż_to'


if __name__ == "__main__":
    app.debug = True
    app.run()

