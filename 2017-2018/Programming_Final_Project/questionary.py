from flask import Flask
from flask import request, render_template, redirect, url_for
from flask import send_file
from manage_quests import dicts
import sqlite3
from bd import making_bd as bd
import csv
import os


# Цвета


app = Flask(__name__)


def take_user_id():
    if not os.path.exists('colour_questionary.sqlite'):
        bd()
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    c. execute('SELECT ID_user FROM answers')
    res = c.fetchall()
    if not res:
        return 1
    else:
        return res[-1][0] + 1


ID_USER = take_user_id()
QUESTIONS_EN = dicts('quests_en.txt')
QUESTIONS_RU = dicts('quests_ru.txt')
# I = 0


@app.route('/')
def index():
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO answers(ID_user) VALUES (?)', [ID_USER])
    conn.commit()
    global I
    I = 0
    global LANG
    if request.args:
        lang = request.args['lang']
        if lang == 'other':
            LANG = 1
            return redirect('other_lang')
        else:
            c.execute('UPDATE answers SET lang = "{}" WHERE ID_user = {}'.format(lang, ID_USER))
            conn.commit()
            if lang == 'en':
                LANG = 1
            else:
                LANG = 2
            return redirect('quests')
    return render_template('form1.html')


@app.route('/other_lang')
def other_lang():
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    if request.args:
        lang = request.args['lang']
        c.execute('UPDATE answers SET lang = "{}" WHERE ID_user = {}'.format(lang, ID_USER))
        conn.commit()
        return redirect('quests')
    return render_template('form2.html')


@app.route('/quests')
def question():
    global I
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    if LANG == 1:
        quest = QUESTIONS_EN[I]['quest']
        comment = QUESTIONS_EN[I]['comment']
        index = QUESTIONS_EN[I]['index']
    else:
        quest = QUESTIONS_RU[I]['quest']
        comment = QUESTIONS_RU[I]['comment']
        index = QUESTIONS_RU[I]['index']
    if request.args:
        ans = request.args['quest']
        c.execute('UPDATE answers SET "{}" = "{}" WHERE ID_user = {}'.format(str(index), ans, ID_USER))
        conn.commit()
        I += 1
        if I == 42:
            return redirect('final')
        return redirect('quests')
    return render_template('form3.html', i=I, quest=quest, comment=comment, index=index)


@app.route('/final')
def final_quest():
    global ID_USER
    global I
    global QUESTIONS_EN
    global QUESTIONS_RU
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    if LANG == 1:
        quest = QUESTIONS_EN[I]['quest']
        comment = QUESTIONS_EN[I]['comment']
        index = QUESTIONS_EN[I]['index']
    else:
        quest = QUESTIONS_RU[I]['quest']
        comment = QUESTIONS_RU[I]['comment']
        index = QUESTIONS_RU[I]['index']
    if request.args:
        ans = request.args['quest']
        c.execute('UPDATE answers SET "{}" = "{}" WHERE ID_user = {}'.format(str(index), ans, ID_USER))
        conn.commit()
        ID_USER += 1
        I = 0
        QUESTIONS_EN = dicts('quests_en.txt')
        QUESTIONS_RU = dicts('quests_ru.txt')
        return redirect('thanks')
    return render_template('form4.html', quest=quest, comment=comment)


# ловим и убиваем на корню ошибку при "пустом вводе"
# (если отправить форму, не заполняя)
@app.errorhandler(400)
def page_not_found(error):
    return render_template('error.html'), 400


# редирект после заполнения анкеты
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route('/results')
@app.route('/results/table')
def table():
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    cursor = c.execute('select * from answers')
    names = list(map(lambda x: x[0], cursor.description))
    rows = cursor.fetchall()
    rows = [k for k in rows if k.count(None) < 45]
    with open('quests_en.txt', encoding='utf-8') as f:
        quests_en = [i.strip() for i in f.readlines() if i.strip() != '']
    with open('quests_ru.txt', encoding='utf-8') as f:
        quests_ru = [i.strip() for i in f.readlines() if i.strip() != '']
    quests = [quests_en[n]+' | '+quests_ru[n] for n in range(len(quests_en))]
    return render_template('table_res.html', cols_names=names, rows=rows, n=None, quests=quests)


def make_csv():
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    with open('bd.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='&')
        first_row = ['id_user', 'lang']
        add_list = [i for i in range(0, 84)]
        first_row.extend(add_list)
        print(first_row)
        writer.writerow(first_row)
        for row in c.execute('SELECT * FROM answers'):
            writer.writerow(row)


@app.route('/file-downloads/')
def downloads():
    make_csv()
    return render_template('downloads.html')


@app.route('/return-files/')
def return_files_tut():
    return send_file('colour_questionary.sqlite', attachment_filename='colour_questionary.sqlite', mimetype='sqlite', as_attachment=True)


@app.route('/return-files-csv/')
def return_files_csv():
    return send_file('bd.csv', attachment_filename='bd.csv', mimetype='text/csv', as_attachment=True)


@app.errorhandler(NameError)
def name_error(error):
    return render_template('error.html')


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
