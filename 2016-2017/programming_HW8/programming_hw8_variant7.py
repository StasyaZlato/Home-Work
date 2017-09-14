#Загадывает слова - сущ., показывает подсказку с распространенным словом, употребимым с сущ.
#-->снег --> белый... --> input
#СЛОВАРЬ
#минимум 5 слов
#csv файл со словами
#случайные формулировки выигрыша/проигрыша

import random

def file():
    with open('dictionary.csv', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        d = {}
        for line in lines:
            line = line.split(';')
            d[line[0]] = line[1].strip('\n')
    return d

def right():
    with open('Верные ответы.txt', 'r', encoding = 'utf-8') as f:
        text = f.read()
        text = text.split('\n')
    return random.choice(text)

def wrong():
    with open('Неверные ответы.txt', 'r', encoding = 'utf-8') as f:
        text = f.read()
        text = text.split('\n')
    return random.choice(text)

def zagadka(d):
    keys = d.keys()
    keys = list(keys)
    key = random.choice(keys)
    print ('Подсказка: ' + key + '...')
    answer = input('Введите ответ: ')
    if answer == d[key]:
        return(right())
    else:
        return(wrong() + ' Верный ответ ' + d[key] + '.')
    
d = file()
a = input('Хочешь поиграть? Введи "да" или "нет":)\n')
while a == 'да':
    print(zagadka(d))
    a = input('Хочешь сыграть еще раз?:) Введи "да" или "нет"\n')
print ('До свидания!')

