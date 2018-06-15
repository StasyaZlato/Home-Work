import re
from pprint import pprint
import random


def open_f(file):
    with open(file, encoding='utf-8') as f:
        all_quests = f.read()
    # print(len([i for i in all_quests.split('\n') if i != '\n' and i != '' and i != ' ']))
    # всего 84 вопроса
    return all_quests


def managing(text_line):
    list_first = text_line.split('\n\n')
    list_first = [i.split('\n') for i in list_first]
    list_general = [i for i in text_line.split('\n') if i != '\n' and i != '' and i != ' ']
    list_quests = []
    for i in list_first:
        i = [item for item in i if item != '' and item != ' ']
        if len(i) == 1:
            quest = i[0]
            index = list_general.index(quest)
        elif len(i) <= 3:
            quest = random.choice(i)
            index = list_general.index(quest)
        else:
            quest = random.sample(i, 2)
            quest = [(list_general.index(q), q) for q in quest]
        if type(quest) == str:
            list_quests.append((index, quest))
        else:
            list_quests.extend(quest)
    return list_quests


def dicts(file):
    list_q = managing(open_f(file))
    # [{'quest': i.split('\t')[0], 'comment': i.split('\t')[1]} for i in list_quests if '\t' in i else {'quest': i, 'comment': ''}]
    final_list = []
    for item in list_q:
        index = item[0]
        i = item[1]
        if '\t' in i:
            final_list.append({'index': index, 'quest': i.split('\t')[0], 'comment': i.split('\t')[1]})
        else:
            final_list.append({'index': index, 'quest': i, 'comment': ''})
    # print(len(final_list))
    # на выход - 43 случайно подобранных вопросов
    return final_list




if __name__=='__main__':
    pprint(dicts())