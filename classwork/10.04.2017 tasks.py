import os
import shutil
import re

#1 вложенные папки, сост. предложение

def make_folders_sent(s):
    sent = s.split()
    b = '\\'.join(sent)
    os.makedirs(b)

s = input('Пожалуйста, введите предложение (без знаков препинания!) \n')
make_folders_sent(s)

#2 вводим число n, создать n папок (1, 2, ..., n), в каждой папке создать i файлов (i - номер папки)

def make_folders_num(n):
    for i in range(1,n+1):
        os.mkdir(str(i))
        for a in range(i):
            name = str(i) + '\\' + str(a+1) + '.txt'
            file = open(name, 'w', encoding = 'utf-8')
            file.write('Hello!')

n = int(input('Пожалуйста, введите натуральное число \n'))
make_folders_num(n)

#4 сколько в заданной папке файлов с разными расширениями?

def count():
    filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
    exts = []
    for f in filelist:
        ext = f.split('.')[-1]
        exts.append(ext)
    c = {e : exts.count(e) for e in exts}
    keys = c.keys()
    for key in keys:
        print('{:^10}'.format(key) + '{:^10}'.format(c[key]))

count()
