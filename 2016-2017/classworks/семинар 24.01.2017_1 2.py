# replace - замена
# sNew = sOld.replace(sWhat, sWith)
# поиск in, not in
# .startswith('')/.endswith('')
# .lower(), .upper(), .capital()
# math – математические функции
# random
# os, shutil – файловая система
# datetime – дата/время
# urllib2 – интернет ресурсы
# xml.dom
# codecs – работа с кодировками
# re – регулярные выражения
# \ - спец символ
# экранирует спец символы (\n, \t – табуляция, \’, \”, \\)

# Найти в тексте все вхождения слова Händel / Haendel / Handel => регулярные выражения
# | или, ? предыдущего символа может не быть, в () - группировка, . один любой символ: H(ä|ae?)ndel

# Регулярные выражения используются в текстовых редакторах, др. языках прогр. и т.д.
# модуль re


# M(u|ou?)'?a?mm?ar ((A|a|E|e)l)?-? (Q|G|Kh?)a(d(d|h(dh)?)|th|zz)aff?(i|y)
# | - или, * - предыдущий символ или группа повторены любое кол-во раз,
# + - предыдущий символ или группа повторены любое положительное кол-во раз
# .* - любое кол-во любых символов, .+ - любое количество > 1
# NB * берет максимальное количество символов
# [...] - один из перечисленных символов, [...-...] - один символ из диапазона
# Можно комбинировать: [a-zA-Zбв]
# Экранирование метасимволов \[, \(, \], \), \*...
# Итак...

import re

# m = re.search(regex, s)
# if m != None:
#   print('Я нашел!')
#   print(m.group())

# regcat = '\bкот(ы|у|е|о[мв]|a(х|ми?)?)?\b'
# \b - граница слова, перед кавычкой r!!!


#1 написать рег. выр. для любого выражения
#2 функция, спрашивающая слова и говорящая, являются ли они формой данного существительного
