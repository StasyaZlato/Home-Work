# импортируем все, что нужно

import urllib.request # для работы с сайтами
import re # регулярки
import os # ходить по папкам
import csv # табличка
import time # чтобы поставить перерывы между обращениями к серверу


# создаем папки 

def make_folders():
    directory = 'C:\\Users\\1\\Yoshkar-Ola'
    if not os.path.exists(directory):
        os.makedirs(directory) # создаем корневую директорию
    directories = [directory + '\\plain', directory + '\\mystem-xml', directory + '\\mystem-plain']
    for dirs in directories: # создаем каталоги для текстов   
        if not os.path.exists(dirs):
            for year in range(2014, 2018): # папки по годам
                folder_year = dirs + '\\' + str(year)
                if not os.path.exists(folder_year):
                    os.makedirs(folder_year)
                for month in range(1,13): # папки по месяцам (второй аргумент range - не входит в промежуток)
                    folder_month = folder_year + '\\' + str(month)
                    if not os.path.exists(folder_month):
                        os.makedirs(folder_month)
    print('Директории созданы.')


# функция, скачивающая любую страницу

def download(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl) # берем страницу
        html = page.read().decode('utf-8') # достаем html
        return html 
    except:
        print('Error at ', pageUrl) 

 
# ф-я, ищущая на странице новостей ссылки на отдельные статьи

def find_news_URL(url_main):
    references = []
    content_main = download(url_main) # скачиваем страницу раздела
    reg_ref = re.compile('<h2 class="entry-title"><a href="(.*?)" rel="bookmark">', re.DOTALL) # регулярка для ссылки
    ref = re.findall(reg_ref, content_main) # ищем
    for r in ref:
        ref1 = re.sub('<h2.*?><a href="', '', r) # убираем теги из найденного
        reference = re.sub('" rel="bookmark">', '', ref1)
        references.append(reference) # кидаем в итоговый массив
    return references


# ф-я, ищущая номер последней страницы архива новостей 
# на каждой странице отображаются номер первой, предыдущей, следущей и последней страниц

def last_page():
    url = 'https://gg12.ru/category/novosti/'
    html = download(url)
    reg_pages = re.compile('<a class=\'page-numbers\'.*?>(\d+)</a>', re.DOTALL) # ищем все видные на странице номера страниц
    pages = re.findall(reg_pages, html)
    nums = []
    for i in pages:
        i1 = re.sub(reg_pages, '\1', i) # вычленяем только число между тегами
        nums.append(int(i1))
    return max(nums) # страница с максимальным номером - и есть последняя


# mystem принимает только файлы с названием на латинице. Мне лень переделывать красивую функцию, 
# называющие файлы по названию статьи. Легче написать еще одну для транслитерации xD

def transliter(string):
    dic_alph_cyr_lat = {'а':'a',
                       'б':'b',
                       'в':'v',
                       'г':'g',
                       'д':'d',
                       'е':'e',
                       'ё':'e',
                       'ж':'zh',
                       'з':'z',
                       'и':'i',
                       'й':'j',
                       'к':'k',
                       'л':'l',
                       'м':'m',
                       'н':'n',
                       'о':'o',
                       'п':'p',
                       'р':'r',
                       'с':'s',
                       'т':'t',
                       'у':'u',
                       'ф':'f',
                       'х':'h',
                       'ц':'ts',
                       'ч':'ch',
                       'ш':'sh',
                       'щ':'sch',
                       'ъ':'',
                       'ы':'y',
                       'ь':'',
                       'э':'e',
                       'ю':'yu',
                       'я':'ya',
                       ' ':'_'} # словарь кириллица VS латиница
    string = string.lower() # Приведем строку к нижнему регистру, потому что иначе аббревиатуры будут выглядеть некрасиво
    for cyrillic, latin in dic_alph_cyr_lat.items():
        string = string.replace(cyrillic, latin)
    return string


# ф-я, проходящая по всем папкам директории и достающая оттуда все файлы

