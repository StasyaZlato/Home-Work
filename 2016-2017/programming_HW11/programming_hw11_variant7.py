#открываем статью Вики "Птицы" html
#заменяем "птица" на "рыба"
#записываем в новый файл

import re

def open_file():
    with open('Птицы.html', 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def sub_word():
    word1 = '\\bпти́?ц(((а(х|ми?)?)|ей?|ы|у)?)\\b'
    word2 = '\\bПти́?ц(((а(х|ми?)?)|ей?|ы|у)?)\\b'
    s = re.sub(word1, 'рыб\\1', open_file())
    m = re.sub(word2, 'Рыб\\1', s)
    return m

def add_file():
    with open('Замена.html', 'w', encoding = 'utf-8') as k:
        k.write(sub_word())
    return k

add_file()
