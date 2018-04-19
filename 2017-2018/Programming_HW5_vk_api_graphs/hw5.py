# Тут использованы прекрасные библиотеки vk и vk_api. Да, все то же можно было сделать через
# urllib, но это вышло бы значительно дольше (как минимум, у urllib есть свое ограничение на
# длину запросов, не позволяющее собрать сразу весь пласт информации в один запрос) и объемнее.
# А еще придется установить seaborn, если еще не.

# Все это замечательно устанавливается через pip install, если что.


import json
from time import sleep
import vk
import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# seaborn - это (как написано в интернете) "обертка" над matplotlib, тут посимпатичней дизайн и
# поменьше кода на единицу графиков


ACCESS_TOKEN = input('Введите access-token:\n')
session = vk.Session(access_token=ACCESS_TOKEN)
api = vk.API(session, v=5.74)


# данные в бд - из сообщества Обитель Лесной Ведьмы, owner_id = -42311101
OWNER_ID = int(input('Введите id сообщества для выкачки. \nЕсли на главной стронице сообщества отображается '
                     'короткое имя сообщества (domain), откройте один из постов сообщества. \nАдрес поста сообщества '
                     'будет выглядеть следующим образом: https://vk.com/{DOMAIN}?w=wall{OWNER_ID}_{POST_ID}. '
                     '\nСкопируйте часть "OWNER_ID" (со знаком минус в начале!).\nOwner_id: '))
NAME_OF_DB = 'Data_Base_' + str(OWNER_ID)[1:] + '.sqlite'


# Заранее создаем все необходимые папки.
def make_folder(name):
    path = '.\\{}\\'.format(name)
    if not os.path.exists(path):
        os.mkdir(path)


