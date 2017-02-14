# Статья про Стива Джобса
#1a удалить все html-тэги
#1b удалить все лишние пробелы (\s)
#2 заменить все вхождения Стива Джобса на кого-то еще
#3 заменить во всех словах, где больше 1 слога, все гласные на ы


import re

def opentext(a):
    with open(a, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def delete_tags():
    s = re.sub ('<.*?>', '', opentext(name), flags = re.DOTALL)
    return s

def delete_odd():
    s = re.sub ('(\\s)+', '\\1', delete_tags())
    return s

#def substitute():
    #s = re.sub('Сти?в(ен)?', 'Майкл', delete_odd())
    #m = re.sub('Джобс', 'Джексон', s)
    #return m
name = input('Введите название файла: ')
#print (substitute())
print (delete_odd())
