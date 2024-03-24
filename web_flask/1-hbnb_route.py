#!/usr/bin/python3
"""This module contains a script that starts a Flask web application"""

from flask import Flask


app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