def list_files(path):
    files_list = []
    for d, dirs, files in os.walk(path):
        for f in files:
            path_f = os.path.join(d, f)
            files_list.append(path_f)
    return files_list


# ф-я, определяющая будущее название файла
# и путь к нему

def path_html(url, html):
    path_base = 'C:\\Users\\1\\Yoshkar-Ola\\plain' 
    metadata = meta(url, html) # ищем данные для определения пути
    date = metadata['created']
    date_f = date.split('.') 
    date_year = date_f[2] # год
    date_month = int(date_f[1]) # месяц. int - чтобы убрать 0 в начале (напр. 04)
    prob_illegal_title = transliter(metadata['header']) 
    illegal = re.compile('[\?#%&\*\.,\|:\"«»<>/№;!–-—]') # убираем все "незаконные" символы 
    title = re.sub(illegal, '', prob_illegal_title)
    if title.count('\\') > 0: # почему-то регуляркой backslash не захотел убираться, прописываем отдельно
        title = title.replace('\\', '')
    path = path_base + '\\' + date_year + '\\' + str(date_month) + '\\' + title + '.txt'
    return(path)


# ф-я, вытаскивающая из html инфу для начала файла

def inf(file, URL, html):
    metadata = meta(URL, html)
    with open(file, 'a', encoding = 'utf-8') as f:
        f.write('@au ' + metadata['author'] + '\n')
        f.write('@ti ' + metadata['header'] + '\n')
        f.write('@da ' + metadata['created'] + '\n')
        f.write('@topic ' + metadata['topic'] + '\n')
        f.write('@url ' + URL + '\n' + '\n')
        f.close()


# ф-я, очищающая html от тегов и иже с ними

def clean(text):
    # убираем все под тегом <head>
    reg_head = re.compile('<head>.*?</head>', re.DOTALL)
    clean_html = re.sub(reg_head, '', text)
    # убираем все ссылки
    reg_ref = re.compile('<a .*?>.*?</a>', re.DOTALL)
    clean_html = re.sub(reg_ref, '', clean_html)
    # убираем "Читайте также"
    reg_related = re.compile('<div class="related-content-wrapper">.*?</div><!-- related-content-wrapper -->', re.DOTALL)
    clean_html = re.sub(reg_related, '', clean_html)
    # убираем комменты
    reg_com = re.compile('<!--.*?-->', re.DOTALL)
    clean_html = re.sub(reg_com, '', clean_html)
    # убираем возрастное ограничение
    reg_age = re.compile('<section id="text-8" class="widget widget_text">.*?<div class="textwidget">.*?</div>', re.DOTALL)
    clean_html = re.sub(reg_age, '', clean_html)
    # убираем сегодняшнюю дату
    reg_tdate = re.compile('<div class="date-section">.*?<\/div>', re.DOTALL)
    clean_html = re.sub(reg_tdate, '', clean_html)
    # убираем все скрипты
    reg_script = re.compile('<script.*?>.*?</script>', re.DOTALL)
    clean_html = re.sub(reg_script, '', clean_html)
    # убираем заголовки - они есть в шапке
    reg_titles = re.compile('<h(1|2|3|4).*?>.*?</h(1|2|3|4)>', re.DOTALL)
    clean_html = re.sub(reg_titles, '', clean_html)
    # убираем строчку поделиться - иначе она уходить не хочет
    reg_share = re.compile('<p class="screen-reader-text juiz_sps_maybe_hidden_text">.*?</p>', re.DOTALL)
    clean_html = re.sub(reg_share, '', clean_html)
    # наконец, убираем непосредственно все теги
    reg_tags = re.compile('<.*?>', re.DOTALL)
    html_clean = re.sub(reg_tags, '', clean_html)
    # убираем встречающиеся в html символы |
    html_clean = re.sub('\|', '', html_clean)
    # убираем лишние табуляции и пустые строки
    hc = re.sub('\t{2,}', '', html_clean)
    hc = re.sub('\s{2,}', '\n', hc)
    # если не убирать тег span, то находится много лишнего до и после текста. Если убирать - часть
    # статей, в которых контент тоже оформлен в этот тег, остается пустой. Поэтому просто обрезаем 
    # всю оставшуюся ерунду
    reg_content = re.compile('Найти:(.*?)Просмотров:.*?gg12.ru', re.DOTALL)
    content_1 = re.search(reg_content, hc)
    content = content_1.group(1)
    hc = re.sub(reg_content, content, hc)
    # обрезаем пробелообразные символы в начале и в конце
    hc = hc.strip()
    # убираем html-символы 
    import html
    hc = html.unescape(hc)
    return hc


