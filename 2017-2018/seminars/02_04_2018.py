import urllib.request as ur
import sys
import json


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
req = ur.Request('https://api.vk.com/method/wall.get?owner_id=265240465&count=10&v=5.73&access_token=8a3d51e08b65e2fa4356fc4dc23b591991af5ce75fbda2ebb34031360a1084300372dbdaea19c43786ace')
response = ur.urlopen(req)
result = response.read().decode('utf-8')
dict_j = result.translate(non_bmp_map)

js = json.loads(dict_j)
# print(json.dumps(js, indent=4))

for i in range(10):
    print('------------ {} ------------'.format(str(i+1)))
    a = js['response']['items'][i]['text']
    if a != '':
        print(a)
    else:
        a = js['response']['items'][i]['copy_history'][0]['text']
        print(a)
