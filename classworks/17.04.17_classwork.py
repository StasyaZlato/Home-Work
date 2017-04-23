import os

def drawtree():
    for root, dirs, files in os.walk('C:\\Users\\1\\Documents\\ниу вшэ'):
        num = root.count('\\')
        new_root = root.split('\\')[-1]
        print('\t'*num+'--'+new_root+'\n')
        for f in files:
            print((num+1)*'\t'+f)
drawtree()
