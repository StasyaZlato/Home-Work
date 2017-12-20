from flask import Flask
from flask import request, render_template, redirect, url_for
import re
import urllib.request
import os


app = Flask(__name__)


# Чтобы скачать страницу
def download(pageurl):
    try:
        page = urllib.request.urlopen(pageurl)
        html = page.read().decode('utf-8')
        return html
    except:
        print('Error at ', pageurl)


# Вытаскиваем инфу из погоды, возвращаем список данных
def weather_infa(html_str):
    script = re.compile('<script.*?>.*?</script>', re.DOTALL)
    style = re.compile('<style.*?>.*?</style>', re.DOTALL)
    html_str = re.sub(script, '', html_str)
    html_str = re.sub(style, '', html_str)
    tag = re.compile('<.*?>', re.DOTALL)
    html_str = re.sub(tag, '', html_str)
    html_str = re.sub('\s\s+', '\n', html_str)
    import html
    inf = html.unescape(html_str)
    infa = re.compile('МакедонияПогода в Скопье сейчас(.*?Сегодня)', re.DOTALL)
    inf = re.search(infa, inf).group(1)
    list_i = inf.split('\n')
    for i in list_i:
        if i == '':
            list_i.remove(i)
    list_i[3] = list_i[3] + ' ' + list_i[4]
    list_i[0] = list_i[0] + ' ' + list_i[1]
    list_i.remove(list_i[4])
    list_i.remove(list_i[1])
    list_i[1] = 'Температура: ' + list_i[1]
    list_i[3] = list_i[4] + ' ' + list_i[3]
    list_i.remove(list_i[4])
    return list_i


# читаем словарик (его обработка - в файле dictionary_file.py)
def dict_slav():
    old_slavic_dict = {}
    with open('dict.csv', 'r', encoding='utf-8') as f:
        dictionary = f.readlines()
        dict_list = [line.lower() for line in dictionary]
        for line in dict_list:
            line = line.split('\t')
            old_slavic_dict[line[0]] = line[1].strip('\n')
    return old_slavic_dict


# html страницу lenta.ru в файл
def news_text():
    news_t = download('https://lenta.ru')
    with open(os.path.join('.\\templates', 'news.html'), 'w', encoding='utf-8') as f:
        f.write(news_t)
    return news_t


# лемматизируем
def mystem(text):
    f = os.path.join('.', 'text.txt')
    f_path_new = os.path.join('.', 'text1.txt')
    # Не уверена, поймет ли майстем строки, поэтому запихну текст в файл (UPD Точно не понимает...)
    with open(f, 'w', encoding='utf-8') as n:
        n.write(text)
    mystem_path = os.path.join('.', 'mystem.exe')
    os.system(mystem_path + " -cid " + f + ' ' + f_path_new)
    os.remove(f)
    with open(f_path_new, 'r', encoding='utf-8') as k:
        text = k.read()
    return text


# ищем самые частотные 10 слов (получается немного больше, потому что по несколько слов имеют
# одинаковую частоту)
def freq_10(text):
    text_list = text.split()
    dic = {i: 0 for i in text_list}
    for i in text_list:
        dic[i] += 1
    inv_dic = {v: [] for v in dic.values()}
    nums = list(dic.values())
    words = list(dic.keys())
    for i in range(len(nums)):
        if dic[words[i]] == nums[i]:
            inv_dic[nums[i]].append(words[i])
    max10 = []
    for i in range(10):
        max10.append(max(nums))
        nums.remove(max(nums))
    top10 = {', '.join(inv_dic[i]): i for i in max10}
    return top10


