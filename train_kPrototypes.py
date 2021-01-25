# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 14:30:33 2021

@author: Asus
"""
import pandas as pd
from kmodes.kprototypes import KPrototypes

data = pd.read_csv("created files/drug_gene_disease.csv")
#data.drop(columns=["Unnamed: 0"], inplace=True)

data_copy = data.copy()
data_copy.drop(columns = ["Drug ID","Disease ID"], inplace = True)

#%% eğitime sokmak için ilaç, hastalık, gen ve skor değerleri array'e atılır

tArray = data_copy.values
tArray[:,2] = tArray[:,2].astype(float).round(2)

#%% eğitim

kproto = KPrototypes(verbose = 2, max_iter = 20) # default küme sayısı 8'dir
clusters = kproto.fit_predict(tArray, categorical=[0,1,3]) # kategorik değerlerin olduğu sütunlar belirtilir

#%% küme değeri bilgisi sütun olarak tabloya eklenir

print(kproto.cluster_centroids_)

cluster_array = []

for c in clusters:
    cluster_array.append(c)

data['cluster'] = cluster_array
data_copy['cluster'] = cluster_array

#%% eğitilmiş verinin lokale kaydedilmesi

data.to_csv('trained_kPrototypes.csv', index = False)
data.to_excel('trained_kPrototypes.xlsx', index = False)
data_copy.to_excel('trained_kPrototypes(1).xlsx', index = False)

#%% çeşit sayısını görmek için

num_clusters =  pd.Series(data["cluster"].drop_duplicates().values)
num_diseases =  pd.Series(data["Disease Name"].drop_duplicates().values) 
num_genes = pd.Series(data["geneInferences"].drop_duplicates().values) 
num_drugs = pd.Series(data["Drug Name"].drop_duplicates().values)

