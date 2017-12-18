import urllib.request
import re
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


# Сайт не захотел отдавать данные подобру-поздорову. Пришлось отнимать силой (решение взято из оф. документации)
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def download(page_url):
    opener = AppURLopener()
    req = opener.open(page_url)
    html = req.read().decode('utf-8')
    return html


def create_file_ps(page_url):
    html = download(page_url)
    reg = re.compile('<head>.*?</head>', re.DOTALL)
    html = re.sub(reg, '', html)
    reg = re.compile('<div.*?>.*?</div>', re.DOTALL)
    html = re.sub(reg, '', html)
    reg = re.compile('<li.*?>.*?</li>', re.DOTALL)
    html = re.sub(reg, '', html)
    reg = re.compile('<h2> <span class="mw-headline" id="Abbreviations">.*', re.DOTALL)
    html = re.sub(reg, '', html)
    with open('chernovik.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    return


def find_parts_of_speech():
    with open('chernovik.txt', 'r', encoding='utf-8') as m:
        html = m.read()
    reg = re.compile('<i>(.*?)</i>', re.DOTALL)
    arr = re.findall(reg, html)
    count = len(arr)
    for i in range(count):
        t = arr[i]
        if re.search('&', t) is not None:
            i0 = t.split('&')
            arr[i] = i0[0]
    list_ = ['adj.',
             'adv.',
             'v. aux.',
             'conj.',
             'det.',
             'intj.',
             'n.',
             'na.',
             'ni.',
             'np.',
             'num.',
             'pn.',
             'prep.',
             'prop. n.',
             'v.',
             'vin.',
             'vtr.']
    dic = {i: arr.count(i) for i in arr if i in list_}
    return dic


def plot_all():
    dic1 = find_parts_of_speech()
    dic2 = count_let()
    
    x1 = [i for i in dic1.keys()]
    x1.sort()
    y1 = [dic1[i] for i in x1]

    x3 = [i for i in dic2.keys()]
    x3.sort()
    y3 = [dic2[i] for i in x3]
    
    plt.subplot(221)
    # plt.scatter(x1, y1, c='orange')
    plt.plot(x1, y1)
    plt.title('График для частей речи', color = 'black', family = 'fantasy', fontsize = 'small')

    plt.subplot(222)
    # plt.scatter(x3, y3, c='orange')
    plt.plot(x3, y3)
    plt.title('График для букв', color = 'black', family = 'fantasy', fontsize = 'small')

    plt.subplot(223)
    # plt.scatter(x, y, c='orange')
    plt.barh(x1, y1)
    plt.title('Диаграмма для частей речи', color = 'black', family = 'fantasy', fontsize = 'small')

    plt.subplot(224)
    # plt.scatter(x, y, c='orange')
    plt.barh(x3, y3)
    plt.title('Диаграмма для букв', color = 'black', family = 'fantasy', fontsize = 'small')
    plt.tight_layout()
    plt.show()

    
def plot_graph(dic, title):
    x = [i for i in dic.keys()]
    x.sort()
    y = [dic[i] for i in x]
    plt.scatter(x, y, c='orange')
    plt.plot(x, y)
    plt.title(title)
    plt.show()
    return plt


def plot_bar(dic, title):
    # dic = find_parts_of_speech()
    x = []
    for i in dic.keys():
        x.append(i)
    x.sort()
    x = [i for i in dic.keys()]
    y = [dic[i] for i in x]
    plt.bar(x, y)
    plt.title(title)
    plt.show()
    return plt


# а если соединить, то такая прикольная хрень выходит, такая прикольная...
# Типа город с подвесными мостами, только некрасивый xD
def plot_bar_and_graph(dic, title):
    # dic = find_parts_of_speech()
    x = [i for i in dic.keys()]
    x.sort()
    y = [dic[i] for i in x]
    plt.scatter(x, y, c='orange')
    plt.plot(x, y)
    plt.bar(x, y)
    plt.title(title)
    plt.show()
    return plt


def create_file_letters(page_url):
    html = download(page_url)
    reg = re.compile('<head>.*?</head>', re.DOTALL)
    html = re.sub(reg, '', html)
    reg = re.compile('<div.*?>.*?</div>', re.DOTALL)
    html = re.sub(reg, '', html)
    reg = re.compile('<h2> <span class="mw-headline" id="Abbreviations">.*', re.DOTALL)
    html = re.sub(reg, '', html)
    with open('chernovik_l.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    return


def count_let():
    with open('chernovik_l.txt', 'r', encoding='utf-8') as f:
        html = f.read()
    html_l = html.split('<table')
    html = html_l[1]
    html_letters = html.split('<h3>')[1:]
    letters = ['a',
               'c',
               'd',
               'e',
               'f',
               'g',
               'h',
               'i',
               'j',
               'k',
               'l',
               'm',
               'n',
               'o',
               'q',
               'r',
               's',
               't',
               'v',
               'y',
               'z']
    dic = {letters[i]: html_letters[i].count('<dl>') for i in range(len(letters))}
    return dic


def main(page_url):
    # create_file_letters(page_url)
    # create_file_ps(page_url)
    # здесь график некрасивый из-за сортировки списка выходит, как исправить в той же функции, не создавая
    # новую, не знаю, так что обойдемся диаграммой
    # plot_graph(count_let())
    # plot_graph(find_parts_of_speech(), 'График для частей речи')
    # plot_bar(count_let(), 'Диаграмма для букв')
    # plot_bar(find_parts_of_speech(), 'Диаграмма для частей речи')
    # plot_bar_and_graph(count_let())
    # plot_bar_and_graph(find_parts_of_speech(), 'Диаграмма и график для частей речи (мосты!)')
    plot_all() # все эти штуки на одном листе - правда, надписи друг на друга наезжают из-за масштаба:((


url = 'http://wiki.dothraki.org/Vocabulary'
main(url)