# общий транслит. Очень длинный и некрасивый, и его можно было бы укоротить больше чем вдвое,
# но я этого, конечно, делать не буду.
# зато формы слов видит.
def translit_main(text):
    dic = dict_slav()
    text_list = mystem(text).lower().split()
    regex = re.compile('(.*?){(.*?)=.*?}(.?)')
    regex1 = re.compile('(.*?){.*?\?\?}(.?)')
    flex_adj = {'ая': 'ая',
                'ий': 'ій',
                'ый': 'ый',
                'ое': 'ое',
                'ой': 'ой',
                'ей': 'ѣй',
                'ого': 'аго',
                'ому': 'ому',
                'ую': 'ую',
                'ым': 'ымъ',
                'ом': 'омъ',
                'яя': 'яя',
                'ее': 'ее',
                'его': 'яго',
                'ему': 'ѣму',
                'юю': 'юю',
                'ем': 'ѣмъ',
                'ых': 'ыхъ',
                'их': 'ихъ',
                'им': 'имъ',
                'ыми': 'ыми',
                'ими': 'ими'}
    flex_noun = {'я': 'я',
                 'а': 'а',
                 'ы': 'ы',
                 'е': 'ѣ',
                 'у': 'у',
                 'ой': 'ой',
                 'ом': 'омъ',
                 'и': 'и',
                 'ю': 'ю',
                 'ей': 'ѣй',
                 'ем': 'емъ',
                 'ам': 'амъ',
                 'ами': 'ами',
                 'ах': 'ахъ',
                 'ям': 'ямъ',
                 'ями': 'ями',
                 'ях': 'яхъ',
                 'ов': 'овъ',
                 'ии': 'іи'}
    new_text = []
    for i in range(len(text_list)):
        if re.search(regex, text_list[i]) is not None:
            word = re.search(regex, text_list[i]).group(2)
            word_form = re.search(regex, text_list[i]).group(1)
            punct = re.search(regex, text_list[i]).group(3)
            if word == word_form and word in dic.keys():
                new_text.append(dic[word] + punct)
                continue
            if word in dic.keys():
                word = dic[word]
            else:
                if word.endswith(('б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ')):
                    word += 'ъ'
                for l in range(len(word)):
                    try:
                        next_letter = word[l + 1]
                    except IndexError:
                        next_letter = ''
                    if word[l] == 'и' and next_letter in 'аеёийоуыэюя':
                        word = re.sub(word[l]+next_letter, 'і'+next_letter, word)
                # приставки
                if re.search('^бес\S', word) is not None:
                    word = re.sub('бес', 'без', word)
                if re.search('^черес\S', word) is not None:
                    word = re.sub('бес', 'без', word)
                if re.search('^черес\S', word) is not None:
                    word = re.sub('бес', 'без', word)
                if re.search('^расс', word) is not None:
                    word = re.sub('расс', 'разс', word)
                if re.search('^восс', word) is not None:
                    word = re.sub('восс', 'возс', word)
                if re.search('^исс', word) is not None:
                    word = re.sub('исс', 'изс', word)
                    # сохраняем (спокойствие) пунктуацию
            try:
                word_next = text_list[i+1]
            except IndexError:
                word_next = ''
            if '=a=' in text_list[i] or '=a,' in text_list[i]:
                new_text.append(translit_adj(word, word_form, flex_adj, word_next) + punct)
            elif 'прич' in text_list[i]:
                new_text.append(translit_ptcp(word_form, flex_adj,word_next, dic) + punct)
            elif '=s=' in text_list[i] or '=s,' in text_list[i]:
                new_text.append(translit_nouns(word, word_form, flex_noun, text_list[i]) + punct)
            else:
                if word_form.endswith(('б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ')):
                    word_form += 'ъ'
                for l in range(len(word_form)):
                    try:
                        next_letter = word_form[l + 1]
                    except IndexError:
                        next_letter = ' '
                    if word_form[l] == 'и' and next_letter in 'аеёийоуыэюя':
                        word_form = re.sub(word_form[l]+next_letter, 'і'+next_letter, word_form)
                new_text.append(word_form + punct)
        elif re.search(regex1, text_list[i]) is not None:
            word_form = re.search(regex1, text_list[i]).group(1)
            punct = re.search(regex1, text_list[i]).group(2)
            new_text.append(word_form + punct)
    return ' '.join(new_text)


