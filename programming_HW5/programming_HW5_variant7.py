#какой процент строк содержит больше 5 слов?
with open ('hw5.txt', 'r', encoding = 'utf-8') as f:
    lines = f.readlines ()
    list_1 = []
    for line in lines:
        line = line.split()
        n = len (line)
        list_1.append (n)
    sum_list = 0
    sum_line = 0
    for elem in list_1:
        if elem > 5:
            sum_list += 1
            sum_line += 1
        else:
            sum_list += 1
    percent = (sum_line / sum_list) * 100
    print (percent, '% строк содержит больше 5 слов')
    
