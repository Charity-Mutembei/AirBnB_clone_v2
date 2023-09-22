#!/usr/bin/python3
"""
Adding more routes for paths
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def text_display(text):
    formatted_text = text.replace('_', ' ')
    return 'C {}'.format(formatted_text)


@app.route('/python', strict_slashes=False)
def python_without_text():
    return 'Python is cool'


@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text):
    formatted_text_two = text.replace('_', ' ')
    return 'Python {}'.format(formatted_text_two)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
