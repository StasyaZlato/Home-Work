import sqlite3


def making_bd():
    conn = sqlite3.connect('colour_questionary.sqlite')
    c = conn.cursor()
    command = 'CREATE TABLE IF NOT EXISTS answers(ID_user INTEGER UNIQUE, lang VARCHAR, '
    for i in range(0, 84):
        if i != 83:
            command += '"' + str(i) + '"' + ' VARCHAR, '
        else:
            command += '"' + str(i) + '"' + ' VARCHAR)'
    print(command)
    c.execute(command)
    return


if __name__ == '__main__':
    making_bd()