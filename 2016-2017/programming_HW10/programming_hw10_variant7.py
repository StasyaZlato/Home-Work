

#открываем статью Вики html о языке
#смотрим стандартные шаблоны-карточки
#считываем трехбуквенный код (ISO 639-3)
#вписываем в новый файл

import re

def open_file(a):
    with open(a, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def find_ISO():
    reg = 'ISO 639-3</a(.*?)>(\\w{3})</a>'
    m = re.search(reg, open_file(a), flags = re.DOTALL)
    if m:
        ISO = m.group(2)
        return ISO
    else:
        return 'В статье не указано ISO 639-3'

def add_file():
    with open('Result.txt', 'a', encoding = 'utf-8') as k:
        k.write('\n')
        k.write(a)
        k.write(': ')
        k.write(find_ISO())
    return k

a = input('Введите название статьи в формате Название.html: ')
add_file()
