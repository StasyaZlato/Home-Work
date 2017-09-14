#1 статья Википедии в html
# найти все ссылки с findall
# распечатать текст ссылки - адрес

import re

def opentext(a):
    with open (a, 'r', encoding = 'utf-8') as f:
        content = f.read()
    return content

def find_all_links():
    reg = r'<a\s+href="(.*?)".*?>(.*?)</a>'
    links = re.findall(reg, opentext(a))
    return links

a = input('Введите название файла: ')
#links = find_all_links()
#for link in links[:20]:
    #print (link[1], '-->', link[0])


#2 Найти все подписи к картинкам
def pictures():
    reg = r'<div style="padding-bottom:(.*?)\swidth:(.*?)">(.*?)</div>'
    pictures = re.findall(reg, opentext(a))
    return pictures

pictures = pictures()
print ('Подписи к картинкам: ')
for picture in pictures:
    print (picture[2])
