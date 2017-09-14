with open('Austen_Jane_Pride_and_Prejudice.txt', 'r', encoding = 'utf-8') as f:
    text = f.readlines()
    list_ = []
    for line in text:
        line = line.split()
        list_.extend(line)
print (list_)