# транслит прилагательных
def translit_adj(word, word_form, flex_adj, word_next):
    word_slav = ''
    regex1 = re.compile('[оы]й\??')
    regex2 = re.compile('[іи]й\??')
    if word.endswith('?'):
        word = word[:-1]
    for f in flex_adj.keys():
        if word_form.endswith(f):
            word_slav = word[:-2] + flex_adj[f]
            break
    if word_form.endswith('ие') or word_form.endswith('ые'):
        if 'жен' in word_next or 'сред' in word_next:
            if re.search(regex2, word) is not None:
                word_slav = re.sub(regex2, 'ія', word)
            else:
                word_slav = re.sub(regex1, 'ыя', word)
        else:
            word_slav = word_form
    else:
        word_slav = word_form
    return word_slav


# транслит причастий
def translit_ptcp(word_form, flex_adj, word_next, dic):
    word_slav = ''
    word0 = word_form
    if word_form.endswith(('щая', 'щее', 'щей', 'щего', 'щему', 'щую', 'щим', 'щем', 'щие', 'щих', 'щими')):
        regex = re.compile('щ(.+)')
        flex = re.search(regex, word_form).group(0)
        word0 = re.sub(flex, 'щий', word_form)
    elif word_form.endswith(('ая', 'ое', 'ой', 'ую', 'ом', 'ые', 'ых', 'ым')):
        word0 = word_form[:-2] + 'ый'
    elif word_form.endswith(('ого', 'ому', 'ыми')):
        word0 = word_form[:-3] + 'ый'
    elif word_form.endswith(('яя', 'ее', 'ей', 'юю', 'ем', 'ие', 'их', 'им')):
        word0 = word_form[:-2] + 'ий'
    elif word_form.endswith(('его', 'ему', 'ими')):
        word0 = word_form[:-3] + 'ий'
    if word0 in dic:
        word0 = dic[word0]
    else:
        if word0.endswith(('б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ')):
            word0 += 'ъ'
        for l in range(len(word0)):
            try:
                next_letter = word0[l + 1]
            except IndexError:
                next_letter = ' '
            if word0[l] == 'и' and next_letter in 'аеёийоуыэюя':
                word0 = re.sub(word0[l] + next_letter, 'і' + next_letter, word0)
    for f in flex_adj.keys():
        if word_form.endswith(f):
            word_slav = re.sub('.й', flex_adj[f], word0)
            break
        else:
            word_slav = word0
    if word_form.endswith('ие') or word_form.endswith('ые'):
        if 'жен' in word_next or 'сред' in word_next:
            if re.search('ие', word_form) is not None:
                word_slav = re.sub('.й', 'ія', word0)
            else:
                word_slav = re.sub('.й', 'ыя', word0)
        else:
            word_slav = word0
    return word_slav


# транслит существительных
def translit_nouns(word, word_form, flex_noun, mystem_w):
    word_slav = ''
    if word.endswith('?'):
        word = word[:-1]
    # на ять должно заменяться только в косвенных падежах
    if 'им' in mystem_w and word_form.endswith('е'):
        word_slav = word
    else:
        for f in flex_noun.keys():
            if word_form.endswith(f):
                if word.endswith(('б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц',
                                  'ч', 'ш', 'щ')):
                    word_slav = word + flex_noun[f]
                else:
                    word_slav = word[:-1] + flex_noun[f]
                break
            else:
                word_slav = word
    return word_slav


# из-за чего появились квадратики - хз, но они вроде на месте знаков препинания и некоторых цифр.
# что-то странное, в общем
def translit_html(html_str):
    import html
    html_str = html.unescape(html_str)
    reg1 = re.compile('<script.*?>.*?</script>', re.DOTALL)
    html_str = re.sub(reg1, '', html_str)
    reg2 = re.compile('<.*?>')
    html_str = re.sub(reg2, '\n', html_str)
    spaces = re.compile('(\s)\s+', re.DOTALL)
    html_str = re.sub(spaces, '\1', html_str)
    html_str = translit_main(html_str)
    return html_str


