#!/usr/bin/python3
"""This module contains a script that starts a Flask web application"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C_is_fun(text):
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text='is cool'):
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def is_a_number(n):
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_even_or_odd(n):
    if n % 2 == 0:
        num_type = 'even'
    else:
        num_type = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, num_type=num_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