# Создаем бд с необходимыми таблицами.
def making_bd():
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts(post_id INTEGER UNIQUE, 
        from_id INTEGER NOT NULL, 
        signer_id INTEGER, 
        post_text VARCHAR, 
        text_len INTEGER, 
        comments_num INTEGER, 
        comments_av_len INTEGER, 
        attachments VARCHAR)''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments(comment_id INTEGER UNIQUE NOT NULL, 
        post_id INTEGER NOT NULL, 
        from_id INTEGER NOT NULL, 
        comment_text VARCHAR, 
        comment_len INTEGER,
        comment_attachments VARCHAR)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users(user_id INTEGER UNIQUE NOT NULL, 
        city_id INTEGER, 
        city_title VARCHAR,
        bdate VARCHAR,
        age VARCHAR)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ages(age INTEGER UNIQUE NOT NULL,
            num_users INTEGER,
            num_comments INTEGER,
            num_posts INTEGER, 
            av_comment INTEGER, 
            av_post INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS cities(city_title VARCHAR UNIQUE,
                num_users INTEGER,
                num_comments INTEGER,
                num_posts INTEGER, 
                av_comment INTEGER, 
                av_post INTEGER)''')
    conn.commit()


# Собираем посты сообщества.
def take_posts():
    posts_list = []
    offset = 0
    # Сейчас скачивается вся стена сообщества. Чтобы скачать кусок, достаточно
    # поменять True на offset < 201, например (тогда скачается 300 записей). Выход из цикла
    # предусмотрен if-ом, и он работает. Просто долговато скачивать 6000 записей на проверке
    print('Offsets:', end=' ')
    while True:
        posts = api.wall.get(owner_id=OWNER_ID, count=100, offset=offset, filter='all')
        if not posts['items']:
            break
        print(offset)
        posts_list.extend(posts['items'])
        # на всякий, потому что жадный вк не хочет отдавать больше 3 запросов в секунду. Не люблю ловить исключения.
        sleep(1)
        offset += 100
    print('\nКоличество скачанных постов сообщества ' + str(len(posts_list)))
    return posts_list


# Заполняем бд полученной информацией.
def filling_bd(posts_list):
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    for i in posts_list:
        post_id = i['id']
        if "signer_id" in i.keys():
            signer_id = i["signer_id"]
        else:
            signer_id = None
        with open(str(OWNER_ID)[1:] + '\\json\\{}.json'.format(str(post_id)), 'w', encoding='utf-8') as f:
            json.dump(i, f, ensure_ascii=False, indent=4)
        c.execute('''INSERT OR IGNORE INTO posts(post_id, 
        from_id, 
        signer_id, 
        post_text, 
        text_len, 
        comments_num,
        attachments)
        VALUES (?, ?, ?, ?, ?, ?, ?)''', [post_id,
                                          i["from_id"],
                                          signer_id,
                                          i["text"],
                                          count_len_posts(i),
                                          i["comments"]["count"],
                                          take_attachments_for_bd(i)])
    conn.commit()


# Не уверена, что нужно, но мне кажется, приложения к посту/комментарию тоже могут быть полезны. Поэтому собираем.
# (Здравствуйте, я хомяк. Приятно познакомиться xD )
def take_attachments_for_bd(post):
    if "attachments" in post.keys():
        attachments = post["attachments"]
        photos = []
        audios = []
        docs = []
        videos = []
        links = []
        for i in attachments:
            if i["type"] == "photo":
                photos.append(i["photo"]["id"])
            elif i["type"] == "doc":
                docs.append(i["doc"]["title"])
            elif i["type"] == "video":
                videos.append(i["video"]["title"])
            elif i["type"] == "audio":
                audios.append([i["audio"]["artist"], i["audio"]["title"]])
            elif i["type"] == "link":
                links.append([i["link"]["url"], i["link"]["title"]])
        return json.dumps({"photos": photos, "docs": docs, "audios": audios, "videos": videos, "links": links},
                          ensure_ascii=False)
    else:
        return None


# Собираем комменты.
def take_comments(post_list):
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    # можно было бы конечно воспользоваться и сэтами, и еще чем-нибудь... но все равно пришлось бы добавлять либо новую
    # переменную, либо больше циклов. Так что, И ТАК СОЙДЕТ
    ids_posts1 = [post_list[i]['id'] for i in range(len(post_list)) if int(post_list[i]['comments']['count']) <= 100]
    ids_posts2 = [post_list[i]['id'] for i in range(len(post_list)) if int(post_list[i]['comments']['count']) > 100]
    # сначала обработаем все записи с количеством комментов меньше 100
    # execute может захапать за раз только 25 записей. Наша задача его не перекормить
    post_list_by_25 = [ids_posts1[i:i + 25] for i in iter(range(0, len(ids_posts1), 25))]
    m = 0
    for i in post_list_by_25:
        m += 1
        print(m)
        # тут мне очень захотелось воспользоваться execute, да
        code = 'return ['
        for post_id in i:
            code = code + '{"post_id": ' + str(post_id) + ', "comments": API.wall.getComments({\"owner_id\": ' \
                   + str(OWNER_ID) + ', \"post_id\":' + str(post_id) + '})},'
        code = code + '];'
        res = api.execute(code=code)
        for l in res:
            post_id = l['post_id']
            with open(str(OWNER_ID)[1:] + '\\json\\{}_comments.json'.format(str(post_id)), 'w', encoding='utf-8') as f:
                json.dump(l, f, ensure_ascii=False, indent=4)
            av_len = count_average_len_comment(l)
            c.execute('UPDATE posts SET comments_av_len = "{}" WHERE post_id = "{}"'.format(str(av_len), str(post_id)))
            comments = l["comments"]["items"]
            if not comments:
                continue
            else:
                for comment in comments:
                    c.execute('''INSERT OR IGNORE INTO comments(comment_id, 
                                post_id, 
                                from_id, 
                                comment_text, 
                                comment_len, 
                                comment_attachments)
                                VALUES (?, ?, ?, ?, ?, ?)''', [comment["id"],
                                                               post_id,
                                                               comment["from_id"],
                                                               comment["text"],
                                                               count_len(comment["text"]),
                                                               take_attachments_for_bd(comment)])
        sleep(0.5)
    # теперь отдельно обработаем записи, где количество комментов больше 100.
    # наверное, это немного изврат - использовать одновременно и модуль vk, и модуль vk_api.
    # Но большую часть времени мне было норм с vk - писать меньше. А вот тут лень делать цикл,
    # так что добро пожаловать на все готовенькое
    if ids_posts2:
        # так как vk_api я использую ровно один раз за программу, чтобы быстрее запускалось, вставлю импорт сюда -
        # и только если ЕСТЬ записи с более чем сотней комментариев.
        import vk_api
        for i in ids_posts2:
            m += 1
            print(m)
            vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
            tools = vk_api.VkTools(vk_session)
            res = tools.get_all('wall.getComments', 100, {'owner_id': OWNER_ID, 'post_id': i})
            # унифицируем вывод
            res1 = dict()
            res1["post_id"] = i
            res1["comments"] = res
            with open(str(OWNER_ID)[1:] + '\\json\\{}_comments.json'.format(str(i)), 'w', encoding='utf-8') as f:
                json.dump(res1, f, ensure_ascii=False, indent=4)
            comments = res1["comments"]["items"]
            av_len = count_average_len_comment(res1)
            c.execute('UPDATE posts SET comments_av_len = "{}" WHERE post_id = "{}"'.format(str(av_len), str(i)))
            if not comments:
                continue
            else:
                for comment in comments:
                    c.execute('''INSERT OR IGNORE INTO comments(comment_id, 
                                            post_id, 
                                            from_id, 
                                            comment_text, 
                                            comment_len, 
                                            comment_attachments)
                                            VALUES (?, ?, ?, ?, ?, ?)''', [comment["id"],
                                                                           i,
                                                                           comment["from_id"],
                                                                           comment["text"],
                                                                           count_len(comment["text"]),
                                                                           take_attachments_for_bd(comment)])
    conn.commit()
    return


# Считаем длину произвольного текста в словах.
def count_len(text):
    words = text.split()
    return len(words)


# Считаем длину поста.
def count_len_posts(post):
    text = post["text"]
    length = count_len(text)
    return length


# Считаем среднюю длину комментов.
def count_average_len_comment(comments):
    if "items" not in comments["comments"].keys():
        len_average = 0
    else:
        comments_all = comments["comments"]["items"]
        texts = []
        for i in comments_all:
            texts.append(i["text"])
        lens_texts = [count_len(i) for i in texts]
        try:
            len_average = round(sum(lens_texts)/len(lens_texts))
        except ZeroDivisionError:
            len_average = 0
    return len_average


# Берем из бд инфу для построения первого графика.
def make_data():
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    c.execute('SELECT post_id, text_len, comments_av_len FROM posts')
    data1 = c.fetchall()
    return {int(data1[i][0]): [int(data1[i][1]), int(data1[i][2])] for i in range(len(data1))}


# Строим график (эта функция - для первых трех графиков, длина поста от длин комментов, и средние длины от возраста).
def graph(data, name_x="posts", name_y="comments"):
    data_np = np.array([[data[i][0], data[i][1]] for i in data.keys()])
    df = pd.DataFrame(data_np, columns=[name_x, name_y])
    print('Данные для построения графика сформированы...')
    sns.jointplot(x=name_x, y=name_y, kind="reg", color='green', data=df)
    print('Количество точек для графика: ' + str(len(data_np)))
    plt.savefig(name_x+'_'+name_y+'.png', format='png')
    return


# Обрабатываем всех пользователей.
def take_users_ids():
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    # юзеров, писавших комментарии и посты, обрабатываем по отдельности.
    c.execute('SELECT from_id, signer_id FROM posts')
    users_posts1 = c.fetchall()
    users1 = [i[0] for i in users_posts1 if str(i[0]).startswith('-') is False]
    users1.extend([i[1] for i in users_posts1 if str(i[1]).startswith('-') is False])
    users_posts = []
    for user in users1:
        if user is not None and user not in users_posts:
            users_posts.append(user)
    c.execute('SELECT from_id FROM comments')
    users_comments1 = c.fetchall()
    users1 = [i[0] for i in users_comments1 if str(i[0]).startswith('-') is False]
    users_comments = []
    for user in users1:
        if user not in users_comments:
            users_comments.append(user)
    return [users_posts, users_comments]


# Скачиваем инфу про пользователей.
def inf_of_users(list_of_users):
    users_by_1000 = [list_of_users[i:i + 1000] for i in iter(range(0, len(list_of_users), 1000))]
    users = []
    for pack in users_by_1000:
        users1 = api.users.get(user_ids=pack, fields='bdate,city')
        users.extend(users1)
        sleep(0.6)
    check_ids = [users[i]['id'] for i in range(len(users))]
    # почему-то часть пользователей не отдает свои данные с первого раза, а со второго - очень даже
    not_taken = list((set(list_of_users) ^ set(check_ids)))
    i = 0
    while not_taken:
        users.extend(api.users.get(user_ids=not_taken, fields='bdate,city'))
        not_taken = list((set(list_of_users) ^ set([users[i]['id'] for i in range(len(users))])))
        if i > 10:
            # скорее всего, у меня подыхал инет, но десяток пользователей из 15 000 не скачались даже с десятого раза.
            # ну их в болото
            print('Пользователи ' + str(not_taken) + ' не скачаны, потому что жадины.')
            break
        sleep(0.6)
        i += 1
    return users


# Заполняем бд с пользователями.
def update_bd_users(users: list):
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    for i in users:
        user_id = i["id"]
        if "city" in i.keys():
            if "id" in i["city"].keys():
                city_id = i["city"]["id"]
            else:
                city_id = 0
            if "title" in i["city"].keys():
                city_title = i["city"]["title"]
            else:
                city_title = 'город неизвестен'
        else:
            city_id = 0
            city_title = 'город неизвестен'
        if "bdate" in i.keys():
            bdate = i["bdate"]
        else:
            bdate = 'дата рождения неизвестна'
        c.execute('''INSERT OR IGNORE INTO users(user_id,
        city_id,
        city_title,
        bdate) VALUES (?, ?, ?, ?)''', [user_id, city_id, city_title, bdate])
    conn.commit()
    return


# Считаем возраст.
def count_age():
    import datetime
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    c.execute('SELECT user_id, bdate FROM users')
    dates = c.fetchall()
    now = datetime.datetime.now()
    current_day = now.day
    current_month = now.month
    current_year = now.year
    for i in dates:
        if i[1] == 'дата рождения неизвестна' or len(i[1].split('.')) == 2:
            age = 0
        else:
            date = i[1].split('.')
            day_b = int(date[0])
            month_b = int(date[1])
            year_b = int(date[2])
            if current_month < month_b:
                age = current_year - year_b - 1
            elif current_month == month_b and current_day < day_b:
                age = current_year - year_b - 1
            else:
                age = current_year - year_b
        c.execute('UPDATE users SET age="{}" WHERE user_id="{}"'.format(str(age), str(i[0])))
    conn.commit()


# Заполняем таблицы по городам и возростам; дефолтно - по городам, в main вызывается с аргументами
# для заполнения возрастов.
def cities_and_ages_av(age_or_city='city_title', table_name='cities'):
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    c.execute('SELECT user_id, {} FROM users'.format(age_or_city))
    users_ages = c.fetchall()
    ages_dict = {users_ages[i][1]: [] for i in range(len(users_ages))}
    for i in users_ages:
        ages_dict[i[1]].append(i[0])
    c.execute('SELECT from_id, comment_len FROM comments')
    users_comments = c.fetchall()
    for key in ages_dict.keys():
        lens = []
        num_users = len(ages_dict[key])
        for i in ages_dict[key]:
            for n in users_comments:
                if n[0] == i:
                    lens.append(n[1])
        try:
            av_comment = round(sum(lens) / len(lens))
        except ZeroDivisionError:
            av_comment = 0
        num_comment = len(lens)
        c.execute('''INSERT OR IGNORE INTO {}({},
            num_users,
            num_comments,
            av_comment) VALUES ("{}", {}, {}, {})'''.format(table_name,
                                                            age_or_city,
                                                            str(key),
                                                            str(num_users),
                                                            str(num_comment),
                                                            str(av_comment)))
    c.execute('SELECT from_id, signer_id, text_len FROM posts')
    users_posts = c.fetchall()
    for key in ages_dict.keys():
        lens = []
        for i in ages_dict[key]:
            for n in users_posts:
                if n[0] == i or n[1] == i:
                    lens.append(n[2])
        try:
            av_post = round(sum(lens) / len(lens))
        except ZeroDivisionError:
            av_post = 0
        num_posts = len(lens)
        c.execute('''UPDATE {} SET num_posts = {}, av_post = {} WHERE {} = "{}"'''.format(table_name,
                                                                                          num_posts,
                                                                                          av_post,
                                                                                          age_or_city,
                                                                                          key))
    conn.commit()
    return ages_dict


# Создаем данные для графиков по возрасту и по городу; дефолтные переменные для функции - возраст, для
# создания инфу по городам им присваиваются другие значения в теле main.
def make_data_age_or_city(col='age', table='ages'):
    conn = sqlite3.connect(os.path.join('.', NAME_OF_DB))
    c = conn.cursor()
    c.execute('SELECT {}, av_comment, av_post FROM {}'.format(col, table))
    data_first = c.fetchall()
    data_first = [list(data_first[i]) for i in range(len(data_first))]
    data_1 = {i: [data_first[i][0], int(data_first[i][1])] for i in range(len(data_first))}
    data_2 = {i: [data_first[i][0], int(data_first[i][2])] for i in range(len(data_first))}
    not_true1 = []
    not_true2 = []
    for i in data_1.keys():
        if data_1[i][1] == 0:
            not_true1.append(i)
        if data_2[i][1] == 0:
            not_true2.append(i)
    for i in not_true1:
        data_1.pop(i)
    for i in not_true2:
        data_2.pop(i)
    return [data_1, data_2]


# для городов придется построить отдельный график, так как разброс индексов слишком большой, jointplot очень
# плохо отображает данные.
def graph_cities(i, y_ax='av_com'):
    ys = [i[n][1] for n in i.keys()]
    xs = [i[n][0] for n in i.keys()]
    df = pd.DataFrame(dict(x=xs, y=ys))
    print('Данные для построения графика сформированы...')
    ax = sns.factorplot("x", "y", data=df, kind="bar", palette="Greens", size=6, aspect=2, legend_out=False)
    ax.set_axis_labels("city", y_ax)
    ax.set_xticklabels(rotation=90)
    plt.savefig('city_'+y_ax+'.png', format='png')
    return


# Вызываем все, что надо.
def main():
    make_folder(str(OWNER_ID)[1:])
    make_folder(str(OWNER_ID)[1:] + '\\json')
    making_bd()
    print('Необходимые для результатов директории созданы или уже существуют...')
    posts = take_posts()
    filling_bd(posts)
    print('Скачивание постов завершено. Проверьте директорию {}\\json...\nБаза данных создана...'.format(str(OWNER_ID)[1:]))
    take_comments(posts)
    print('Скачивание комментариев завершено. Проверьте директорию {}\\json...'.format(str(OWNER_ID)[1:]))
    print('Выполнено.')
    for i in take_users_ids():
        users = inf_of_users(i)
        update_bd_users(users)
    print('Пользователи, оставлявшие комментарии или писавшие посты, собраны')
    count_age()
    print('Возраста пользователей подсчитаны.')
    cities_and_ages_av(age_or_city='age', table_name='ages')
    print('Средние длины по возрастам подсчитаны и внесены в таблицу.')
    cities_and_ages_av()
    print('Средние длины по городам подсчитаны и внесены в таблицу.')
    graph(make_data())
    i = make_data_age_or_city()
    print('График зависимости длины комментария от длины поста готов.')
    graph(i[0], name_x="age", name_y="av_comment")
    print('График зависимости длины комментария от возраста готов.')
    graph(i[1], name_x="age", name_y="av_post")
    print('График зависимости длины поста от возраста готов.')
    i = make_data_age_or_city(col='city_title', table='cities')
    # # не удивляйтесь, пожалуйста, возрастам вроде 150 - некоторые люди очень любят прикалываться.
    graph_cities(i[0])
    print('Количество точек для графика: ' + str(len(i[0])))
    print('Столбчатая диаграмма длины комментария от города готова.')
    graph_cities(i[1], y_ax='av_post')
    print('Количество точек для графика: ' + str(len(i[1])))
    print('Столбчатая диаграмма длины поста от города готова.')
    plt.show()


main()
