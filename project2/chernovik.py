import sqlite3
import os
from flask import Flask
from flask import request, render_template, redirect, url_for
import json


app = Flask(__name__)


def get_json_data():
    conn = sqlite3.connect(os.path.join(r'D:\HSE\linguistics\KILR_and_programming\flask\project2', 'stats1.sqlite'))
    c = conn.cursor()
    c.execute('SELECT * FROM users INNER JOIN answers ON users.id_user = answers.id_user ORDER BY id_user')
    answers = c.fetchall()
    answers1 = []
    data = []
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
    data.append(dic)
    data.append(answers1)
    data1 = json.dumps(data, indent=2, ensure_ascii=False, separators=(',', ': '))
    with open(os.path.join('.\\templates', 'data.json'), 'w', encoding='utf-8') as f:
        f.write(data1)
    return data1


# print(get_json_data())


@app.route('/')
def index():
    # data = json.dumps(get_data())
    data = get_json_data()
    return render_template('data.json', data=data)


if __name__ == "__main__":
    app.run(debug=True)
