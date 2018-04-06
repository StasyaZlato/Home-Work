import lxml.etree as tree_it
import re
import os


text_try = '''Barat dan Timur adalah guruku Muslim, Hindu, Kristen, Buddha,
Pengikut Zen dan Tao
Semua adalah guruku
Kupelajari dari semua orang saleh dan pemberani
Rahasia cinta, rahasia bara menjadi api menyala
Dan tikar sembahyang sebagai pelana menuju arasy-Nya
Ya, semua adalah guruku
Ibrahim, Musa, Daud, Lao Tze Buddha, Zarathustra,
Socrates, Isa Almasih Serta Muhammad Rasulullah
Tapi hanya di masjid aku berkhidmat
Walau jejak-Nya
Kujumpai di mana-mana.'''


regex_word = re.compile('([a-zA-Z-]+)')
text_1 = re.split(regex_word, text_try)

print(text_1)

# text_try_xml = []
# for i in range(len(text_1)):
#     if re.search('\w', text_1[i]) is not None:
#         new = '<w>' + text_1[i] + '</w>'
#         text_try_xml.append(new)
#     else:
#         text_try_xml.append(text_1[i])
#     if '\n' in text_1[i]:
#         new = '</se>' + text_1[i]
#         if i + 1 <= len(text_1):
#             text_1[i+1] = '<se>' + text_1[i+1]
# print(''.join(text_try_xml))

# f = r'D:\HSE\linguistics\KILR_and_programming\Yoshkar-Ola\plain\2014\12\i_zhit_stalo_gorazdo_legche.txt'
# f_path_new = r'C:\Users\User\Desktop\1.txt'
# if not os.path.exists(f_path_new): # обрабатываем все файлы mystem, если еще нет
#     mystem_path = os.path.join('D:\HSE\linguistics\KILR_and_programming', 'mystem.exe')
#     os.system(mystem_path + " -cid --format xml " + f + ' ' + f_path_new)
html_1 = tree_it.Element('html')
root = tree_it.SubElement(html_1, 'body')
for i in range(len(text_1)):
    if re.search('\w', text_1[i]) is not None:
        sth = tree_it.SubElement(root, 'w')
        sth.text = text_1[i]
        sth1 = tree_it.SubElement(sth, 'ana', gr='some grammatical features')
        if i + 1 < len(text_1) and re.search('\w', text_1[i+1]) is None:
            sth.tail = text_1[i+1]

a = (tree_it.tostring(html_1, pretty_print=True, xml_declaration=True))

tree =  tree_it.ElementTree(html_1)
tree.write(r"C:\Users\User\Desktop\try.xml")

