import re

string = '''Hi, my dear


I hope you still remember me.






No?.. WHat a pity...
I am Nadin. Remember now?
You killed me 3 years ago.



And now it is time for me to have the revenge.'''


b = string.splitlines()
d = re.split('\n{2,}', string)
### ооо да, детка, я поняла, нахрена нужен re.split



# print(b)
# for i in range(len(b)):
#     try:
#         k = b[i+1]
#     except Exception:
#         k = 'a'
#     if k == '' and b[i] != '':
#         print(b[i])


print(d)