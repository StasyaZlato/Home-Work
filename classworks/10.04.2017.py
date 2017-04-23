#Зачем? кодировки и пути: windows:   C:\\Users\\Student\\downloads, Linux, Mac:     /home/student/downloads
# Текущая папка - в кот лежит программа

print (os.path.abspath('.')) # получить абсолютный путь к текущей папке, '.' - текущая папка

print (os.getcwd()) # то же самое

os.path.join('texts', '1.txt') # --> f = 'texts\\1.txt'

# ' '.join(['hello', 'world']) --> hello world

os.path.exists('texts')  # --> существует ли в папке файл?

print (os.listdir('.')) # --> что лежит в текущей папке?

#os.listdir('texts') # --> '1.txt', '2.txt', ...
s = 'hello'
i = 1
texts = [f for f in os.listdir('.') if f.endswith('.txt')]
print (texts)
for f in os.listdir('.'):
    if f.endswith('.txt'):
        with open(f, 'a', encoding = 'utf-8') as w:
            w.write (s*i)
            i += 1

os.mkdir('corpus1') # --> создать папку
os.makedirs('a\\b\\long\\long') # --> создает вложенные папки
os.rename('texts\\1.txt', 'texts\\2.txt') # --> переименовывает

os.path.isfile(r'texts\corpus1.txt') # --> является ли файлом?
os.path.isdir(r'texts') # --> является ли папкой?

shutil.copy(r'texts\2.txt', r'new_corpus\2.txt')
shutil.move('откуда', 'куда')
shutil.copytree('папка', 'папка2') # --> копирует ВСЕ

os.remove(r'new_corpus\2.txt')
shutil.rmtree('corpus')
