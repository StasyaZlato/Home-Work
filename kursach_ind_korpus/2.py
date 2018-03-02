import re

with open('kbbi_kak_zhe_ia_s_nim_zadolbalas.txt', 'r', encoding='utf-8') as f:
    dictionary_prev = f.readlines()
regex = re.compile(' / (\w{1,4}) /')
dict_plain = {}
dict_transform = {}
for line in dictionary_prev:
    if re.search(regex, line) is not None:
        line = line.strip()
        line = line.replace('\ufeff', '')
        line1 = line.split('/')
        parts_with_om = re.findall(regex, line)
        parts_with_om_copy = []
        for i in parts_with_om:
            if i not in parts_with_om_copy:
                parts_with_om_copy.append(i)
        dict_plain[line1[0].strip()] = parts_with_om_copy
    else:
        if re.search('-->', line) is not None:
            line = line.strip()
            line1 = line.split('-->')
            dict_transform[line1[0]] = line1[1]
print(dict_plain)
# print(dict_transform)

# print(dict_plain['dahulu'])

poem = '''Ibuku, dehulu marah padaku
diam ia tiada berkata
akupun lalu-lalu merajuk pilu
tiada peduli apa terjadi'''

text_for_parse = poem.split('\n')
# text_for_parse = poem.lower().split()
regex = re.compile('(\w+-?\w*)(\W)?')
text_new = []
for line in text_for_parse:
    words = []
    line1 = line.split()
    for word in line1:
        a = re.search(regex, word).group(1)
        b = re.search(regex, word).group(2)
        if a in dict_plain.keys():
            a += str(dict_plain[a.lower()])
        else:
            if a.endswith('ku') or a.endswith('mu'):
                try:
                    a += str(dict_plain[a[:-2].lower()])
                except KeyError:
                    continue
            elif a.endswith('nya') or a.endswith('pun') or a.endswith('lah'):
                try:
                    a += str(dict_plain[a[:-3].lower()])
                except KeyError:
                    continue
            # elif a.endswith('pun') or a.endswith('lah'):
            #     try:
            #
            else:
                a += '[?]'
        if b is not None:
            word1 = a + b
        else:
            word1 = a
        words.append(word1)
    text_new.append(' '.join(words))
print('\n'.join(text_new))


# c = {1: 2, 3: 4, 5: 6}
# c[7] = c.pop(1)
# print(c)