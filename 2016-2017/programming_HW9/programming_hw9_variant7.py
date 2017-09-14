#В этом домашнем задании программа должна открывать файл с русским текстом в кодировке UTF-8
#и распечатывать из него по одному разу все встретившиеся в нём (в зависимости от варианта):
#7. формы глагола "сидеть"
#В формы глагола включаются деепричастия, причастия и формы на -ся и
#не включаются видовые пары (тем более что не у всех из перечисленных глаголов они имеются).
#И особое внимание стоит уделить тому, чтобы программа ничего, кроме форм этих глаголов,
#не распознавала.

import re

def opentext(text):
    with open(text, 'r', encoding = 'utf-8') as f:
        text = f.readlines()
        list_ = []
        for line in text:
            line = line.split()
            list_.extend(line)
        words = []
        for i in range(len(list_)):
            a = list_[i]
            a = a.strip('.,?!"":;*()%$#@^&<>=+')
            words.append(a)
    return words

def find_form():
    form = 'си((жу)|д((и((шь)|м|(те?))?)|(е((ть)|(л(а|и|о)?)|(в(ш((и(й|е|х|(ми?))?)|(е((го)|(му?)|й|е)?)|(ая)|(ую))))))|(я(щ((и(й|(ми?)|х|е))|(е((го)|(му?)|й|е))|(ая)|(ую)))?)))'
    form2 = 'буд((ут?)|(е(м|(шь)|(те?))))'
    words = opentext(text)
    forms = []
    for i in range(len(words)):
        m = re.search(form, words[i])
        if m != None:
            if words[i] == 'сидеть' and re.search(form2, words[i-1]) != None:
                form_fut = words[i-1] + ' ' + words[i]
                if form_fut not in forms:
                    forms.append(form_fut)
                else:
                    continue
            else:
                if words[i] not in forms:
                    forms.append(words[i])
                else:
                    continue
        else:
            continue
    return forms

text = input('Введите название файла: ')
m = find_form()
print ('Формы глагола "сидеть", встретившиеся в тексте:')
for i in range(len(m)):
    print (m[i], end = '\n')

