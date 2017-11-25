#Программа, которая заполняет первую (фиксированную) табличку

import re
import sqlite3
conn = sqlite3.connect('stats.sqlite')
c = conn.cursor()

def bd_1_colour_quest():
    with open('templates\\questions.html', 'r', encoding='utf-8') as f:
        html = f.read()
        #print(html)
    str_re = re.compile('<table>(.*?)</table>', re.DOTALL)
    a = re.search(str_re, html).group(1)
    a = a.splitlines()
    list_f = []
    for line in a:
        str_re2 = re.compile('filename=\'(.*?)\'', re.DOTALL)
        files = re.search(str_re2, line)
        if files != None:
            list_f.append(files.group(1))
    c.execute('CREATE TABLE colours_quest(id INTEGER PRIMARY KEY AUTOINCREMENT, colour VARCHAR NOT NULL, img VARCHAR NOT NULL)')
    for i in range(len(list_f)):
        c.execute('INSERT INTO colours_quest (colour, img) VALUES(?, ?)', ['Цвет'+str(i+1), list_f[i]])

        conn.commit()
    print('Done')

bd_1_colour_quest()