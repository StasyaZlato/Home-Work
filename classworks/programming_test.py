#Задание1. Открыть файл и вывести на экран строчки, содержащие союз

with open ('freq.txt', 'r', encoding = 'utf-8') as f:
    lines = f.readlines ()
    for line in lines:
        if 'союз' in line:
            print (line)


#Задание2. Распечатать через запятую все существительные женского рода
#единственного числа и вывести сумму ipm

with open ('freq.txt', 'r', encoding = 'utf-8') as f:
    lines = f.readlines ()
    a = []
    for line in lines:
        line = line.split ()
        if 'жен' in line and 'ед' in line:
            print (line[0], end = ', ')
            a.append (line[-1])
    ipm_sum = 0
    for elem in a:
        elem = float (elem)
        ipm_sum += elem
    print (ipm_sum)


#Задание3. Спрашиваем слова, пока пользователь не введет пустое слово.
#Выводим для каждого морф. информацию и ipm

with open ('freq.txt', 'r', encoding = 'utf-8') as f:
    lines = f.readlines ()
    word = input ()
    while word:
        for line in lines:
            line = line.split()
            if word in line:
                print ('Морфологическая информация: ' + ' '.join (line[2:-2]))
                print ('IPM = ' + line[-1])
        word = input ()

        
        
            
            
            
            
            
