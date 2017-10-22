
# coding: utf-8

# In[518]:


from tkinter import *
import random
#import time


# In[519]:


root = Tk()
root.title('Морфа')

frame1 = Frame(root,width=500,height=300)
frame2 = Frame(root, width=500, height=100)
ent = Text(frame1,font="14",width=20,height=3,wrap=WORD)
txt = Text(frame1,font="14",width=40,height=10,wrap=WORD)
btn1 = Button(frame2,text="Нажми на меня!")
ent1 = Text(root, font="14",width=3, height=1)
#btn2 = Button(frame2,text="Тест")


# In[520]:


def list_of_terms():
    with open(r'термины.txt', 'r', encoding='utf-8') as f:
        terms = f.read()
        list_of_terms = terms.split('\n\n')
        f.close()
    return list_of_terms


# In[521]:


def dict_morph():
    terms = list_of_terms()
    dic = {}
    for term in terms:
        try:
            dic[term.split('-', maxsplit=1)[0]] = term.split('-', maxsplit=1)[1]
        except IndexError:
            print ('Ошибка на термине ', term)
    return dic


# In[ ]:


global lnd
lnd = list_of_terms()

def term(event):   
    print(len(lnd))
    a = random.choice(lnd)
    term1 = a.split('-', maxsplit=1)
    if len(lnd) > 0:
        try:
            ent.delete(1.0,END)
            ent.insert(END,term1[0])
            txt.delete(1.0,END)
            txt.insert(END,term1[1])
            ent1.delete(1.0,END)
            ent1.insert(END, str(len(lnd)))
            lnd.remove(a)
        except:    
            ent.insert(END,term1[0])
            txt.insert(END,term1[1])
            ent1.insert(END,str(len(lnd)))
            lnd.remove(a)
    
        

frame1.pack()
frame2.pack()

ent1.pack()
ent.grid(row=0,column=0,padx=20)
txt.grid(row=0,column=1,padx=20,pady=10)

btn1.pack()
#btn2.grid(row=0,column=1)
btn1.bind("<Button-1>",term)
#btn2.bind("<Button-1>", new_wind)



root.mainloop()



