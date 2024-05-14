#!/usr/bin/env python3
'''Basic Flask application'''
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    '''Returns the rendered template for index.html page'''
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