# Ф-я, инвертирующая словарь

def invert_dic(d):
    inverted_dic = {value:key for key, value in d.items()}
    return inverted_dic


# ф-я, вытаскивающая метаданные из html

def meta(URL, html):
    reg_author = re.compile('<div class="entry-meta">(.*?)<span class="author vcard">(.*?)</a>', re.DOTALL) # регулярка для автора
    reg_title = re.compile('<h1 class="entry-title">(.*?)</h1>', re.DOTALL) # регулярка для заголовка
    reg_created = re.compile('<div class="entry-meta">.*?<time.*?>(.*?)</time>', re.DOTALL) # регулярка для даты
    reg_topic = re.compile('<span class="tags-links">Tagged(.*?)</span>', re.DOTALL) # регулярка для категории
    author1 = re.search(reg_author, html) # ищем рег1 - автора
    if author1 != None:
        author2 = author1.group(2)
        author = re.sub('<.*?>', '', author2) # т.к. регулярка неаккуратная (иначе была бы слишком длинной), приходится еще избавляться от тегов
    else:
        author = ''
    title = re.search(reg_title, html).group(1) # ищем рег2 - заголовки
    created = re.search(reg_created, html) # ищем рег3 - дата
    created1 = created.group(1)
    topic1 = re.search(reg_topic, html)
    if topic1 != None:
        topic2 = topic1.group(1) # ищем рег4 - категории
        topic = re.sub('<.*?>', '', topic2) # регулярка опять корявая, поэтому снова убираем теги
    else:
        topic = ''
    dic_meta = {'author': author, 'sex': '', 'birthday': '', 'header': title, 'created': created1, 'sphere': 'публицистика', 'genre_fi': '', 'type': '', 'topic': topic, 'chronotop': '', 'style': 'нейтральный', 'audience_age': 'н-возраст', 'audience_level': 'н-уровень', 'audience_size': 'городская', 'source': URL, 'publication': 'Йошкар-Ола', 'publisher': '', 'publ_year': created1[-4:], 'medium': 'газета', 'country': 'Россия', 'region': 'Марий-Эл', 'language': 'ru'} # создаем словарь
    return dic_meta


# ф-я, создающая csv таблицу

def csv_meta_base():
    file = 'C:\\Users\\1\\Yoshkar-Ola\\metadata.csv'
    # заливаем все переменные в список
    data = [['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age', 'audience_level', 'audience_size', 'source', 'publication', 'publisher', 'publ_year', 'medium', 'country', 'region', 'language']]
    # воспользуемся модулем csv
    with open(file, 'w', newline = '') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(data)
    print('Шаблон таблицы csv создан.')


# Ф-я, заполняющая строки таблицы

def meta_csv(ref, html, file): # ref - ссылка, html - текст html, file - путь к файлу. 
    # Можно было обойтись ссылкой, но тогда пришлось бы лишний раз обращаться к серверу для скачки материалов
    meta_csv = []
    metadata = meta(ref, html) # берем метаданные конкретного файла
    meta_list = [file] # в метаданных изначально нет сочетания путь:значение пути, его заливаем в нужный список отдельно
    inv_meta = invert_dic(metadata)
    meta_list.extend(inv_meta.keys())
    meta_csv.append(meta_list)
    with open('C:\\Users\\1\\Yoshkar-Ola\\metadata.csv', 'a', newline = '') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(meta_csv)


