import random

# random.choice(arr) ---> случайный элемент массива
# random.shuffle(arr) ---> перемешивает массив

with open ('words.txt', 'r', encoding = 'utf-8') as f:
     lines = f.readlines()
     random.shuffle(lines)
     score = 0
     for line in lines:
        line = line.strip ()
        word, hint = line.split(' ', 1)
        response = input ('Какое слово я загадала?\n ' + 'Подсказка: ' + hint + ' ')
        if response == word:
            print ('Правильно, молодец!')
            score += 1
        else:
            print ('А вот и нет, слово было ', word)

with open ('scores.txt', 'w', encoding = 'utf-8') as n:
    percent = score / 5 * 100
    n.write('Вот результат\n')
    n.write(str(percent) + '%')
