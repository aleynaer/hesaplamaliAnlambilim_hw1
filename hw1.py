# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:51:04 2022

@author: AleynaEr
"""


with open("isimler_2022_mart.txt",encoding="utf8") as f:
    nouns = f.readlines()
#%%

with open("fiiller_2022_mart.txt") as f:
    verbs = f.readlines()
#%%
"""
import turkishnlp
from turkishnlp import detector
obj = detector.TurkishNLP()
obj.download()
obj.create_word_set()"""
#%%
def cleanText(text):
    
    import re
    pattern = re.compile("iliski")
    pattern2 = re.compile("\n")
    punc = '''!()-[]{};:""''\<>.@#$%^&*_?''' # ?/
    
    for element in text:
        if element in punc:
            text = text.replace(element,"")
            text = text.replace("�","ğ")
            text = text.replace("/"," ")
            text = re.sub(pattern,'',text)
            text = re.sub(pattern2,'',text)
            text = text.lstrip()
            
    #text = obj.auto_correct(text)
    return text
#%% nouns için metin temizleme

for i in range(len(nouns)):
    sample = nouns[i]
    nouns[i] = cleanText(sample)
#%%
import pandas as pd

df_noun = pd.DataFrame(nouns, columns = ["kelime"])
df_noun[['kelime', 'ilişki_türü','ilişki_değeri']] = df_noun["kelime"].str.split(',',3,expand=True)
print(df_noun["ilişki_türü"].unique())
#%% verbs için metin temizleme

for i in range(len(verbs)):
    sample = verbs[i]
    verbs[i] = cleanText(sample)
#%%
df_verbs = pd.DataFrame(verbs, columns = ["kelime"])
df_verbs[['kelime', 'ilişki_türü','ilişki_değeri']] = df_verbs["kelime"].str.split(',',3,expand=True)
print(df_verbs["ilişki_türü"].unique())
#%%
print(df_noun.tail()) # her sütunda bozukluk var, spell checker uygula
#%%
df_words = pd.concat([df_noun,df_verbs], axis = 0)
#%%
df_words["ilişki_türü"].unique() # veri kaybı olacak, yazım yanlışları çok sıkıntı
#%%
"""import turkishnlp
from turkishnlp import detector
obj = detector.TurkishNLP()
obj.download()
obj.create_word_set()

lwords = obj.list_words("vri kümsi idrae edre ancaka daha güezl oalbilir")
corrected_words = obj.auto_correct(lwords)
corrected_string = " ".join(corrected_words)

x = "ğekli nasğl?"
xl = obj.list_words(x)
correct = obj.auto_correct(xl)
print(correct) """
#%%
noun_excel = pd.read_excel("AleynaEr_isimler.xlsx",nrows = 0)
noun_excel.drop(columns=noun_excel.columns[0], axis=1, inplace = True)
noun_cols = noun_excel.columns

verb_excel = pd.read_excel("AleynaEr_fiiller.xlsx",nrows = 0)
verb_excel.drop(columns=verb_excel.columns[0], axis=1, inplace = True)
verb_cols = verb_excel.columns
#%%
cols = set()

for i in noun_cols:
    cols.add(i)
    
for i in verb_cols:
    cols.add(i)
    
cols = list(cols)
#%%

data = pd.DataFrame(columns=cols)
#%%
data = pd.concat([df_words,data], axis = 1)
#%%
data.to_excel("data.xlsx",index = False)
#%%
data.to_csv("word_data.csv", index = False, encoding="utf8")
#%%

a = pd.read_csv("word_data.csv")