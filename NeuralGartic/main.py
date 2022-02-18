from flask import Flask
from flask import render_template, request, redirect, url_for, session


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game', methods=['POST'])
def game():
    img = request.files['file'].read()

    return prediction(None)


def prediction(image) -> str:
    return 'wolę_równania_stanu_niż_to'


if __name__ == "__main__":
    app.debug = True
    app.run()