# Главная страница - форма с транслитом и погода в Скопье
@app.route('/')
def index():
    text = ''
    list_i = weather_infa(str(download('https://www.gismeteo.ru/weather-skopje-3253/now/')))
    if request.args:
        text = request.args['translit']
        text_slav = translit_main(text)
        return render_template('form.html', list_i=list_i, text=text_slav)
    return render_template('form.html', list_i=list_i, text=text)


# Вторая страница - лента.ру в дореволюционном и строчка с 10 СЧС
@app.route('/news')
def news():
    html_str1 = news_text()
    html_str = translit_html(html_str1)
    html_list = html_str.split('')
    dic = freq_10(html_str)
    qual = len(html_list)
    return render_template('news_page.html', text=html_list, dic=dic, qual=qual)


# Третья страница - тест на ять 
@app.route('/test')
def test():
    global dic_test
    dic_test = {1: [url_for('static', filename='bread.jpg'), 'bread', ['Хлѣбъ', 'Хлебъ']],
                2: [url_for('static', filename='forest.jpg'), 'forest', ['Лѣсъ', 'Лесъ']],
                3: [url_for('static', filename='flower.jpg'), 'flower', ['Цвѣтокъ', 'Цветокъ']],
                4: [url_for('static', filename='feather.jpg'), 'feather', ['Пѣро', 'Перо']],
                5: [url_for('static', filename='vedro1.jpg'), 'vedro', ['Вѣдро', 'Ведро']],
                6: [url_for('static', filename='repei.jpg'), 'repei', ['Рѣпей', 'Репей']],
                7: [url_for('static', filename='repa.jpg'), 'repa', ['Рѣпа', 'Репа']],
                8: [url_for('static', filename='sun.jpg'), 'star', ['Звѣзда', 'Звезда']],
                9: [url_for('static', filename='village.jpg'), 'country', ['Сѣло', 'Село']],
                10: [url_for('static', filename='lion.jpg'), 'lion', ['Лѣвъ', 'Левъ']]}
    if request.args:
        global answers_user
        answers_user = {'bread': request.args['bread'],
                        'forest': request.args['forest'],
                        'feather': request.args['feather'],
                        'flower': request.args['flower'],
                        'vedro': request.args['vedro'],
                        'repei': request.args['repei'],
                        'repa': request.args['repa'],
                        'star': request.args['star'],
                        'country': request.args['country'],
                        'lion': request.args['lion']}
        for k in dic_test.keys():
            if answers_user[dic_test[k][1]] == 'yat':
                answers_user[dic_test[k][1]] = dic_test[k][2][0]
            else:
                answers_user[dic_test[k][1]] = dic_test[k][2][1]
        global answers_correct
        answers_correct = {'bread': 'Хлѣбъ',
                           'forest': 'Лѣсъ',
                           'feather': 'Перо',
                           'flower': 'Цвѣтокъ',
                           'vedro': 'Ведро',
                           'repei': 'Репей',
                           'repa': 'Рѣпа',
                           'star': 'Звѣзда',
                           'country': 'Село',
                           'lion': 'Левъ'}
        global sum
        sum = 0
        for n in answers_user.keys():
            if answers_user[n] == answers_correct[n]:
                sum += 1
        return redirect(url_for('results'))
    return render_template('test.html', dic=dic_test)


@app.route('/test/results')
def results():
    return render_template('results.html', answers_user=answers_user, dic=dic_test, answers_correct=answers_correct, sum=sum)


# если незаполнен тест или что-то вроде - перенаправление на главную
@app.errorhandler(NameError)
def name_error(error):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
