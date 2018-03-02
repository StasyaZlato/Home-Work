import download_module
# from lxml import html, etree
# from pandas import DataFrame
from bs4 import BeautifulSoup
import re
import sqlite3
import os

def gusmus_crouler():
    poems = []
    for n in range(1,12):
        page = download_module.download('http://gusmus.net/puisi/?N={}'.format(str(n)))
        page1 = download_module.del_html(page)
        soup = BeautifulSoup(page1, 'lxml')
        container = soup.find_all('div', {'class': 'col-xs-12 col-sm-10 blog-content'})
        for i in container:
            regex = re.compile('<.*?>', re.DOTALL)
            text = re.sub(regex, '\n', str(i))
            text_ready = re.sub('\n{2,}', '\n', text)
            text_ready = re.sub('\xa0', ' ', text_ready)
            poems.append(text_ready.strip())
            file_name = 'Mustofa Bisri\\A. Mustofa Bisri - ' + text_ready.strip().split('\n')[0].capitalize() + '.txt'
            print(file_name)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write('http://gusmus.net/puisi/?N={}'.format(str(n)))
                f.write(text_ready)
    print(poems)


def poems_info(filename):
    print(filename)
    infa = {}
    with open(filename, 'r', encoding='utf-8') as f:
        all = f.readlines()
        infa['url'] = all[0].strip()
        infa['name'] = all[1].strip().capitalize()
        infa['author'] = 'A. Mustofa Bisri'
        infa['text'] = '\n'.join(all[3:]).strip()
    return infa


def insert_into_BD(infa: dict):
    conn = sqlite3.connect(os.path.join('.', 'main_bd.sqlite'))
    c = conn.cursor()
    c.execute('SELECT poem_name FROM poems_info WHERE author = "A. Mustofa Bisri"')
    existed = []
    for i in c.fetchall():
        existed.append(i[0].strip())
    print(existed)
    if infa['name'] not in existed:
        c.execute('INSERT OR IGNORE INTO poems_info (poem_name, poem_url, author) VALUES (?, ?, ?)', [infa['name'], infa['url'], infa['author']])
        c.execute('INSERT OR IGNORE INTO poems (poem_text) VALUES (?)', [infa['text']])
        conn.commit()
        print('В базу данных внесены изменения')
    else:
        print('Такое стихотворение уже существует')


def main():
    file_list = os.listdir('Mustofa Bisri')
    for file_name in file_list:
        file_name = 'Mustofa Bisri\\' + file_name
        infa = poems_info(file_name)
        insert_into_BD(infa)


main()