# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 10:47:56 2022

@author: AleynaEr
"""
#%% read files
with open("isimler_2022_mart.txt",encoding="utf8") as f:
    nouns = f.readlines()

with open("fiiller_2022_mart.txt") as f:
    verbs = f.readlines()
#%% import libs for turkish spell correction
import turkishnlp
from turkishnlp import detector
obj = detector.TurkishNLP()
obj.download()
obj.create_word_set()
#%% spell correction func
def autoCorrect(text):
    text = obj.list_words(text)
    corrected_text = obj.auto_correct(text)
    corrected_text = " ".join(corrected_text)
    return corrected_text
#%% text cleaning func
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
            text = text.lower()
            
    #text = obj.auto_correct(text)
    return text
#%% creating noun df

for i in range(len(nouns)):
    sample = nouns[i]
    nouns[i] = cleanText(sample)

import pandas as pd

df_noun = pd.DataFrame(nouns, columns = ["kelime"])
df_noun[['kelime', 'ilişki_türü','ilişki_değeri']] = df_noun["kelime"].str.split(',',3,expand=True)
df_noun.sort_values(by = ["kelime"], ascending = True, inplace = True, ignore_index = True)
print(df_noun["ilişki_türü"].unique())
#%% creating verb df

for i in range(len(verbs)):
    sample = verbs[i]
    verbs[i] = cleanText(sample)

df_verbs = pd.DataFrame(verbs, columns = ["kelime"])
df_verbs[['kelime', 'ilişki_türü','ilişki_değeri']] = df_verbs["kelime"].str.split(',',3,expand=True)
print(df_noun.tail()) # her sütunda bozukluk var, spell checker uygula
df_verbs.sort_values(by = ["kelime"], ascending = True, inplace = True, ignore_index = True)
print(df_verbs["ilişki_türü"].unique())

#%% concat noun and verb data
df_words = pd.concat([df_noun,df_verbs], axis = 0)
#%% relation types
print(df_words["ilişki_türü"].unique()) # veri kaybı olacak, yazım yanlışları çok sıkıntı
#%% auto correct the annotators data 

for word in range(len(df_words)):
    relation_value = df_words["ilişki_değeri"].values[word]
    #relation_type = df_words["ilişki_türü"].values[word]
    #print(relation_value)
    corrected = autoCorrect(relation_value)
    #corrected2 = autoCorrect(relation_type)
    #print(corrected2)
    df_words["ilişki_değeri"].values[word] = corrected
    
#%% data singularity

#data = df_words.drop_duplicates(subset=["kelime","ilişki_türü","ilişki_değeri"], inplace=True)
data = pd.DataFrame(df_words.groupby(["kelime","ilişki_türü"])["ilişki_değeri"].agg(list))
#%% turn index into columns after agg
data = data.reset_index(level=1)
data = data.reset_index(level=0)
#%% all columns

all_cols = ['neyi kimi yapılır',
 'ağırlık gr kg',
 'nerede yapılır',
 'ne işe yarar',
 'sıfatları',
 'nasıl yapılır',
 'niçin yapılır',
 'yapınca ne olur',
 'kim ne ile yapılır',
 'rengi',
 'hammaddesi nedir',
 'canlı cansız',
 'ne olunca yapılır',
 'kim ne yapar',
 'fiziksel zihinsel',
 'kim kullanır',
 'hacmi cm3 m3',
 'üst kavramı nedir',
 'içinde neler bulunur',
 'neye kime yapılır',
 'şekli nasıl',
 'tanımı nedir',
 'yanında neler bulunur',
 'nerede bulunur']


#%% necessary columns for hot&cold game

cols = ['kelime','tanımı nedir','ne işe yarar','nasıl yapılır','nerede bulunur','niçin yapılır',
        'yanında neler bulunur','ne olunca yapılır','içinde neler bulunur','yapınca ne olur',
        'hammaddesi nedir','neyi kimi yapılır','üst kavramı nedir','kim ne ile yapılır',
        'kim kullanır','neye kime yapılır','sıfatları','nerede yapılır','rengi',
        'kim ne yapar','şekli nasıl','fiziksel zihinsel','canlı cansız']
#%% concat cols and data

final_data = pd.DataFrame(columns=all_cols)
final_data = pd.concat([data,final_data], axis = 1)
#%%
#final_data.sort_values(by = ["kelime", "ilişki_türü"], ascending = [True,True], inplace = True, ignore_index = True)
#%% correcting typos for relation types
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

for record in range(len(data)):
    relation = data["ilişki_türü"].values[record]
    relation = str.lower(relation)
    if(relation not in all_cols):
        max_sim = 0
        for r in all_cols:
            ratio = similar(relation,r)
            #print(ratio,r,relation)
            if(ratio > max_sim):
                max_sim = ratio
                true_rel = r
                
        print(true_rel, "düzeltilen : ", relation, max_sim)
        final_data["ilişki_türü"].values[record] = r
    else:
        final_data["ilişki_türü"].values[record] = relation
            
#%%
print(final_data["ilişki_türü"].unique())
print(final_data["ilişki_türü"].nunique())
#%% relation type infos to relation columns

for i in range(len(final_data)): # satırlar arası dolaşır, başlangıç kelimesi seçer
    #values = []
    values = set()
    word = final_data["kelime"].values[i]
    relation_type = final_data["ilişki_türü"].values[i]
    relation_value = final_data["ilişki_değeri"].values[i]
    for v in relation_value:
        #values.append(v)
        values.add(v)
    for j in range(len(final_data)): # karşılaştırılacak kayıtları gezer
        if(j>i): # kendinden sonra gelen kayıtlara bakar
            word2 = final_data["kelime"].values[j]
            relation_type2 = final_data["ilişki_türü"].values[j]
            if(word == word2 and relation_type == relation_type2):
                relation_value2 = final_data["ilişki_değeri"].values[j]
                for v2 in relation_value:
                    #values.append(v2)
                    values.add(v2)
                    #print("*****",values)
    print(word,relation_type, "",values)
    final_data[relation_type].values[i] = list(values)
            

#%%

#%% creating data for game (only necessary columns & order of cols is important)

df = pd.DataFrame(data=final_data, columns = cols)
    
#%% creating data singularity
df = df.groupby(["kelime"]).first() # data for use in game
    
#%% save the general data 

"""final_data.to_csv("wordnRelations.csv", index = False)
final_data.to_excel("wordnRelations.xlsx", index = False)"""
#%% save the data (for game)
"""df.to_csv("hotncold_data.csv", index = False)
df.to_excel("hotncold_data.xlsx", index = False)"""