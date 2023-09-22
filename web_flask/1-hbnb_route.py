#!/usr/bin/python3
"""
Script that starts the Flask application
the ports ought to listen to 0.0.0.0.port 5000
Routes: "/" display Hello HBNB! and
"/hbnb" display "HBNB"
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
