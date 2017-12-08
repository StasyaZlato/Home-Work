import sqlite3
import re
import os


conn = sqlite3.connect(os.path.join('.','stats1.sqlite'))
c = conn.cursor()


def bd_1_colour_quest():
    with open('templates\\questions.html', 'r', encoding='utf-8') as f:
        html = f.read()
    str_re = re.compile('<table>(.*?)</table>', re.DOTALL)
    a = re.search(str_re, html).group(1)
    a = a.splitlines()
    list_f = []
    for line in a:
        str_re2 = re.compile('filename=\'(.*?)\'', re.DOTALL)
        files = re.search(str_re2, line)
        if files != None:
            list_f.append(files.group(1))
    c.execute('CREATE TABLE IF NOT EXISTS colours_quest(id_colour INTEGER PRIMARY KEY AUTOINCREMENT, colour VARCHAR NOT NULL, img VARCHAR NOT NULL)')
    for i in range(len(list_f)):
        c.execute('INSERT INTO colours_quest (colour, img) VALUES(?, ?)', ['Цвет'+str(i+1), list_f[i]])
        conn.commit()
    return


def bd_users():
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, age INTEGER, language VARCHAR, native_city VARCHAR, current_city VARCHAR)')
    return


def bd_answers():
    c.execute('CREATE TABLE IF NOT EXISTS answers (id_user INTEGER PRIMARY KEY AUTOINCREMENT, colour1 VARCHAR, colour2 VARCHAR, colour3 VARCHAR, colour4 VARCHAR, colour5 VARCHAR, colour6 VARCHAR)')
    return


def main():
    bd_1_colour_quest()
    bd_users()
    bd_answers()
    conn.commit()
main()
