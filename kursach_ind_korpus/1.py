import re
import os


def dic_indonesian():
    dic = {}
    files_list = os.listdir(r'C:\Users\User\Documents\progs2\teks')
    others = []
    for file in files_list:
        with open(os.path.join(r'C:\Users\User\Documents\progs2\teks', file), 'r', encoding='utf-8') as f:
            words = f.readlines()
            for word in words:
                try:
                    li = word.split('\t')[0:2]
                    dic[li[0]] = li[1]
                except IndexError:
                    others.append(word)
                    continue
    return dic


def parse_with_partsofspeech(text):
    lines1 = text.split('\n')
    lines = [line + ' ' for line in lines1]
    regex = re.compile('(\w+-?\w*)\W')
    dict = dic_indonesian()
    text_new = []
    for line in lines:
        dict_words = {}
        line_new = line.lower()
        words1 = re.findall(regex, line_new)
        words = []
        for word1 in words1:
            if word1 not in words:
                words.append(word1)
        for word in words:
            if word in dict.keys():
                part_of_speech = dict[word]
            elif word not in dict.keys() and (word.endswith('ku') or word.endswith('mu')):
                word0 = word[:-2]
                try:
                    part_of_speech = dict[word0]
                except KeyError:
                    part_of_speech = '?'
            elif word not in dict.keys() and word.endswith('nya'):
                word0 = word[:-3]
                try:
                    part_of_speech = dict[word0]
                except KeyError:
                    part_of_speech = '?'
            else:
                part_of_speech = '?'
            line = re.sub(word, word + '{' + part_of_speech + '} |', line)
            line = re.sub(word.title(), word.title() + '{' + part_of_speech + '} |', line)

        # print(dict_words)
        text_new.append(line)
    print('\n'.join(text_new))


poem = '''Ibuku dehulu marah padaku
diam ia tiada berkata
akupun lalu merajuk pilu
tiada peduli apa terjadi

matanya terus mengawas daku
walaupun bibirnya tiada bergerak
mukanya masam menahan sedan
hatinya pedih kerana lakuku

Terus aku berkesal hati
menurutkan setan, mengkacau-balau
jurang celaka terpandang di muka
kusongsong juga - biar chedera

Bangkit ibu dipegangnya aku
dirangkumnya segera dikucupnya serta
dahiku berapi pancaran neraka
sejuk sentosa turun ke kalbu

Demikian engkau;
ibu, bapa, kekasih pula
berpadu satu dalam dirimu
mengawas daku dalam dunia.
'''
parse_with_partsofspeech(poem)