# Dołączanie modułu flask
import flask
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        return render_template('game.html', topic='Pen Pineapple Apple Pen GET') + ''
    elif request.method == 'POST':
        # get the image
        image = request.files['img']


        return render_template('game.html', topic='Pen Pineapple Apple Pen POST')
    else:
        return 'Coś poszło nie tak...'


if __name__ == "__main__":
    app.debug = True
    app.run()

