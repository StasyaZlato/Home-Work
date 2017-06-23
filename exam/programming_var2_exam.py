#task 1

import os
import re

def list_files(path):
    files_list = []
    for d, dirs, files in os.walk(path):
        for f in files:
            path_f = os.path.join(d, f)
            files_list.append(path_f)
    return files_list

def open_file(f):
    with open(f, 'r', encoding = 'utf-8') as k:
        text = k.readlines()
    return text

def count_sent(path):
    files = list_files(path)
    list_sent = {}
    for f in files:
        b = re.search('(_.*?.xhtml)', f)
        f_name = b.group(1)
        sent = 0
        file_text = open_file(f)
        for line in file_text:
            if re.search('</se>', line) != None:
                sent = sent + 1
        list_sent[f_name] = sent
    return list_sent

def file_format_sent(path):
    sent = count_sent(path)
    with open('task1.txt', 'w', encoding = 'utf-8')as k:
        for key in sent.keys():
            k.write(key + '\t' + str(sent[key]) + '\n')
        

#task 2

def inf(f):
    text = open_file(f)
    inf = {}
    for line in text:
        author = re.search('content="(.*?)" name="author"', line)
        if author != None:
            author1 = author.group(1)
    for line in text:
        topic = re.search('content="(.*?)" name="topic"', line)
        if topic != None:
            topic1 = topic.group(1)
    inf[author1] = topic1
    return inf

def create_csv(path):
    files = list_files(path)
    with open('task2.csv', 'w', encoding = 'utf-8') as k:
        for f in files:
            infa = inf(f)
            f_name = re.search('(_.*?.xhtml)', f).group(1)
            for key in infa.keys():
                k.write(str(f_name) + '\t' + str(key) + '\t' + str(infa[key]) + '\n')


#task 3

def pr_loc(f):
    text = open_file(f)
    bigrams = []
    for i in range(len(text)):
        pr = re.search('gr="PR"', text[i])
        if pr != None:
            prep = re.search('</ana>(.*?)</w>', text[i]).group(1)
            loc = re.search('"S.*?loc', text[i+1])
            if loc != None:
                S_loc = re.search('</ana>(.*?)</w>', text[i+1]).group(1)
                bigrams.append(prep + ' ' + S_loc)
    return bigrams

def text_without_tegs(f):
    text = open_file(f)
    text_w_t = ''
    for line in text:
        if re.search('<w>', line) != None:
            word = re.search('</ana>(.*?)</w>', line).group(1)
            prep = re.search('</w>(.)(</se>)?', line)
            if prep != None:
                if prep.group(1) == '.' or prep.group(1) == '!' or prep.group(1) == '?':
                    text_w_t = text_w_t + ' ' + word + prep.group(1)+'\n'
                else:
                    text_w_t = text_w_t + ' ' + word + prep.group(1)
            else:
                text_w_t = text_w_t + ' ' + word
                
    return text_w_t

#def sent_with_bigr(f):
 #   bigrams = pr_loc(f)
  #  text = text_without_tegs(f)
   # a = text.split('\n')
    #sent = {}
    #for b in bigrams:
     #   for line in text:
      #      if re.search(b, line) != None:
       #         sent[line] = b
    
    #return sent

def bigr(path):
    files = list_files(path)
    with open('task3.txt', 'w', encoding = 'utf-8') as k:
        for f in files:
            for b in pr_loc(f):
                k.write(b + '\n')
                
        
        
    

path = 'C:\\Users\\1\\Documents\\ниу вшэ\\КИЛИ и программирование\\python\\экзамен\\news'
file_format_sent(path)
create_csv(path)
bigr(path)