# ф-я, заливающая обработанные html в соотв. папки директории plain

def plain():
    url = 'https://gg12.ru/category/novosti/page'
    last = last_page()
    # i - по количеству страниц в архиве
    for i in range(1, last+1):
        # url каждой страницы вполне ищется при добавлении "page№" или "page/№" в конце ссылки 
        url1 = url + str(i)
        refs = find_news_URL(url1)
        # идем по ссылкам на странице
        for ref in refs:
            try:
                html = download(ref) # скачиваем
                file = path_html(ref, html) # даем файлу имя
                    # проверяем наличие файла в директории
                if not os.path.exists(file):
                    inf (file, ref, html)
                    html_clean = clean(html) # чистим
                    with open(file, 'a', encoding = 'utf-8') as f:
                        f.write(html_clean)
                        f.close()
                    meta_csv(ref, html, file)
                    # делаем паузу между запросами
                time.sleep(2)
            except:
                print('Error at ', ref)
    print('Выкачка файлов в папку plain завершена. Таблица csv заполнена.')

# при последней проверке в ошибку уходила единственная страница с ломаным заголовком - в заголовок 
# умудрились запихнуть весь текст статьи, программа ломалась


# После первой обработки всего массива файлов в mystem оказалось, что часть файлов выпадают в ошибку. 
# У этих файлов в названии оказались несколько пропущенных мной в программе создания пути к файлу "нелегальных" (для mystem) символов. 
# Я исправила ошибку в теле кода, но выкачивать все 2000+ файлов с сайта заново кажется не очень оправданным. Поэтому делаем ф-ю, 
# переименовывающую файлы в директории, если в них оказались символы, не принимаемые mystem-ом.

def rename_file(directory):
    files = list_files(directory)
    regex= re.compile('[\?#%&\*,\|:\"«»<>/№;!–-—`]') # еще раз пропишу все символы
    for f in files:
        list_n = f.split('\\')
        name = list_n[-1]
        if re.search(regex, name) != None: 
            new_name = re.sub(regex, '', name)
            new_name = re.sub('__', '_', new_name)
            list_n1 = list_n[:-1]
            list_n1.append(new_name)
            new_name_path = '\\'.join(list_n1)
            os.rename(f, new_name_path)
    print('Файлы в директории переименованы.')


# Убираем строки с метаданными из файлов mystem папок

def cut_meta(path):
    with open(path, 'r', encoding = 'utf-8') as f: 
        text = f.readlines()
        text_wm_l = text[6:]
        text_wm = ''.join(text_wm_l)
        f.close()
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(text_wm)
        f.close()


# Размечаем майстемом в формате plain text

def mystem_plain():
    path_base = 'C:\\Users\\1\\Yoshkar-Ola\\plain'
    files = list_files(path_base) # берем все файлы директории plain
    #создаем на всякий случай файл, в который уйдут названия всех файлов с ошибками
    with open('C:\\Users\\1\\Yoshkar-Ola\\errors_mystem.txt', 'a', encoding='utf-8') as n: 
        n.write('Ф-я mystem_plain(). Ошибки при обработке следующих файлов: ' + '\n')
        n.close()
    for f in files:
        try:
            f_path_new = f.replace('plain', 'mystem-plain')
            if not os.path.exists(f_path_new): # обрабатываем все файлы mystem, если еще нет
                os.system("C:\\Users\\1\\mystem.exe -cid " + f + ' ' + f_path_new)
                cut_meta(f_path_new)
        except FileNotFoundError: # собственно единственная ошибка, которая возникала (кажется) из-за имени файла
            print('Ошибка при обработке файла ' + f)
            with open('C:\\Users\\1\\Yoshkar-Ola\\errors_mystem.txt', 'a', encoding='utf-8') as n:
                n.write(f + '\n')
                n.close()
    print('Обработка mystem файлов из директории plain в формате plain text завершена.')


