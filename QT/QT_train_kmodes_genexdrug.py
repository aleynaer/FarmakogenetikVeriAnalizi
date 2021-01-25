# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 16:54:04 2021

@author: Asus
"""
import pandas as pd
from sklearn import preprocessing
from kmodes.kmodes import KModes

class kModes_geneDrug():
    
    def train_kModes_gd(self):
        
        data = pd.read_csv("drug_gene_disease.csv")
        #data.drop(columns=["Unnamed: 0"], inplace=True)

        data_copy = data.copy()
        data_copy.drop(columns = ["Drug ID","Disease Name","Disease ID","Inference Score"], inplace = True)

# sadece şu sütunlar eğitime sokulur = Drug Name, gene
# eğitime sokulan değerlere göre veriler kümelenir, böylelikle gene x drug ilişkisi incelenir

# her bir feature (sütun) için değerler kategorilendirilir (etiketlenir)

        le = preprocessing.LabelEncoder()
        data_copy = data_copy.apply(le.fit_transform)
        data_copy.head()

# eğitim

        km_huang = KModes(init = "Huang", n_init = 1, verbose=1, max_iter = 20) # default küme sayısı 8'dir
        fitClusters_huang = km_huang.fit_predict(data_copy)

# küme değeri bilgisi sütun olarak tabloya eklenir

        cluster_array = []

        for c in fitClusters_huang:
            cluster_array.append(c)

        data['cluster'] = cluster_array
        data_copy['cluster'] = cluster_array

# eğitilmiş verinin lokale kaydedilmesi

        data.to_csv('trained_kmodes(genexdrug).csv', index = False)
        data.to_excel('trained_kmodes(genexdrug).xlsx', index = False)
        data_copy.to_excel('trained_kmodes(genexdrug)(1).xlsx', index = False)