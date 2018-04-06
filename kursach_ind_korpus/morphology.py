import re
import sqlite3


def prefix_meN(word):
    if word.startswith('me'):
        root_var1 = word[2:]
        if root_var1[0:2] == 'mb':
            root_pref = root_var1[1:]
        elif root_var1[0:2] == 'nd':
            root_pref = root_var1[1:]
        elif root_var1[0:2] == 'ng':
            if root_var1[2] == 'g' or root_var1[2] == 'h':
                root_pref = root_var1[2:]
            else:
                root_pref = [root_var1[2:], 'k' + root_var1[2:]]
        elif root_var1[0] == 'l' or root_var1[0] == 'r':
            root_pref = root_var1
        elif root_var1[0] == 'n':
            if root_var1[1] == 'y':
                root_pref = 's' + root_var1[2:]
            else:
                root_pref = [root_var1, 't' + root_var1[1:]]
        else:
            root_pref = [root_var1, 'p' + root_var1[1:]]
        return ['me', root_pref]
    else:
        root_pref = word
        return root_pref


def suffix_kan(root):
    if type(root) == str:
        if root.endswith('kan'):
            root_2 = root[:-3]
            return [root_2, 'kan']
        else:
            return root
    else:
        pref = root[0]
        root_1 = root[1]
        if type(root_1) == str:
            if root_1.endswith('kan'):
                root_2 = root_1[:-3]
                return [pref, root_2, 'kan']
            else:
                return [pref, root_1]
        else:
            root_2 = []
            for i in range(len(root_1)):
                if root_1[i].endswith('kan'):
                    root_2.append(root_1[i][:-3])
                    suf = 'kan'
                else:
                    root_2.append(root_1[i])
                    suf = ''
            if suf != '':
                return [pref, root_2, suf]
            else:
                return [pref, root_2]


print(suffix_kan(prefix_meN('gunakan')))



# di-, ke-, se-, per-, peN-, memper-
# -nya, -ku, -mu, -i, -wati, -an
def prefix_ter(word):
    if word.startswith('ter'):
        root = word[3:]
        return ['ter', root]
    else:
        return ['', word]

print(prefix_ter('terbesar'))


def prefix_ber(word):
    if word.startswith('ber'):
        root = word[3:]
        return ['ber', word]
    else:
        return ['', word]


def passive(word):
    if word.startswith('ku') or word.startswith('di'):
        root = word[2:]
        return ['ku', root]
    else:
        return ['', word]


def prefix_ke():
