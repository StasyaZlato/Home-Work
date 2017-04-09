# Взять файл, прочитать, поделить на предложения, удалить знаки препинания
# В каждом предложении найти слова, встретившиеся больше 1 раза
# Распечатать таблицу с выравниваем по центру, в которой сказано, сколько раз они встретились

import re

def opentext(text):
    with open(text, 'r', encoding = 'utf-8') as f:
        sentences = f.read()
        text = re.sub('\.(\.\.)?|\?', '!', sentences)
        list_ = text.split('!')
    return list_

def text_format(text):
    text = opentext(text)
    text1 = [re.sub('( - )|( — )|( ‒ )', ' ', i) for i in text]
    sents = [sent.split() for sent in text1]
    sents2 = [[i.strip('.,?!":;#%*&()_-\ \n') for i in sent] for sent in sents]
    sents3 = [[i.lower() for i in sent] for sent in sents2]
    return sents3

def search(text):
    sentences = text_format(text)
    repeated = [[w for w in sent if sent.count(w) > 1] for sent in sentences]
    return repeated

def count(text):
    a = search(text)
    b = opentext(text)
    for i in range(len(a)):
        if a[i]:
            print (str(b[i]) + '\n')
            c = {w : a[i].count(w) for w in a[i]}
            keys = c.keys()
            for key in keys:
                print ('{:^10}'.format(key) + '{:^10}'.format(c[key]))

text = input('Введите название файла: ')
count(text)
            
    