# ф-я, обрабатывающая все файлы директории plain в mystem в формате xml

def mystem_xml():
    path_base = 'C:\\Users\\1\\Yoshkar-Ola\\plain'
    files = list_files(path_base)
    for f in files:
        try:
            f_path_new_txt = f.replace('plain', 'mystem-xml')
            f_path_new_xml = f_path_new_txt.replace('txt', 'xml')
            if not os.path.exists(f_path_new_xml):
                os.system("C:\\Users\\1\\mystem.exe -cid --format xml " + f + ' ' + f_path_new_xml)
                cut_meta(f_path_new_xml)
        except FileNotFoundError:
            print('Ошибка при обработке файла ' + f)
            # эти файлы уже не добавляем в файл с ошибками mystem, потому что в обеих функциях mystem ругается на одни и те же файлы
    print('Обработка mystem файлов из директории plain в формате xml завершена.')


# т.к. несколько файлов все равно может улететь в ошибку после mystem, и я не знаю, что с ними делать - вроде все норм - удалим их,
# чтобы во всех директориях было равное количество файлов. Для этого воспользуемся созданным файлом с названиями файлов-ошибок

def delete_error_files():
    with open('C:\\Users\\1\\Yoshkar-Ola\\errors_mystem.txt', 'r', encoding='utf-8') as f:
        errors = f.read()
        errors_l = errors.split('\n') # считываем файл с ошибками, отсекая перенос на другую строку! (я просто рассплитила по переносам)
    for error in errors_l: 
        if os.path.exists(os.path.join(error)): # как минимум первая строка - шапка "Ошибки были в следующих файлах..."
            os.remove(os.path.join(error))
            print('Файл ' + error + ' удален.')
    print('Файлы, на которых mystem ломается, удалены.')


# На всякий случай считаем слова

def count_words(directory):
    files = list_files(directory)
    words = 0
    for f in files:
        with open(f, 'r', encoding = 'utf-8') as k:
            text = k.readlines()
            text_wm = text[6:] # считаем без метаданных в шапке файла
            text_wm_str = ''.join(text_wm)
            text_l = text_wm_str.split()
            words += len(text_l)
    return words


# Т.к. папки создавались в большом количестве, но многие остались пустыми (напр., за декабрь 2017), удаляем пустые папки
# Пустых папок много, т.к. сайт газеты новый, и там есть статьи только начиная с конца 2016 года + 1 статья за 2014

def delete_empty_dirs(directory):
    for d in os.listdir(directory): # берем все папки директории
        a = os.path.join(directory, d) # пишем их адрес
        if os.path.isdir(a): # делаем то же с новыми папками 
            delete_empty_dirs(a) # рекурсия - пока не дойдем до дна:)
            if not os.listdir(a):
                os.rmdir(a)
                print('Директория ' + a + ' удалена')
                

def clean_html_signs_in_text(directory): # появились после создания информационной шапки - были в некоторых заголовках
    files = list_files(directory)
    for f in files:
        with open(f, 'r', encoding = 'utf-8') as k: # открываем и читаем
            text = k.read()
            k.close()
        import html
        text_clean = html.unescape(text) # редактируем
        with open(f, 'w', encoding = 'utf-8') as k:
            k.write(text_clean)
            k.close
    print('HTML символы из файлов удалены')


def main():
    make_folders()
    csv_meta_base()
    plain()
    directory = 'C:\\Users\\1\\Yoshkar-Ola'
    directory1 = 'C:\\Users\\1\\Yoshkar-Ola\\plain'
    clean_html_signs_in_text(directory1)
    rename_file(directory1)
    mystem_plain()
    mystem_xml()
    delete_error_files()
    os.remove('C:\\Users\\1\\Yoshkar-Ola\\errors_mystem.txt')
    delete_empty_dirs(directory)
    print('Все пустые директории удалены.')
    print('Количество слов в корпусе ' + str(count_words(directory1)))
    print('Готово.')


main()
