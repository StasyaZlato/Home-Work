#Примеры
#Лунным сияньем                 В глубине в горах
#Залита вишня в горах.          Топчет красный клена лист
#Вижу, под ветром               Стонущий олень.
#Дрожь по деревьям прошла, -    Слышу плач его... Во мне
#Значит, цветы опадут?!         Вся осенняя печаль
import random

def adjective_Abl_m():
    with open('adjective_Abl_verse1_m.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def adjective_Abl_f():
    with open('adjective_Abl_verse1_f.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)


  
def noun_Abl_m():
    with open('noun_Abl_verse1_m.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)


    
def noun_Abl_f(): 
    with open('noun_Abl_verse1_f.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def noun_phrase():
    with open('prepositions.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        prep = random.choice(line)
        while prep != 'в' and prep != 'к' and prep != 'с':
            prep = random.choice(line)
    if prep == 'в' or prep == 'к':
        with open('noun_verse1_prep1.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun1 = random.choice(noun)
    else:
        with open('noun_verse1_prep2.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun1 = random.choice(noun)
    return prep.title() + ' ' + noun1



def noun_Gen(): 
    with open('noun_Gen_verse1.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def verse11():
    return adjective_Abl_m().title() + ' ' + noun_Abl_m()

def verse12():
    return adjective_Abl_f().title() + ' ' + noun_Abl_f()

def verse13():
    return noun_phrase() + ' ' + noun_Gen()



def participle_adj():
    with open('participle_adjective_verse2.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def subject():
    with open('subject_verse2.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def place():
    with open('places_verse2.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(', ')
    return random.choice(line)



def obj_f():
    with open('adjective_obj_verse2_f.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        adj = random.choice(line)
    with open('object_verse2_f.txt', 'r', encoding = 'utf-8') as k:
        objects = k.readlines()
        for obj in objects:
            obj = obj.split()
        obj = random.choice(obj)
    return adj + ' ' + obj



def obj_m():
    with open('object_verse2_m.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        obj1 = random.choice(line)
    with open('object_Gen_verse2_m.txt', 'r', encoding = 'utf-8') as k:
        objects = k.readlines()
        for obj in objects:
            obj = obj.split()
        obj2 = random.choice(obj)
    with open('adjective_obj_verse2_m.txt', 'r', encoding = 'utf-8') as l:
        adjectives = l.readlines()
        for adjective in adjectives:
            adjective = adjective.split()
        adj = random.choice(adjective)
    return adj + ' ' + obj2 + ' ' + obj1


    
def verse21():
    return participle_adj().title() + ' ' + subject() + ' ' + place() + '.'



def verse22():
    with open('verb_verse2.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        verb = random.choice(line)
    return verb.title() + ' ' + obj_f()



def verse23():
    with open('verb_verse2.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        verb = random.choice(line)
    return verb.title() + ' ' + obj_m()



def verb_feel():
    with open('verb_feelings.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def verse31():
    with open('prepositions.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        prep = random.choice(line)
    with open('base_noun_verse3.txt', 'r', encoding = 'utf-8') as k:
        nouns = k.readlines()
        for noun in nouns:
            noun = noun.split()
        base_noun = random.choice(noun)
    if prep == 'под' or prep == 'над':
        if base_noun == 'мор' or base_noun == 'солнц':
            noun = base_noun + 'ем'
        else:
            noun = base_noun + 'ом'
    elif prep == 'у' or prep == 'от' or prep == 'из':
        if base_noun == 'мор':
            noun = base_noun + 'я'
        else:
            noun = base_noun + 'а'
    elif prep == 'при' or prep == 'на':
        noun = base_noun + 'е'
    elif prep == 'с':
        if base_noun == 'мор' or base_noun == 'солнц':
            noun = base_noun + 'ем'
        else:
            noun = base_noun + 'ом'
        prep = 'как с'
    elif prep == 'в':
        noun = base_noun + 'е'
        prep = 'как в'
    elif prep == 'к':
        if base_noun == 'мор':
            noun = base_noun + 'ю'
        else:
            noun = base_noun + 'у'
        prep = 'как к'
    else:
        if base_noun == 'мор':
            noun = base_noun + 'ю'
        else:
            noun = base_noun + 'у'
    return verb_feel().title() + ',' + ' ' + prep + ' ' + noun



def verse32():
    with open('participle_verse3.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        participle = random.choice(line)
    with open('subject_verse3.txt', 'r', encoding = 'utf-8') as k:
        subjects = k.readlines()
        for sub in subjects:
            sub = sub.split()
        subject = random.choice(sub)
    return participle.title() + ' ' + subject + '.'



def verse41():
    with open('noun_verse41_1.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        noun1 = random.choice(line)
    with open('prepositions.txt', 'r', encoding = 'utf-8') as k:
        preps = k.readlines()
        for preposition in preps:
            preposition = preposition.split()
        prep = random.choice(preposition)
        while prep == 'в' or prep == 'к' or prep == 'с':
            prep = random.choice(preposition)
    if prep == 'под' or prep == 'над':
        with open('noun_verse41_2.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'у' or prep == 'от' or prep == 'из':
        with open('noun_verse41_3.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'при':
        with open('noun_verse41_4.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'на':
        with open('noun_verse41_5.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    else:
        with open('noun_verse41_6.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)        
    if noun1 == 'дрожь' or noun1 == 'ночь' or noun1 == 'сталь' or noun1 == 'тень' or noun1 == 'кровь' or noun1 == 'плеть':
        with open('verb_verse41_1.txt', 'r', encoding = 'utf-8') as l:
            verbs = l.readlines()
            for verb in verbs:
                verb = verb.split()
            verb1 = random.choice(verb)
    else:
        with open('verb_verse41_2.txt', 'r', encoding = 'utf-8') as l:
            verbs = l.readlines()
            for verb in verbs:
                verb = verb.split()
            verb1 = random.choice(verb)
    return noun1.title() + ' ' + prep + ' ' + noun2 + ' ' + verb1 + '.'



def noun42():
    with open('object_verse42.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
    return random.choice(line)



def the_end_of_the_line():
    with open('prepositions.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        line.append('во' and 'со' and 'ко')
        line.remove('под')
        line.remove('у')
        line.remove('от')
        line.remove('по')
        line.remove('из')
        prep = random.choice(line)
    if prep == 'во':
        with open('noun_verse42_1.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'со':
        noun = 'мной'
    elif prep == 'ко':
        with open('noun_verse42_2.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'при' or prep == 'на':
        if noun42() == ('плач' or 'крик' or 'стон' or 'зов' or 'стан' or 'взгляд' or 'прах' or 'плен' or 'хлад'):
            with open('noun_verse42_3.txt', 'r', encoding = 'utf-8') as k:
                nouns = k.readlines()
                for noun in nouns:
                    noun = noun.split()
                noun2 = random.choice(noun)
                while noun2 == 'ней':
                    noun2 = random.choice(noun)
        else:
            with open('noun_verse42_3.txt', 'r', encoding = 'utf-8') as k:
                nouns = k.readlines()
                for noun in nouns:
                    noun = noun.split()
                noun2 = random.choice(noun)
                while noun2 == 'нем':
                    noun2 = random.choice(noun)
    elif prep == 'в':
        with open('noun_verse42_4.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'с':
        with open('noun_verse42_5.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    elif prep == 'к':
        with open('noun_verse42_6.txt', 'r', encoding = 'utf-8') as k:
            nouns = k.readlines()
            for noun in nouns:
                noun = noun.split()
            noun2 = random.choice(noun)
    else:
        if noun42() == ('плач' or 'крик' or 'стон' or 'зов' or 'стан' or 'взгляд' or 'прах' or 'плен' or 'хлад'):
            with open('noun_verse42_7.txt', 'r', encoding = 'utf-8') as k:
                nouns = k.readlines()
                for noun in nouns:
                    noun = noun.split()
                noun2 = random.choice(noun)
                while noun2 == 'ней':
                    noun2 = random.choice(noun)
        else:
            with open('noun_verse42_7.txt', 'r', encoding = 'utf-8') as k:
                nouns = k.readlines()
                for noun in nouns:
                    noun = noun.split()
                noun2 = random.choice(noun)
                while noun2 == 'нем':
                    noun2 = random.choice(noun)
    return prep.title() + ' ' + noun2


    
def verse42():
    with open('pronoun_verse4.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        pronoun = random.choice(line)
    return verb_feel().title() + ' ' + noun42() + ' ' + pronoun + '... ' + the_end_of_the_line()



def verse51():
    with open('pronoun_verse5.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        pronoun = random.choice(line)
    if pronoun == 'вся' or pronoun == 'та':
        with open('adjective_verse5_f_4.txt', 'r', encoding = 'utf-8') as k:
            adjectives = k.readlines()
            for adjective in adjectives:
                adjective = adjective.split()
            adj = random.choice(adjective)
        with open('noun_verse5_f.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun1 = random.choice(noun)
    elif pronoun == 'весь' or pronoun == 'тот':
        with open('adjective_verse5_m_3.txt', 'r', encoding = 'utf-8') as k:
            adjectives = k.readlines()
            for adjective in adjectives:
                adjective = adjective.split()
            adj = random.choice(adjective)
        with open('noun_verse5_m.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun1 = random.choice(noun)
    else:
        with open('adjective_verse5_f_3.txt', 'r', encoding = 'utf-8') as k:
            adjectives = k.readlines()
            for adjective in adjectives:
                adjective = adjective.split()
            adj = random.choice(adjective)
        with open('noun_verse5_f.txt', 'r', encoding = 'utf-8') as l:
            nouns = l.readlines()
            for noun in nouns:
                noun = noun.split()
            noun1 = random.choice(noun)
    return pronoun.title() + ' ' + adj + ' ' + noun1 + '.'



def verse52():
    with open('parenthesis_verse5.txt', 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
        parenthesis = random.choice(line)
    with open('noun_verse52.txt', 'r', encoding = 'utf-8') as k:
        nouns = k.readlines()
        for noun in nouns:
            noun = noun.split()
        noun1 = random.choice(noun)
    if noun1 == 'звезда' or noun1 == 'вуаль' or noun1 == 'туман':
        with open('verb_verse52_sg.txt', 'r', encoding = 'utf-8') as l:
            verbs = l.readlines()
            for verb in verbs:
                verb = verb.split()
            verb1 = random.choice(verb)
    else:
        with open('verb_verse52_pl.txt', 'r', encoding = 'utf-8') as l:
            verbs = l.readlines()
            for verb in verbs:
                verb = verb.split()
            verb1 = random.choice(verb)
    return parenthesis.title() + ' ' + noun1 + ' ' + verb1 + '?!'


    
def poem():
    variant = random.choice([1, 2, 3, 4, 5, 6])
    if variant == 1:
        var = random.choice([1, 2])
        if var == 1:
            return verse11() + '\n' + verse21() + '\n' + verse31() + '\n' + verse41() + '\n' + verse52()
        else:
            return verse12() + '\n' + verse21() + '\n' + verse31() + '\n' + verse41() + '\n' + verse52()
    elif variant == 2:
        var = random.choice([1, 2])
        if var == 1:
            return verse13() + '\n' + verse22() + '\n' + verse32() + '\n' + verse42() + '\n' + verse51()
        else:
            return verse13() + '\n' + verse23() + '\n' + verse32() + '\n' + verse42() + '\n' + verse51()
    elif variant == 3:
        var = random.choice([1, 2, 3, 4])
        if var == 1:
            return verse11() + '\n' + verse22() + '\n' + verse32() + '\n' + verse41() + '\n' + verse52()
        elif var == 2:
            return verse12() + '\n' + verse22() + '\n' + verse32() + '\n' + verse41() + '\n' + verse52()
        elif var == 3:
            return verse11() + '\n' + verse23() + '\n' + verse32() + '\n' + verse41() + '\n' + verse52()
        else:
            return verse12() + '\n' + verse23() + '\n' + verse32() + '\n' + verse41() + '\n' + verse52()
    elif variant ==4:
        return verse13() + '\n' + verse21() + '\n' + verse31() + '\n' + verse41() + '\n' + verse52()
    elif variant == 5:
        var = random.choice([1, 2])
        if var == 1:
            return verse13() + '\n' + verse22() + '\n' + verse32() + '\n' + verse41() + '\n' + verse52()
        else:
            return verse13() + '\n' + verse23() + '\n' + verse32() + '\n' + verse41() + '\n' + verse52()
    else:
        var = random.choice([1, 2, 3, 4])
        if var == 1:
            return verse11() + '\n' + verse22() + '\n' + verse32() + '\n' + verse42() + '\n' + verse51()
        elif var == 2:
            return verse12() + '\n' + verse22() + '\n' + verse32() + '\n' + verse42() + '\n' + verse51()
        elif var == 3:
            return verse11() + '\n' + verse23() + '\n' + verse32() + '\n' + verse42() + '\n' + verse51()
        else:
            return verse12() + '\n' + verse23() + '\n' + verse32() + '\n' + verse42() + '\n' + verse51()



print (poem())
