import uuid
from flask import Flask
from flask_session import Session
from flask import render_template, request, redirect, url_for, session
import os
import random


app = Flask(__name__)
sess = Session()

ROUNDS_COUNT = 5

games = []
# one_game =
# {
#   id: int,
#   info: {
#       round: int,
#       topics: [],
#       images: [],
#       predictions: []
#       }
# }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        game_id = create_new_game()
        session['game'] = game_id

        for game in games:
            if game['id'] == game_id:
                round = game['info']['round']
                return render_template('game.html', topic=game['info']['topics'][round])

    elif request.method == 'POST':
        # get the image but check if there is any image!!!
        # image = request.files['img']
        game_id = session['game']
        for game in games:
            if game['id'] == game_id:
                game['info']['round'] += 1
                round = game['info']['round']

                if round == ROUNDS_COUNT:
                    return redirect(url_for('end'))

                #game['info']['images'].append(image)

                return render_template('game.html', topic=game['info']['topics'][round])
    else:
        return 'Coś poszło nie tak...'


@app.route('/end')
def end():
    return render_template('end.html')


def get_random_topic() -> str:
    all_topic = ['one', 'two', 'three']
    return random.choice(all_topic)


def create_new_game() -> int:
    unique_game_id = uuid.uuid4().int

    topics = []
    for i in range(ROUNDS_COUNT):
        topics.append(get_random_topic())

    games.append({
        'id': unique_game_id,
        'info': {
            'round': 0,
            'topics': topics,
            'images': [],
            'predictions': []
        }
    })

    return unique_game_id


if __name__ == "__main__":
    app.secret_key = 'citrag'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()

