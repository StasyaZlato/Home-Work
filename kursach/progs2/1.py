import re


def find_poems():
    with open('1.html', 'r', encoding='utf-8') as f:
        html_text = f.read()
    regex1 = re.compile('<h3.*?><a href=\'(.*?)\'>(.*?)</a></h3>', re.DOTALL)
    regex2 = re.compile('<a class=\'blog-pager-older-link\' href=\'(.*?)\'.*?>Older Posts</a>', re.DOTALL)
    poems = {}
    list_buf = re.findall(regex1, html_text)
    print(list_buf)
    for i in list_buf:
        ref = re.search(regex1, i).group(1)
        name = re.search(regex1, i).group(2)
        poems[name] = ref
    return poems

print(find_poems())