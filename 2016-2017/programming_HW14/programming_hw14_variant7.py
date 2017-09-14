# Обходит все дерево папок, начиная с папки, в которой находится
# Сообщает, в какой папке больше всего файлов

import os

def max_dir():
    a = {}
    for root, dirs, files in os.walk(os.path.abspath('.')):
        a[root] = len(files)
    max_v = max(a.values())
    if max_v == 1:
        print('Наибольшее количество файлов (' + str(max_v) +' файл) в директориях: ')
    elif max_v == 2 or max_v == 3 or max_v == 4:
        print('Наибольшее количество файлов (' + str(max_v) +' файла) в директориях: ')
    else:
        print('Наибольшее количество файлов (' + str(max_v) +' файлов) в директориях: ')
    for key in a.keys():
        if a[key] == max_v:
            print(key)

max_dir()
