#Задание1
# opentext(fname)
#1 открывает файл с названием fname
#2 переводить текст в нижний регистр
#3 делить на слова
#4 удалить знаки препинания
#5 возвращать массив всех словоформ


def opentext(fname):
    with open(fname, 'r', encoding = 'utf-8') as f:
        text = f.readlines()
        for line in text:
            line = line.split()
        list_ = []
        for i in range (0, len(line)):
            a = line[i]
            a = a.lower()
            a = a.strip('.,?!";:"*()')
            list_.append(a)
    return list_


#Задание2
# first_letter(letter)
#1 возвращает массив слов из текста, которые начинаются на букву letter
#2 использовать функцию opentext(fname)!!!


def first_letter(letter):
    fname = input('введите название файла: ')
    text = opentext(fname)
    words_letter = []
    for i in range(len(text)):
        if text[i].startswith(letter) == True:
            words_letter.append(text[i])
        else:
            continue
    return words_letter


#Задание3
# questions()
#1 спрашивае букву, имя файла и число
#2 распечатывает результат работы first_letter(letter), есди длина слов больше опр. числа


def questions():
    letter = input('введите первую букву: ')
    number = int(input('введите число: '))
    words = first_letter(letter)
    result = []
    for i in range(len(words)):
        if len(words[i]) > number:
            result.append(words[i])
        else:
            continue
    return result
print (questions())
