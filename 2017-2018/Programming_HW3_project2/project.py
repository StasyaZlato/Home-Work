from flask import Flask
from flask import request, render_template, redirect, url_for
import sqlite3
import re
import json
import os

"""чтобы программа заработала, придется установить библиотеку bokeh для визуализации графиков,
но уж больно красиво с ним выходит:))"""

from bokeh.io import output_file
from bokeh.layouts import gridplot, column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import file_html
from bokeh.resources import CDN


# Исследование на семантику цветов - красная гамма


app = Flask(__name__)


# Главная страница с анкетой
@app.route('/')
def index():
    conn = sqlite3.connect(os.path.join('.', 'stats1.sqlite'))
    c = conn.cursor()
    if request.args:
        name = request.args['name']
        age = request.args['age']
        lang = request.args['lang']
        nc = request.args['native']
        cc = request.args['current']
        c.execute('INSERT INTO users (name, age, language, native_city, current_city) VALUES (?, ?, ?, ?, ?)', [name, age, lang, nc, cc])
        gamma1 = request.args['gamma1']
        gamma2 = request.args['gamma2']
        gamma3 = request.args['gamma3']
        gamma4 = request.args['gamma4']
        gamma5 = request.args['gamma5']
        gamma6 = request.args['gamma6']
        c.execute('INSERT INTO answers (colour1, colour2, colour3, colour4, colour5, colour6) VALUES (?, ?, ?, ?, ?, ?)',
                  [gamma1, gamma2, gamma3, gamma4, gamma5, gamma6])
        conn.commit()
        return redirect(url_for('thanks'))
    return render_template('questions.html')


# ловим и убиваем на корню ошибку при "пустом вводе"
# (если отправить форму, не заполняя)
@app.errorhandler(400)
def page_not_found(error):
    return render_template('400.html'), 400


# редирект после заполнения анкеты
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


# забираем данные из базы данных (в виде, готовом для графика)
def get_data():
    conn = sqlite3.connect(os.path.join('.', 'stats1.sqlite'))
    c = conn.cursor()
    colours = ['colour1', 'colour2', 'colour3', 'colour4', 'colour5', 'colour6']
    data = {}
    for colour in colours:
        c.execute('SELECT ' + colour + ' FROM answers')
        mass = c.fetchall()
        mass1 = [mass[i][0] for i in range(len(mass))]
        count_col = {'rose': mass1.count('rose'), 'orange': mass1.count('orange'), 'red': mass1.count('red')}
        data[colour] = count_col
    return data


# забираем из бд сведенную таблицу с пользователями и их ответами; записываем в файл json
def get_data_json():
    conn = sqlite3.connect(os.path.join('.', 'stats1.sqlite'))
    c = conn.cursor()
    c.execute('SELECT * FROM users INNER JOIN answers ON users.id = answers.id_user ORDER BY id_user')
    answers = c.fetchall()
    answers1 = []
    data_simple = []
    for i in answers:
        dic = {'id': i[0],
               'name': i[1],
               'age': i[2],
               'lang': i[3],
               'native_city': i[4],
               'current_city': i[5],
               'answers': {'colour1': i[7],
                            'colour2': i[8],
                            'colour3': i[9],
                            'colour4': i[10],
                            'colour5': i[11],
                            'colour6': i[12]}}
        answers1.append(dic)
    c.execute('SELECT * FROM colours_quest')
    pics = c.fetchall()
    dic = {pics[i][1]: pics[i][2] for i in range(len(pics))}
    data_simple.append(dic)
    data_simple.append(answers1)
    data_json = json.dumps(data_simple, indent=2, ensure_ascii=False, separators=(',', ': '))
    with open(os.path.join('.\\templates', 'infa.json'), 'w', encoding='utf-8') as f:
        f.write(data_json)
    return


# Собираем все данные и впихиваем (#невпихуемое#) в json (на самом деле, отображаем готовый json на сайте)
# а если посмотреть исходный код страницы, так там так красиво, так красиво! Даже с отступами:)
@app.route('/json')
def data_json():
    get_data_json()
    return render_template('infa.json')


