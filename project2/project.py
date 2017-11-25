from flask import Flask
from flask import request, render_template, redirect, url_for
import sqlite3
import re

conn = sqlite3.connect('stats.sqlite')
c = conn.cursor()

import json

# Цвета

app = Flask(__name__)



# Главная страница с анкетой
@app.route('/')
def index():
    if request.args:
        gamma1 = request.args['gamma1']
        gamma2 = request.args['gamma2']
        gamma3 = request.args['gamma3']
        gamma4 = request.args['gamma4']
        gamma5 = request.args['gamma5']
        gamma6 = request.args['gamma6']
        for i in [gamma1, gamma2, gamma3, gamma4, gamma5, gamma6]:
            c.execute('INSERT INTO colours_quest (id, colour, img) VALUES(?, ?, ?)', [place, text, informant])
        return redirect(url_for('thanks'))
    return render_template('questions.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

# Страница со статистикой (таблица / любое визуальное представление)
# @app.route('/stats')
# def stats():
#
#     return
#
# # Страница с json
# @app.route('/json')
# def json():
#
#     return
#
# # Страница с поиском по данным
# @app.route('/search')
# def search():
#
#     return
#
# # Страница с результатами поиска
# @app.route('/results')
# def results():
#
#     return


if __name__ == '__main__':
    app.run(debug=True)

