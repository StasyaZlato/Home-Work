#Вариант7
#сколько слов с приставкой un-
#какой процент имеет длину больше number

def opentext(fname):
    with open(fname, 'r', encoding = 'utf-8') as f:
        text = f.readlines()
        list_ = []
        for line in text:
            line = line.split()
            list_.extend(line)
        words = []
        for i in range(len(list_)):
            a = list_[i]
            a = a.lower()
            a = a.strip('.,?!";:"*()')
            words.append(a)
    return words


def un_forms():
    text = opentext(fname)
    words_un = []
    for i in range(len(text)):
        if text[i].startswith('un') == True:
            words_un.append(text[i])
        else:

            continue
    return words_un

def quantity():
    words = un_forms()
    return len(words)

def percentage(number):
    words = un_forms()
    s = 0
    for i in range(len(words)):
        if len(words[i]) > number:
            s += 1
        else:
            continue
    result = s / len(words) * 100
    return result

fname = input('Введите название файла: ')
number = int(input('Введите число: '))
print ('Количество слов с приставкой un- равно ', quantity())
print ('Процент слов с приставкой un- длинее ', number, ' равен ', percentage(number))
