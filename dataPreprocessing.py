# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 13:44:21 2021

@author: Asus
"""
import pandas as pd
import numpy as np

df1 = pd.read_csv("CTD_D009385_chemicals.csv")
#df2 = pd.read_csv("CTD_D009385_interactions.csv")

print(df1.tail(5))

chems = pd.Series(df1.loc[:, "Chemical Name"].values)  # chemical name sütununu alır
chemList = pd.Series(chems.drop_duplicates().values)  # eşsiz chemical name değerlerini tutar
drugList = [] # sadece ilaçları tutar

filtered_df1 = df1.copy()
#filtered_df2 = pd.DataFrame(df2)

filtered_df1.drop(columns=["CAS RN", "Direct Evidence", "Reference Count"], inplace=True) #29915 satır
#filtered_df2.drop(columns=["CAS RN", "Reference Count", "Organism Count"], inplace=True) #1045869 satır


filtered_df1.sort_values('Chemical ID', ascending=True, inplace=True) # Chemical ID'ye göre artan şekilde sıralar
#df2.sort_values('Chemical ID', ascending=True, inplace=True)

filtered_df1.set_index(np.arange(len(filtered_df1.index)), inplace = True) #sıralanmış veriye göre tekrar indeksleme yapar
#filtered_df2.set_index(np.arange(len(filtered_df2.index)), inplace = True)


#filtered_df1 = pd.read_csv("filtered_df1.csv")  -- hazır dosya ile işlem yaomak için yorumu kaldırın
#filtered_df2 = pd.read_csv("filtered_df2.csv")
#filtered_df1.drop(columns=["Unnamed: 0"], inplace=True) -- hazır dosya ile işlem yaomak için yorumu kaldırın
#filtered_df2.drop(columns=["Unnamed: 0"], inplace=True)


#%% DrugBank sitesine erişilerek "Chemical Name" değerlerini tek tek sorgular
# fazladan işlem yapmamak için ilgili sütunun eşsiz değerlerinin tutulduğu chemList serisi kullanılır
# Sorgu sonucu açılan sayfanın içeriğinde girdiğimiz keywordleri arar, eşleşme bulursa bu kimyasalı 
# oluşturulan drug.txt dosyasına yazar, böylece drugs.txt dosyasında ilaç olarak adlandırdığımız
# "Chemical Name" değerleri toplanır


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

file = open("created files/drugs.txt", "w+",encoding = 'utf-8') # ilaçları kaydetmek için drugs.txt dosyası oluşturur

def drugListUpdate():  # kimyasalların ilaç olup olmadığını denetler -> DrugBank
    global DESCRIPTION_LOCATOR, INDICATION_LOCATOR
    browser = webdriver.Chrome('chromedriver.exe')
    wait = WebDriverWait(browser, 2)
    for chemical in chemList:
        browser.get('https://go.drugbank.com') 
        browser.maximize_window()
        search_input = wait.until(EC.presence_of_element_located((By.ID, "query")))
        search_input.send_keys(chemical)
        search_input.send_keys(Keys.RETURN)
        try:
            no_result = browser.find_element_by_class_name("drug-card")
            result_assertion = no_result.is_displayed()
            assert result_assertion == True
        except:
            continue
        try:
            try:
                NOTICE_BAR = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stub-notice")))
                if NOTICE_BAR.is_displayed():
                    DESCRIPTION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(3) > dd:nth-child(6)")
                    INDICATION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(5) > dd:nth-child(2)")
            except:
                DESCRIPTION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(2) > dd:nth-child(6)")
                INDICATION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(4) > dd:nth-child(2)")
            description_text = wait.until(EC.presence_of_element_located(DESCRIPTION_LOCATOR)).text.upper()
            seperated_description_text = description_text.split(' ')
            keywords = ['DRUG', 'TREAT', 'TREATMENT', 'CURE', 'REMEDY'] # bu kelimeleri içeriyorsa o kimyasalı ilaç sayarız
            if any(i in keywords for i in seperated_description_text):
                print('found on description ' + chemical)
                drugList.append(chemical)
                file = open("created files/drugs.txt", "a",encoding = 'utf-8')
                file.write(chemical)
                file.write("\n")
                continue
            indication_text = wait.until(EC.presence_of_element_located(INDICATION_LOCATOR)).text.upper()
            seperated_indication_text = indication_text.split(' ')
            if any(i in keywords for i in seperated_indication_text):
                print('found on indication ' + chemical)
                drugList.append(chemical)
                file = open("created files/drugs.txt", "a",encoding = 'utf-8')
                file.write(chemical)
                file.write("\n")
                
        except:
            continue
    print(drugList)
    browser.quit()

drugListUpdate()
file.close()

#%% hazır drugs.txt dosyasını kullanmak yorumu kaldırın

f = open("created files/drugs.txt","r",encoding = 'utf-8')
drugList.append(f.read().splitlines())
f.close()

drugList = np.transpose(drugList)

#%% drugList'teki ilaç değerlerine göre Chemical Name sütununu filtreler

y = 0
temp = "aaa" # tekrarlanan kimyasal isimlerini tutmak için
control = 1 # 1 ilac olduğunu, 0 olmadığını gösterir
rows = len(filtered_df1)

while(y < rows):
    i = (filtered_df1["Chemical Name"]).values[y] 
    if(i == temp):
        if(control == 0):
            filtered_df1.drop(filtered_df1.index[y],axis = 0, inplace = True) # ilaç olmayan satırları siler
            print("çıkar",y,i)
        else:
            y += 1
            continue
    else:
        if(not(i in drugList)):
             filtered_df1.drop(filtered_df1.index[y],axis = 0, inplace = True)  # ilaç olmayan satırları siler
             control = 0
             print("çıkar",y,i)
        else:
            print(y,i)
            y += 1
            control = 1
    temp = i 
        
#filtered_df1.set_index(np.arange(len(filtered_df1.index)), inplace = True)

#%% ikinci tablonun (interactions) ilaca göre filtrelenmesi, aynı işlem uygulanır

# y = 0
# temp = "aaa" # tekrarlanan kimyasal isimlerini tutmak için
# control = 1 # 1 ilac olduğunu, 0 olmadığını gösterir
# rows = len(filtered_df2)

# while(y < rows):
#     i = (filtered_df2["Chemical Name"]).values[y] 
#     if(i == temp):
#         if(control == 0):
#             filtered_df2.drop(filtered_df2.index[y],axis = 0, inplace = True)
#             print("çıkar",y,i)
#         else:
#             y += 1
#             continue
#     else:
#         if(not(i in drugList)):
#              filtered_df2.drop(filtered_df2.index[y],axis = 0, inplace = True)
#              control = 0
#              print("çıkar",y,i)
#         else:
#             print(y,i)
#             y += 1
#             control = 1
#     temp = i 

#%% filtrelenmiş tablonun (interactions) kaydedilmesi

# filtered_df2.set_index(np.arange(len(filtered_df2.index)), inplace = True)
# filtered_df2.to_csv('filtered_df2.csv')
# filtered_df2.to_excel('filtered_df2.xlsx', index = False)

#%%% filtreleme sonrasında ilaçla ilişkili sütunları yeniden adlandırır


filtered_df1.rename(columns={'Chemical Name': 'Drug Name', 'Chemical ID': 'Drug ID'}, inplace=True)
#filtered_df2.rename(columns={'Chemical Name': 'Drug Name', 'Chemical ID': 'Drug ID'}, inplace=True)

#%% içerdiği gen değerlerini tek tek listeleyecek şekilde veri setinin satırlarını genişletir

filtered_df1['geneInferences'] = filtered_df1['Inference Network'].str.split('|').tolist()
filtered_df1.drop(["Inference Network"], axis=1, inplace=True)

#filtered_df2['Interaction Type'] = filtered_df2['Interaction Actions'].str.split('|').tolist()
#filtered_df2.drop(["Interaction Actions"], axis=1, inplace=True)
filtered_df1 = filtered_df1.explode('geneInferences', ignore_index = True)

#%%  sayısal değer olan Inference Score'un string'den float'a dönüştürülmesi

filtered_df1["Inference Score"] = filtered_df1['Inference Score'].str.replace(",",".")
filtered_df1["Inference Score"] = pd.to_numeric(filtered_df1["Inference Score"], downcast="float")


#%% NaN değerlerin tablodan silinmesi

filtered_df1.dropna(subset = ["Inference Score"], inplace=True)
filtered_df1.set_index(np.arange(len(filtered_df1.index)), inplace = True)
#%% filtrelenmiş tablonun (filtered_df1) lokale kaydedilmesi

filtered_df1.to_csv('drug_gene_disease.csv', index = False)
filtered_df1.to_excel('drug_gene_disease.xlsx', index = False)

# veri, eğitime hazır.