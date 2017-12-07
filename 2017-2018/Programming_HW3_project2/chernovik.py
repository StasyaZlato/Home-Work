from flask import Flask
from flask import request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        global question
        question = request.args['search']
        return redirect('result')
    return render_template('search.html')


@app.route('/result')
def result():
    conn = sqlite3.connect(os.path.join(r'D:\HSE\linguistics\KILR_and_programming\flask\project2', 'stats1.sqlite'))
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
