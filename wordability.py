from flask import Flask, render_template, redirect
from keras.models import load_model

import numpy as np

import random
import os

app = Flask(__name__)


def file_by_line(file, *args, **kwargs):
    with open(file, 'r', *args, **kwargs) as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()


def read_vocabulary(vocabulary_file):
    words = {}
    i = 0
    for line in file_by_line(vocabulary_file, errors='ignore'):
        line_parts = line.strip().split()

        if len(line_parts) != 3:
            continue

        (n, word, count) = line_parts
        words[word] = int(n)

        i = i + 1
    return words


def invert_vocabulary(vocabulary):
    inv = {}

    for (word, index) in vocabulary.items():
        inv[index] = word

    return inv


def get_nn_result(model, vocabulary, word_number):
    w1 = np.zeros((len(vocabulary),))
    w2 = np.zeros((len(vocabulary),))

    for w in range(1, len(vocabulary) + 1):
        w1[w - 1,] = word_number
        w2[w - 1,] = w

    out = model.predict([w1, w2])
    results = [(w, out[w - 1][0]) for w in range(1, len(vocabulary) + 1)]
    return sorted(results, key=lambda item: item[1], reverse=True)


vocabulary = read_vocabulary(os.path.dirname(__file__) + '/data_10000/vocabulary.txt')
inv_vocabulary = invert_vocabulary(vocabulary)
model = load_model(os.path.dirname(__file__) + '/data_10000/model.0.h5')


@app.route('/')
def index():
    words = []

    for i in range(1, 100):
        words.append({'id': i, 'name': inv_vocabulary[i]})

    random.shuffle(words)

    skins = ['hue', 'saturation']
    skin = skins[random.randint(0, len(skins) - 1)]

    return render_template('index.html', words=words[:21], skin=skin)


@app.route('/word/<int:w>')
def word_by_id(w):
    if w >= len(vocabulary):
        return redirect('/')

    skins = ['fuzzy-hue', 'fuzzy-saturation', 'ring-pink', 'ring-green']
    skin = skins[random.randint(0, len(skins) - 1)]

    nn_result = get_nn_result(model, vocabulary, w)

    words = []
    for i in range(0, 21):
        if nn_result[i][0] == w:
            continue

        words.append({
            'id': nn_result[i][0],
            'percent': '%.2f' % (nn_result[i][1] * 100),
            'name': inv_vocabulary[nn_result[i][0]],
        })

    return render_template('word.html', word=inv_vocabulary[w], skin=skin, words=words)


if __name__ == '__main__':
    app.run()
