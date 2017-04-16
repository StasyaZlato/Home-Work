# Смотрим все файлы и папки в текущей папке
# Сколько папок, в названии которых есть и кириллические, и латинские символы?
# Вывести на экран ВСЕ файлы и папки, БЕЗ ПОВТОРОВ

import os
import shutil
import re

def all_files(): 
    ff = os.listdir('.')
    file_names = []
    for f in ff:
        if os.path.isfile(f):
            a = f.split('.')
            if a[-1].isdigit() or re.search(r'\s', a[-1]) != None:
                a = '.'.join(a)
            elif len(a) > 2:
                a[0] = '.'.join(a[:-1])
            name = a[0]
        file_names.append(name)
    return file_names

def all_dirs(): 
    ff = os.listdir('.')
    dir_names = []
    for f in ff:
        if os.path.isdir(f):
            name = f
            dir_names.append(name)
    return dir_names

def all_without_rep():
    names_file = all_files()
    names_dir = all_dirs()
    names = names_file + names_dir
    names_1 = []
    for name in names:
        if name not in names_1:
            names_1.append(name)
    return names_1

def out_nice():
    names = all_without_rep()
    print('Список папок и файлов в текущей директории: ')
    for name in names:
        print (name)

def cyrill_latin_symb_fold():
    names = all_dirs()
    lat = '[a-zA-Z]'
    cyr = '[а-яА-Я]'
    cyr_lat_dirs = [name for name in names if re.search(lat, name) != None and re.search(cyr, name) != None]
    return len(cyr_lat_dirs)
    
out_nice()
print ('Количество папок, содержащих и латинские, и кириллические символы, равно: ', cyrill_latin_symb_fold())

