import download_module as down
from bs4 import BeautifulSoup
import re
import sqlite3
import os
import traceback


def gusmus_crouler():
    poems = []
    for n in range(1, 12):
        page = down.download('http://gusmus.net/puisi/?N={}'.format(str(n)))
        page1 = down.del_html(page)
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
        all_text = f.readlines()
        infa['url'] = all_text[0].strip()
        infa['name'] = all_text[1].strip().capitalize()
        infa['author'] = 'A. Mustofa Bisri'
        infa['text'] = '\n'.join(all_text[3:]).strip()
    return infa


def abdul_hadi_html():
    page = down.download('http://www.jendelasastra.com/dapur-sastra/dapur-jendela-sastra/lain-lain/puisi-puisi-abdul-hadi-wm')
    page1 = down.del_html(page)
    with open('abdul_h.html', 'w', encoding='utf-8') as f:
        f.write(page1)
    return page1


def abdul_hadi_poems():
    with open('abdul_h.html', 'r', encoding='utf-8') as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text, 'lxml')
    container = soup.find('div', {'class': 'content'})
    texts = str(container)
    texts = re.sub('\xa0', '', texts)
    texts = re.sub('<strong>(\s)?</strong>', '', texts)
    texts_list = texts.split('<strong>')
    regex = re.compile('<.*?>', re.DOTALL)
    new_list = []
    for i in texts_list:
        a = re.sub(regex, '', i)
        if a != '\n':
            new_list.append(a)
    for i in new_list:
        filename = 'Abdul Hadi WM\\' + i.strip().split('\n')[0].capitalize().strip() + '.txt'
        filename = re.sub('[~#&%*{}:?"|+/<>]', '', filename)
        print(filename)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(i)
            print('Ну вроде ок...')
        except Exception:
            with open('errors.log', 'a') as f:
                f.write('{}\n'.format(traceback.format_exc()))
            print('Ooops!')


def abdul_hadi_infa(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        all_text = f. read()
    all_lines = all_text.strip().split('\n')
    name = all_lines[0].capitalize()
    author = 'Abdul Hadi WM'
    url = 'http://www.jendelasastra.com/dapur-sastra/dapur-jendela-sastra/lain-lain/puisi-puisi-abdul-hadi-wm'
    if '19' in all_lines[-1]:
        year = all_lines[-1]
        text = '\n'.join(all_lines[1:-1]).strip()
    else:
        year = ''
        text = '\n'.join(all_lines[1:]).strip()
    return {'name': name, 'year': year, 'text': text, 'url': url, 'author': author}


def insert_into_BD(infa: dict):
    conn = sqlite3.connect(os.path.join('.', 'main_bd.sqlite'))
    c = conn.cursor()
    c.execute('SELECT poem_name FROM poems_info WHERE author = (?)', [infa['author']])
    existed = []
    for i in c.fetchall():
        existed.append(i[0].strip())
    if infa['name'].strip() not in existed:
        c.execute('INSERT OR IGNORE INTO poems_info (poem_name, poem_url, author, year) VALUES (?, ?, ?, ?)', [infa['name'], infa['url'], infa['author'], infa['year']])
        c.execute('INSERT OR IGNORE INTO poems (poem_text) VALUES (?)', [infa['text']])
        conn.commit()
        print('В базу данных внесены изменения')
    else:
        print(infa['name'] + ' - Такое стихотворение уже существует')


def haripuisi_html(url):
    page = down.download(url)
    page = down.del_html(page)
    with open('page.html', 'w', encoding='utf-8') as f:
        f.write(page)
    soup = BeautifulSoup(page, 'lxml')
    return soup


def haripuisi_urls(url):
    print(url)
    soup = haripuisi_html(url)
    urls = []
    try:
        try_sth = soup.find('section', {'class': 'site-content'})
        for link in try_sth.find_all('a'):
            b = link.get('href')
            if (b not in urls) and ('/' in b):
                urls.append(b)
        print(urls)
        regex_urls_posts = re.compile('http://www.haripuisi.com/arsip/[0-9]+')
        url_poem = []
        for url in urls:
            if re.fullmatch(regex_urls_posts, url) is not None:
                url_poem.append(url)
        previous_post = try_sth.find('div', {'class': 'nav-previous'}).find('a').get('href')
        print(len(url_poem))
        return [url_poem, previous_post]
    except Exception:
        with open('errors.log', 'a') as f:
            f.write('{}\n'.format(traceback.format_exc()))
        print('It seems done ?_?')
        return [[], '']


def main1():
    url = 'http://www.haripuisi.com/arsip/category/puisi'
    list_ = haripuisi_urls(url)
    while list_[1] != '':
        with open('urls.txt', 'a', encoding='utf-8') as f:
            for i in list_[0]:
                f.write(i+'\n')
        prev = list_[1]
        list_ = haripuisi_urls(prev)
    print('I hope it\'s really done, but to be on the safe side there is a file with error logs')


# main1()


# чем переделывать предыдущую функцию, чтобы она ловила последнюю страницу, я лучше ее отдельно выловлю
def the_last_page():
    url = 'http://www.haripuisi.com/arsip/category/puisi/page/34'
    soup = haripuisi_html(url)
    urls = []
    try_sth = soup.find('section', {'class': 'site-content'})
    for link in try_sth.find_all('a'):
        b = link.get('href')
        if (b not in urls) and ('/' in b):
            urls.append(b)
    print(urls)
    regex_urls_posts = re.compile('http://www.haripuisi.com/arsip/[0-9]+')
    url_poem = []
    for url in urls:
        if re.fullmatch(regex_urls_posts, url) is not None:
            url_poem.append(url)
    with open('urls.txt', 'a', encoding='utf-8') as f:
        for i in url_poem:
            f.write(i + '\n')
    return url_poem


the_last_page()
