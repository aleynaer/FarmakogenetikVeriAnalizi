# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:33:25 2021

@author: Asus
"""

import pandas as pd
import numpy as np

class dataManipulating:
        
    # def __init__():
    #     pass
        
    def prepareData(self):
        
        df1 = pd.read_csv("CTD_D009385_chemicals.csv")
        filtered_df1 = df1.copy()
        filtered_df1.drop(columns=["CAS RN", "Direct Evidence", "Reference Count"], inplace=True) #29915 satır
        filtered_df1.sort_values('Chemical ID', ascending=True, inplace=True) # Chemical ID'ye göre artan şekilde sıralar
        filtered_df1.set_index(np.arange(len(filtered_df1.index)), inplace = True) #sıralanmış veriye göre tekrar indeksleme yapar
        drugList = []
        
    
        f = open("drugs.txt","r",encoding = 'utf-8')
        drugList.append(f.read().splitlines())
        f.close()

        drugList = np.transpose(drugList)
        
    
        y = 0
        temp = "aaa" # tekrarlanan kimyasal isimlerini tutmak için
        control = 1 # 1 ilac olduğunu, 0 olmadığını gösterir
        rows = len(filtered_df1)

        while(y < rows):
             i = (filtered_df1["Chemical Name"]).values[y] 
             if(i == temp):
                 if(control == 0):
                     filtered_df1.drop(filtered_df1.index[y],axis = 0, inplace = True)
                     print("çıkar",y,i)
                 else:
                    y += 1
                    continue
             else:
                 if(not(i in drugList)):
                    filtered_df1.drop(filtered_df1.index[y],axis = 0, inplace = True)
                    control = 0
                    print("çıkar",y,i)
                 else:
                    print(y,i)
                    y += 1
                    control = 1
                    temp = i 
        filtered_df1['geneInferences'] = filtered_df1['Inference Network'].str.split('|').tolist()
        filtered_df1.drop(["Inference Network"], axis=1, inplace=True)
        filtered_df1.rename(columns={'Chemical Name': 'Drug Name', 'Chemical ID': 'Drug ID'}, inplace=True)
         
    
        filtered_df1 = filtered_df1.explode('geneInferences', ignore_index = True)
        filtered_df1["Inference Score"] = filtered_df1['Inference Score'].str.replace(",",".")
        filtered_df1["Inference Score"] = pd.to_numeric(filtered_df1["Inference Score"], downcast="float")
        filtered_df1.dropna(subset = ["Inference Score"], inplace=True)
        filtered_df1.set_index(np.arange(len(filtered_df1.index)), inplace = True)
        
    
        filtered_df1.to_csv('drug_gene_disease.csv', index = False)
        filtered_df1.to_excel('drug_gene_disease.xlsx', index = False)
        