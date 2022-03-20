# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 22:14:22 2022

@author: AleynaEr


    HOT&COLD GAME (KELİMEYİ BUL)
    
    Kelime listesinden rastgele bir kelime seçilir
    Seçilen kelimeye yakın kelimeler tablo gezilerek listelenir
    Kelimelerin yakınlık dereceleri farklılık göstermektedir
    Kullanıcı, kelimeler girerek bilgisayarın seçtiği random kelimeyi bulmaya çalışır
    Kullanıcının girdiği kelimeler, benzerlik listesinde karşılaştılır
    Kullanıcıya tahminin yakın veya uzak olduğu (anlamsal olarak) bilgisi döndürülür 
    
    random kelimenin tabloda aldığı değerler sütunlar gezilerek bulunur
    sütunlarda, isim-fiil soruları ardışık gelmekte ve bir sonraki çifte geçilirken +1 ceza verilmektedir
    random kelimenin aldığı sütunlarda aldığı değer, tabloda kelime olarak tutulmakta mı bakılır
    şayet tutuluyorsa o kayda da gidilir ve aynı gezme işlemi yapılır
    başka kayda erişmenin cezası +5 tir
    
    ceza, kavramların kelimeye uzakılığını temsil eder
    düşük ceza: yakın anlam, yüksek ceza: uzak anlamlı
    
    ceza max 20 olabilir
    
    0-8: çok sıcak, 8-14: sıcak, 15-20: soğuk
    girilen tahmin similarity sözlüğünde yoksa: çok soğuk
    

"""


#%% importing essential libs and prepare table
import pandas as pd
from ast import literal_eval

table = pd.read_csv("hotncold_data.csv")

# prepare table, turn into values as list (pd.read_csv reads list as string)
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

#%% declaring variables
cols = list(table.iloc[:,1:].columns)
penalty = 1
similar_dict = {}
initial = random_num
copy = {}
dict2 = {}

#%% creating base similarity dict 
def simpleSimilars(penalty, initial):
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
      
#%% find neighbours and update similarity dict 
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
                               if(element not in dict2.keys() and element not in similar_dict.keys() and element != ''):
                                   dict2.update({element:penalty})
    return dict2             

#%% initialize similarity dict 
def createSimilarityDict():
    simpleSimilars(penalty, initial)
    i = 0
    while(i < 3):
        searchOthers(similar_dict,dict2)   
        similar_dict.update(dict2)
        i += 1
        
#%% initialize similarity dict for game
createSimilarityDict()

#%% compare prediction results 
def startPredict(predict):
    if(predict == hidden_word):
        print("Tebrikler! Bildiniz!")
        return True
    if(predict == 1):
        print
    elif(predict in similar_dict.keys()):
        penalty = similar_dict.get(predict)
        if(penalty < 9):
            print(" çok sıcak ")
        elif(penalty < 15):
            print(" sıcak ")
        elif(penalty < 20):
            print(" soğuk ")
    else:
        print(" çok soğuk ")

#%% game init    
def startGame():
    game_counter = 0
    counter = 0
    counter_h = 0
    
    print("***** KELİMEYİ BUL *****")
    print(".. ipucu almak için H'e basın ..")

    while(game_counter < 8):
        game_counter += 1
        
        user_input = input("** tahmin giriniz ** \n")
        user_input = user_input.lower()
        
        if(user_input == 'q'):
            game_counter = 8
            
        elif(user_input == 'h'):
            if(counter_h < 3):
                takeHint()
                counter_h += 1
            else:
                print(" ipucu hakkınız kalmadı :( ")
                game_counter -= 1
    
        else:
            if(counter < 5):
                counter += 1
                predict = startPredict(user_input)
                if(predict == True):
                    game_counter = 8
            else:
                print("bilemediniz..")
                game_counter = 8
            
#%% take hints for hidden word
def takeHint():
    up = len(similar_dict)
    ran_num = random.randint(0,up)
    keys_list = list(similar_dict)
    hint = keys_list[ran_num]
    print("ipucu: ", hint)
    
#%% starting game
startGame()
#%%
