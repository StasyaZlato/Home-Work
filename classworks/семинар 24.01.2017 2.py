#1 написать рег. выр. для любого выражения
#2 функция, спрашивающая слова и говорящая, являются ли они формой данного существительного

import re


def func1(regw, word1):
    word = input('Введите слово: ')
    m = re.search(regw, word)
    if m != None:
        return 'Данное слово является формой слова ' + word1
    else:
        return 'Данное слово не является формой слова ' + word1

word1 = 'свобода'
regw = r'\b(с|С)вобод(ы|е|у|ой|а((ми?)|х)?)\b'



#3а есть ли в тексте хоть одна словоформа вашего слова?
#3б сколько раз словоформы вашего слова встретились в тексте?

def if_any(s, regw):
    m = re.search(regw, s)
    s = s.split()
    p = []
    for i in range(len(s)):
        m = re.search(regw, s[i])
        if m != None:
            p = p.append(s[i])
        else:
            continue
    return 'Слово встречается в тексте ' + len(p) + ' раз'

s = 'Свободу попугаям!'
print(if_any(s, regw))
