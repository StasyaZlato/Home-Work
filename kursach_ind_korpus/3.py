import urllib.request
import re
import download_module as down
from bs4 import BeautifulSoup as bs


text_try = '''Barat dan Timur adalah guruku Muslim, Hindu, Kristen, Buddha,
# Pengikut Zen dan Tao
# Semua adalah guruku
# Kupelajari dari semua orang saleh dan pemberani
# Rahasia cinta, rahasia bara menjadi api menyala
# Dan tikar sembahyang sebagai pelana menuju arasy-Nya
# Ya, semua adalah guruku
# Ibrahim, Musa, Daud, Lao Tze Buddha, Zarathustra,
# Socrates, Isa Almasih Serta Muhammad Rasulullah
# Tapi hanya di masjid aku berkhidmat
# Walau jejak-Nya
# Kujumpai di mana-mana.'''

# text_try = '''Walau jejak-Nya
# Kujumpai di mana-mana.'''


# Самая очевидная ф-я. Берем адрес, добавляем слово - ищем. На самом деле,
# None не появится никогда (если без ошибок), потому что там выдается страница,
# что слово не найдено. Она не парсится
def take_word_page(word):
    html = down.download('https://kbbi.web.id/' + word.lower())
    if html is None:
        print('Сорян, слово не найдено! Печалька :(')
    else:
        with open(r'html_changing.txt', 'w', encoding='utf-8') as f:
            f.write(down.del_html(html.replace('&#183;', '')))
        return down.del_html(html.replace('&#183;', ''))


# Уууу... а вот тут буит мясо
def word_information(html):
    # На всякий
    if html is not None:
        # тут у некоторых слов есть второе значение (в другой словарной статье),
        # тогда там появляется штука вроде <b>some word<sup>1</sup></b>, из-за
        # этого все чуть-чуть ломается временами. Но нам это не нужно, правда?..
        html = re.sub('<sup>.*?</sup>', '', html)
        # супим хтмл
        soup = bs(html, 'lxml')
        # ищем нужный тег
        container = soup.find('div', {'id': 'd1'})
        terms_tag = container.find_all('b')
        parts_tag = container.find_all('em')
        terms = []
        parts1 = []
        # достаем из распарсенных тегов текст
        for i in terms_tag:
            text = i.get_text()
            terms.append(text)
        for i in parts_tag:
            text = i.get_text()
            parts1.append(text)
        # Очень сложно. Нужно отсеять непосредственно термины (коих в одной статье
        # несколько - все однокоренные формы) от их коллокаций (напр., запись вроде
        # ~ air - это сочетание искомого слова с air. Ну и нумерация значений
        # тоже жирным обозначается
        i = 0
        while i + 1 <= len(terms):
            if '--' in terms[i] or '~' in terms[i] or '- ' in terms[i] or ' -' in terms[i] or ',' in terms[i] or re.search('\d', terms[i]) is not None:
                terms.remove(terms[i])
            else:
                i += 1
        k = 0
        parts = []
        # контекстный костыль. кое-где курсивом выделены целые предложения, или (sic!)
        # сочетания пометы вроде Sas с частью речи, откуда нам нужна только часть речи.
        # Приходится это дело сперва сплитить,...
        for t in parts1:
            c = t.split()
            for i in c:
                parts.append(i)
        # ...а после фильтровать.
        while k + 1 <= len(parts):
            a = parts[k]
            if a != 'n' and a != 'v' and a != 'pron' and a != 'adv' and a != 'a' and a != 'num' and a != 'p':
                parts.remove(a)
            else:
                k += 1
        print(terms)
        print(parts)
        # несмотря на все ухищрения, иногда какой-то мусор остается, и тогда съезжает
        # размерность. Приходится бороться - против лома, как говорится...
        try:
            dict_p = {terms[num]: parts[num] for num in range(len(terms))}
            with open('DICTIONARY.txt', 'r', encoding='utf-8') as f:
                dict_text = f.read()
            with open('DICTIONARY.txt', 'a', encoding='utf-8') as f:
                for k, v in dict_p.items():
                    line = k + '\t' + v
                    if re.search(line, dict_text) is None:
                        f.write(line + '\n')
            return dict_p
        except IndexError:
            print('Упс! Опять циферки не совпали :(')
            return {}
    else:
        return None


def main():
    regex_word = re.compile('([a-zA-Z-]+)')
    text_1 = re.split(regex_word, text_try)
    text_new = []
    with open('DICTIONARY.txt', 'r', encoding='utf-8') as f:
        dict_text = f.readlines()
        dict1 = {}
        for l in dict_text:
            line = l.split('\t')
            dict1[line[0]] = line[1].strip()
    for i in range(len(text_1)):
        if re.search('\w', text_1[i]) is not None:
            word = text_1[i]
            if word in dict1.keys():
                print('Ура! Слово ' + word + ' в словарике!')
                inf = {word: dict1[word]}
            elif word.lower() in dict1.keys():
                print('Ура! Слово ' + word + ' в словарике!')
                inf = {word: dict1[word.lower()]}
            # else:
            #     if word.startswith('ter'):
            #         take_word_page(word[3:])
            else:
                take_word_page(word)
                with open(r'html_changing.txt', 'r', encoding='utf-8') as f:
                    html = f.read()
                inf = word_information(html)
                if inf == {}:
                    if word.lower().startswith('ter'):
                        html = take_word_page(word[3:])
                        inf = word_information(html)
                    if word.endswith('ku') or word.endswith('mu'):
                        html = take_word_page(word[:-2])
                        inf = word_information(html)
                    elif word.lower().endswith('-nya'):
                        html = take_word_page(word[:-4])
                        inf = word_information(html)
                    elif word.endswith('kau') or word.endswith('nya'):
                        html = take_word_page(word[:-3])
                        inf = word_information(html)
                    # такое правда у одного автора сплошь и рядом встречалось
                    elif word.lower().startswith('ku') or word.lower().startswith('di'):
                        # html = take_word_page(word[2:])
                        inf = {word: 'v'}
                    elif '-' in word:
                        word_new = word.split('-')[0]
                        html = take_word_page(word_new)
                        inf = word_information(html)
                    elif re.match('[A-Z]', word) is not None:
                        inf = {word: 'n'}
            # Очень тупо, конечно, расставлять инфы в каждом условии, но как еще
            # вставить уникальный инф в последний элиф, я придумать не могу. Так что
            # ДА БУДУТ КОСТЫЛИ
            text_new.append(word + str(inf))
        else:
            text_new.append(text_1[i])
    return ''.join(text_new)
print(main())


# with open('DICTIONARY.txt', 'r', encoding='utf-8') as f:
#     dict_text = f.readlines()
#     dict1 = {}
#     for l in dict_text:
#         line = l.split('\t')
#         dict1[line[0]] = line[1]
# print(dict1)