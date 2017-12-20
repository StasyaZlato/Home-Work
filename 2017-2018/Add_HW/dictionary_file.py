import re
import csv

with open('dict.txt', encoding='utf-8') as f:
    dict_list = f.readlines()

dict_st = {}


for i in range(len(dict_list)):
    try:
        dict_list[i] = dict_list[i].replace('\'', '')
        dict_list[i] = dict_list[i].strip('\t\n ')
        element = dict_list[i].split(maxsplit=1)
        element[1] = ''.join(element[1].split(maxsplit=1)[:1])
        element[1] = element[1].strip(',.')
        dict_st[element[0]]=element[1]
        with open('dict1.txt', 'a', encoding='utf-8') as k:
            k.write(element[0]+'\t'+element[1]+'\n')
        with open('dict.csv', 'a', encoding='utf-8', newline='') as l:
            writer = csv.writer(l, delimiter='\t')
            writer.writerows([element])

    except:
        print(dict_list[i])
        raise
        continue

print(len(dict_st.keys()))
