from flask import Flask
from flask import request, render_template, redirect, url_for
import re
import urllib.request
import os


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('how_it_looks.html')


if __name__ == '__main__':
    app.run(debug=True)
