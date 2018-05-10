from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem
from random import choice
import re
import json


morph = MorphAnalyzer()


def take_sentence(sentence):
    # sentence = input('Ваше сообщение:\n')
    regex_word = re.compile('(\w+-?\w*)')  # в общем, мне не улыбается стрипить от слова все знаки
    # препинания после деления по пробелам - все равно никогда не выходило перечислить ВСЕ.
    # Поэтому я придумала регулярку для деления текста на слова по наличию буквенных символов и дефиса:)
    # а еще это позволяет сохранить на своих местах все знаки препинания и пробелы.
    words_list = re.split(regex_word, sentence)
    return words_list


def analize_sent(splited_sentence: list):
    for i in range(len(splited_sentence)):
        if re.search('\w', splited_sentence[i]) is not None:
            ana = morph.parse(splited_sentence[i])
            splited_sentence[i] = {splited_sentence[i]: ana[0].tag}
    return splited_sentence


def make_dict_ruscorpora():
    with open('1grams-3.txt', 'r', encoding='utf-8') as f:
        all = f.readlines()
    new_dict = {}
    # try:
    #     with open('dict_forms.txt', 'r', encoding='utf-8') as k:
    #         text = k.read()
    # except FileNotFoundError:
    #     text = ''
    # print(text)
    with open('dict_forms.txt', 'a', encoding='utf-8') as js:
        for i in all:
            # if re.search('\n'+i.split('\t')[1].strip()+'\t', text) is not None or text.startswith(i+'\t'):
            #     print('+', end=' ~ ')
            #     continue
            # else:
                # print(i, end=' ')
            item = i.split('\t')[1].strip()
            ana = morph.parse(item)
            new_dict[item] = ana[0].tag
            js.write(item + '\t' + str(ana[0].tag) + '\n')
    return new_dict


def make_dict_book():
    with open('text_for_dict.txt', 'r', encoding='utf-8') as f:
        all = f.read()
    regex_word = re.compile('(\w+-?\w*)')
    words_list = re.split(regex_word, all)
    just_words = []
    for i in words_list:
        if re.search('\w', i) is not None:
            just_words.append(i.strip())
    new_dict = {}
    with open('dict_forms_text.txt', 'w', encoding='utf-8') as f:
        for item in just_words:
            print(item)
            ana = morph.parse(item)
            new_dict[item] = ana[0].tag
            f.write(item + '\t' + str(ana[0].tag) + '\n')
    return new_dict



def find_same_morph(word_with_morph: dict, new_dict: dict):
    morph_base = list(word_with_morph.values())[0]
    word_base = list(word_with_morph.keys())[0]
    suit = []
    for word, morph_new in new_dict.items():
        if morph_new == str(morph_base):
            suit.append(word)
    return choice(suit)


def morph_in_dict(name):
    # question = input('Работать с файлом НКРЯ или с текстом? Введите 1, если с НКРЯ, и 2, если с текстом.\n')
    # if question == '1':
    #     name = 'dict_forms.txt'
    # else:
    #     name = 'dict_forms_text.txt'
    with open(name, 'r', encoding='utf-8') as f:
        all = f.readlines()
    dict_wf = {}
    for line in all:
        wf_and_m = line.split('\t')
        dict_wf[wf_and_m[0].strip().lower()] = wf_and_m[1].strip()
    return dict_wf


def main(sentence):
    list_of_w = analize_sent(take_sentence(sentence))
    # dict_wf = make_dict_ruscorpora()
    # dict_wf = make_dict_book()
    dict_wf = morph_in_dict('dict_forms_text.txt')
    new_list = []
    for item in list_of_w:
        if type(item) == dict:
            new_word = find_same_morph(item, dict_wf)
            new_list.append(new_word)
        else:
            new_list.append(item)
    return ''.join(new_list)


if __name__ == '__main__':
    sentence = ''
    main(sentence)
