name = input ('Введите ваше имя: ')
age = input ('Сколько вам лет? ')
colour = input ('Какой ваш любимый цвет? ')
music = input ('Кто ваш любимый музыкальный исполнитель? ')
dream = input ('Какова ваша заветная мечта? ')

with open ('information.txt', 'w', encoding = 'utf-8') as f:
    f.write ('Информация о соседе\n')
    f.write (name + '\n' + age + '\n' + colour + '\n' + music + '\n' + dream)
    