# Собственно построение диаграммок (мур)
def barchart_create():
    output_file(os.path.join('.\\templates', 'bars.html'))
    colours = ['rose', 'red', 'orange']
    color = ['#FF0066', '#FF0000', '#FF9933']

    data = get_data()
    data1 = [data['colour1']['rose'], data['colour1']['red'], data['colour1']['orange']]
    data2 = [data['colour2']['rose'], data['colour2']['red'], data['colour2']['orange']]
    data3 = [data['colour3']['rose'], data['colour3']['red'], data['colour3']['orange']]
    data4 = [data['colour4']['rose'], data['colour4']['red'], data['colour4']['orange']]
    data5 = [data['colour5']['rose'], data['colour5']['red'], data['colour5']['orange']]
    data6 = [data['colour6']['rose'], data['colour6']['red'], data['colour6']['orange']]

    source1 = ColumnDataSource(data=dict(colours=colours, data1=data1, color=color))
    source2 = ColumnDataSource(data=dict(colours=colours, data2=data2, color=color))
    source3 = ColumnDataSource(data=dict(colours=colours, data3=data3, color=color))
    source4 = ColumnDataSource(data=dict(colours=colours, data4=data4, color=color))
    source5 = ColumnDataSource(data=dict(colours=colours, data5=data5, color=color))
    source6 = ColumnDataSource(data=dict(colours=colours, data6=data6, color=color))

    p1 = figure(x_range=colours, y_range=(0, max(data1) + 1), plot_height=250, title="Colour1",
                toolbar_location=None, tools="")
    p1.vbar(x='colours', top='data1', width=0.4, color='color', legend="colours", source=source1)
    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0
    p1.legend.orientation = "horizontal"
    p1.legend.location = "top_center"

    p2 = figure(x_range=colours, y_range=(0, max(data2) + 1), plot_height=250, title="Colour2",
                toolbar_location=None, tools="")
    p2.vbar(x='colours', top='data2', width=0.4, color='color', legend="colours", source=source2)
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0
    p2.legend.orientation = "horizontal"
    p2.legend.location = "top_center"

    p3 = figure(x_range=colours, y_range=(0, max(data3) + 1), plot_height=250, title="Colour3",
                toolbar_location=None, tools="")
    p3.vbar(x='colours', top='data3', width=0.4, color='color', legend="colours", source=source3)
    p3.xgrid.grid_line_color = None
    p3.y_range.start = 0
    p3.legend.orientation = "horizontal"
    p3.legend.location = "top_center"

    p4 = figure(x_range=colours, y_range=(0, max(data4) + 1), plot_height=250, title="Colour4",
                toolbar_location=None, tools="")
    p4.vbar(x='colours', top='data4', width=0.4, color='color', legend="colours", source=source4)
    p4.xgrid.grid_line_color = None
    p4.y_range.start = 0
    p4.legend.orientation = "horizontal"
    p4.legend.location = "top_right"

    p5 = figure(x_range=colours, y_range=(0, max(data5) + 1), plot_height=250, title="Colour5",
                toolbar_location=None, tools="")
    p5.vbar(x='colours', top='data5', width=0.4, color='color', legend="colours", source=source5)
    p5.xgrid.grid_line_color = None
    p5.y_range.start = 0
    p5.legend.orientation = "horizontal"
    p5.legend.location = "top_center"

    p6 = figure(x_range=colours, y_range=(0, max(data6) + 1), plot_height=250, title="Colour6",
                toolbar_location=None, tools="")
    p6.vbar(x='colours', top='data6', width=0.4, color='color', legend="colours", source=source6)
    p6.xgrid.grid_line_color = None
    p6.y_range.start = 0
    p6.legend.orientation = "horizontal"
    p6.legend.location = "top_center"
    # запиливаем графики в форму колонки, задаем изменение размера графика 
    # в зависимости от размера окна и забираем готовый html
    p = column(p1, p2, p3, p4, p5, p6, sizing_mode='scale_width')
    html = file_html(p, CDN, "Столбчатая диаграмма")
    with open(os.path.join('.\\templates', 'bars.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    return p


# статистика в виде столбчатых диаграмм
@app.route('/stats')
def stats():
    barchart_create()
    temp = '''<body>
    <table width="100%">
        <tr><th>
            <a href="http://127.0.0.1:5000" title="Нажмите сюда, если хотите перейти на страницу анкеты" style="text-decoration: none">Анкета</a>
        </th><th>
            <a href="http://127.0.0.1:5000/stats" title="Нажмите сюда, если хотите посмотреть статистику ответов" style="text-decoration: none">Статистика</a>
        </th><th>
            <a href="http://127.0.0.1:5000/json" title="Нажмите сюда, если хотите посмотреть или скачать данные исследования в формате json" style="text-decoration: none" target="_blank">JSON</a>
        </th><th>
            <a href="http://127.0.0.1:5000/search" title="Нажмите сюда для поиска по полученным данным" style="text-decoration: none">Поиск</a></th></tr>
    </table>
    <hr/>'''
    with open(os.path.join('.\\templates', 'bars.html'), 'r', encoding='utf-8') as f:
        bars_html = f.read()
    if re.search(temp, bars_html) is None:
        bars_html = bars_html.replace('<body>', temp)
    with open(os.path.join('.\\templates', 'bars.html'), 'w', encoding='utf-8') as k:
        k.write(bars_html)
    return render_template('bars.html')


# Страница с поиском по данным
@app.route('/search')
def search():
    if request.args:
        global question
        question = request.args['search']
        return redirect('results')
    return render_template('search.html')


# Страница с результатами поиска
@app.route('/results')
def results():
    conn = sqlite3.connect(os.path.join('.', 'stats1.sqlite'))
    c = conn.cursor()
    c.execute('''SELECT id_user, age, language, native_city, current_city, colour1, colour2, colour3, colour4, colour5, colour6  
                FROM users 
                INNER JOIN answers ON users.id = answers.id_user 
                WHERE age = "{0}" 
                OR language = "{0}" 
                OR native_city = "{0}" 
                OR current_city = "{0}" 
                OR colour1 = "{0}" 
                OR colour2 = "{0}" 
                OR colour3 = "{0}" 
                OR colour4 = "{0}" 
                OR colour5 = "{0}" 
                OR colour6 = "{0}"
                ORDER BY id_user'''.format(question))
    data = c.fetchall()
    t = len(data)
    return render_template('result.html', data=data, t=t)


@app.errorhandler(NameError)
def name_error(error):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
