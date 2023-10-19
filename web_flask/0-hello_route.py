#!/usr/bin/python3
"""
this is a script that starts a Flask web application
"""
from flask import Flask
import socket

app = Flask(__name__)


@app.route('/airbnb-onepage/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


def find_available_port(port):
    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', port))
            server.close()
            return port
        except OSError:
            port += 1


port = 5000
if __name__ == '__main__':
    port = find_available_port(port)
    app.run(host='0.0.0.0', port=5000)
