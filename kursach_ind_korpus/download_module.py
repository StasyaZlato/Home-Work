import urllib.request
import re


def download(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl) # берем страницу
        html = page.read().decode('utf-8') # достаем html
        print('Страница {} скачана.'.format(pageUrl))
        return html
    except:
        print('Error at ', pageUrl)
        return None


def del_html(html_text):
    import html
    html_text = html.unescape(html_text)
    return html_text

def clean_html(html_text):
    regex_script = re.compile('<script.*?>.*?</script>', re.DOTALL)
    html_text = re.sub(regex_script, '', html_text)
    regex_style = re.compile('<style.*?>.*?</style>', re.DOTALL)
    html_text = re.sub(regex_style, '', html_text)
    regex_head = re.compile('<head>.*?</head>', re.DOTALL)
    html_text = re.sub(regex_head, '', html_text)
    regex_p = re.compile('</?p.*?>', re.DOTALL)
    html_text = re.sub(regex_p, '\n', html_text)
    html_text = re.sub('</?br( /)?>\n*', '\n', html_text)
    regex_tags_all = re.compile('<.*?>', re.DOTALL)
    html_text_wt = re.sub(regex_tags_all, '', html_text)
    html_text_wt = re.sub('\r', '', html_text_wt)
    html_text_clean = re.sub('\s{2,}', '\n', html_text_wt)
    html_text_clean = re.sub('\n+', '\n', html_text_clean)
    print(html_text_clean.split('\n'))

    # a = html_text_wt.split('\n')
    # html_text_list = []
    # for i in range(len(a)):
    #     if a[i] != '':
    #         html_text_list.append(a[i])
    # print(html_text_list)
    # html_text_clean = '\n'.join(html_text_list)
    return html_text_clean

# def gusmus_poems(html_text):
#     regex =
#     return poems


if __name__ == "__main__":
    print('sth')

