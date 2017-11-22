from flask import Flask, render_template, redirect
# from keras.models import load_model

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


# model = load_model('./data_10000/model.0.h5')


@app.route('/')
def index():
    words = []

    for i in range(1, 100):
        words.append({'id': i, 'name': inv_vocabulary[i]})

    random.shuffle(words)

    skins = ['hue', 'saturation']
    skin = skins[random.randint(0, len(skins) - 1)]

    return render_template('index.html', words=words[:8], skin=skin)


@app.route('/word/<int:w>')
def word_by_id(w):
    if w >= len(vocabulary):
        return redirect('/')

    skins = ['fuzzy-hue', 'fuzzy-saturation', 'ring-pink', 'ring-green']
    skin = skins[random.randint(0, len(skins) - 1)]
    return render_template('word.html', word=vocabulary[w], skin=skin)


if __name__ == '__main__':
    app.run()
