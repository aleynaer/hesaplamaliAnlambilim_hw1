# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:31:15 2022

@author: Asus
"""

import pandas as pd
from ast import literal_eval

table = pd.read_csv("hotncold_data.csv")

table.fillna("empty", inplace = True)
cols = table.iloc[:,1:].columns

for i in range(len(table)):
    for j in cols:
        cell = table[j].values[i]
        if(cell == "empty"):
            table[j].values[i] = [""]
        else:
            cell = literal_eval(cell)
            table[j].values[i] = cell
#%% pick random word
import random
upper = len(table)
random_num = random.randint(0,upper)
hidden_word = table["kelime"].values[random_num]
#%%
cols = list(table.iloc[:,1:].columns)
penalty = 1
similar_dict = {}
initial = random_num
dict2 = {}
#%%
def searchSimilars(penalty, initial):
    if(penalty < 20):
        for col in cols:
            colnum = cols.index(col) # curr col
            if(colnum % 2 == 1):
                penalty += 1
            sims = table[col].values[initial] # birinci dereceden yakınlar eklenir
            #temp_penalty = penalty
            for element in sims:
                if(element not in similar_dict.keys() and element != ''):
                    #pair = {i:penalty}
                    similar_dict.update({element:penalty})
                    #penalty += 1
                #penalty = temp_penalty 
    return similar_dict
#%% 
#%%
"""
def findSimilarss(penalty,initial):
    if(penalty < 20):
        for col in cols:
            colnum = cols.index(col) # curr col
            if(colnum % 2 == 1):
                penalty += 1
            sims = table[col].values[initial] # birinci dereceden yakınlar eklenir
            temp_penalty = penalty
            for element in sims:
                if(element not in similar_dict.keys() and element != ''):
                    #pair = {i:penalty}
                    similar_dict.update({element:penalty})
                    copy = similar_dict # yeni ekledim
                    for keys in copy.keys(): #similar_dict olacak
                        initial = table[table["kelime"]==keys].index.values # key tabloda kelime olarak var mı
                        if(initial > 0): # varsa
                            penalty = copy.get(keys)
                            penalty += 8
                            initial = initial[0]
                            findSimilars(penalty,initial)
                            #return copy
                            print("girdi ve çağırdı") 
            penalty = temp_penalty
            initial = random_num
    return similar_dict"""
                
#%%
a = searchSimilars(penalty, initial)
#%%
#♠b = findSimilars(penalty,initial)
#%%
def searchOthers(similar_dict,dict2):
    for key in similar_dict.keys():
        initial = table[table["kelime"]==key].index.values # key tabloda kelime olarak var mı
        if(initial > 0): # varsa
           penalty = similar_dict.get(key)
           #print(keys,"",penalty)
           penalty += 5 # başka bir kayda erişmenin cezası +5
           if(penalty < 20):
               initial = initial[0]
               for col in cols:
                   colnum = cols.index(col) # curr col
                   if(colnum % 2 == 1):
                       penalty += 1
                       if(penalty < 20):
                           sims = table[col].values[initial]
                           for element in sims:
                               if(element not in dict2.keys() and element not in dict2.keys() and element != ''):
                                   dict2.update({element:penalty})
    return dict2
#%%
searchSimilars(penalty, initial)                  
#%%
searchOthers(similar_dict,dict2)
#%%
"""
#%%
#elems = []
def findSimilars(penalty,initial):
    if(penalty < 20):
        for col in cols:
            colnum = cols.index(col) # curr col
            if(colnum % 2 == 1):
                penalty += 1
            sims = table[col].values[initial] # birinci dereceden yakınlar eklenir
            #temp_penalty = penalty
            for element in sims:
                if(element not in similar_dict.keys() and element != ''):
                    #pair = {i:penalty}
                    similar_dict.update({element:penalty})
                    
        #copy = similar_dict # yeni ekledim
        for keys in similar_dict.keys(): #similar_dict olacak
            initial = table[table["kelime"]==keys].index.values # key tabloda kelime olarak var mı
            if(initial > 0): # varsa
                penalty = similar_dict.get(keys)
                penalty += 3
                if(penalty < 20):
                    initial = initial[0]
                    print(initial)
                    sims = table[col].values[initial]
                    for element in sims:
                        print(element)
                        if(element not in dict2.keys() and element not in similar_dict.keys() and element != ''):
                            dict2.update({element:penalty})
                    
                    #return copy
    #◘dict2.update(similar_dict)                 
    return dict2,similar_dict
#%%
b = findSimilars(penalty,initial)"""