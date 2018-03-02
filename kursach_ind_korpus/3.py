import urllib.request
import re

def download(url):
    # try:
    page = urllib.request.urlopen(url) # берем страницу
    html1 = page.read().decode('utf-8') # достаем html
    import html
    html1 = html.unescape(html1)
    return html1
    # except:
    #     print('Error at ', url)


def dont_need_all_html(url):
    all_rubbish = download(url)
    regex_tag = re.compile('<head>.*?</head>', re.DOTALL)
    all_rubbish = re.sub(regex_tag, '', all_rubbish)
    regex_tag = re.compile('<script.*?>.*?</script>', re.DOTALL)
    all_rubbish = re.sub(regex_tag, '', all_rubbish)
    regex_tag = re.compile('<style.*?>.*?</style>', re.DOTALL)
    all_rubbish = re.sub(regex_tag, '', all_rubbish)
    regex = re.compile('>([^<>]+)<', re.DOTALL) # Это, мать вашу, гениально! Но не нужно...
    without_tags = re.findall(regex, all_rubbish)
    for i in range(len(without_tags)):
        without_tags[i] = without_tags[i].strip()
    without_tags1 = [i for i in without_tags if i != '']
    print('\n'.join(without_tags1))

dont_need_all_html('https://kbbi.web.id/kadang')