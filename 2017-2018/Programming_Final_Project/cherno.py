import sqlite3
import csv
import shutil
import pandas


conn = sqlite3.connect('colour_questionary.sqlite')
c = conn.cursor()


with open('bd.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='&')
    first_row = ['id_user', 'lang']
    add_list = [i for i in range(0, 84)]
    first_row.extend(add_list)
    print(first_row)
    writer.writerow(first_row)
    for row in c.execute('SELECT * FROM answers'):
        writer.writerow(row)

# shutil.copy('colour_questionary.sqlite', 'test_bd.sqlite')


df = pandas.read_csv('bd.csv', delimiter='&')
df.to_sql('answers_new', conn, if_exists='append', index=False)
