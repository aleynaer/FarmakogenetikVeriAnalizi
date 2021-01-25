import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class FilterDrugs:
    def __init__(self):
        self.drugList = None
        self.chemList = None

    def createChemList(self):
        df1 = pd.read_csv("CTD_D009385_chemicals.csv")
        df2 = pd.read_csv("CTD_D009385_interactions.csv")

        print(df1.tail(5))
        print(df2.tail(5))

        df1.sort_values('Chemical ID', ascending=True, inplace=True)
        df2.sort_values('Chemical ID', ascending=True, inplace=True)

        self.drugList = []
        chems = pd.Series(df1.loc[:, "Chemical Name"].values)  # gets chem name column
        self.chemList = pd.Series(chems.drop_duplicates().values)  # gets unique values

        df1.drop(columns=["CAS RN", "Direct Evidence", "Reference Count"], inplace=True)
        df2.drop(columns=["CAS RN", "Reference Count", "Organism Count"], inplace=True)

        df = pd.DataFrame(df1)
        df['geneInferences'] = df['Inference Network'].str.split('|')
        df.drop(["Inference Network"], axis=1, inplace=True)
        file = open("drugs.txt", "a", encoding='UTF - 8')

    def drugListUpdate(
            self):  # listeden alınan anahtar kelimelerin ilaç olup olmama durumuna göre filtrelemek için oluşturulan fonksiyon
        self.createChemList()
        global DESCRIPTION_LOCATOR, INDICATION_LOCATOR
        browser = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        wait = WebDriverWait(browser, 2)
        count = 0
        for chemical in self.chemList:  # listedeki eleman kadar döngü devam edecek
            browser.get('https://go.drugbank.com')
            count += 1
            print(count)
            browser.maximize_window()
            search_input = wait.until(EC.presence_of_element_located((By.ID, "query")))
            search_input.send_keys(chemical)  # arama yaptığımız kısım
            search_input.send_keys(Keys.RETURN)
            try:  # sonuç bulmazsa ilerleyeceği senaryo
                no_result = browser.find_element_by_class_name("drug-card")
                result_assertion = no_result.is_displayed()
                assert result_assertion == True
            except:
                continue
            try:  # site yapısında iki farklı konumda bulunabiliyorlar o yüzden iki konumu da deneyip doğru olanı buluyor
                try:
                    NOTICE_BAR = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stub-notice")))
                    if NOTICE_BAR.is_displayed():
                        DESCRIPTION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(3) > dd:nth-child(6)")
                        INDICATION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(5) > dd:nth-child(2)")
                except:
                    DESCRIPTION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(2) > dd:nth-child(6)")
                    INDICATION_LOCATOR = (By.CSS_SELECTOR, "dl:nth-child(4) > dd:nth-child(2)")
                description_text = wait.until(EC.presence_of_element_located(DESCRIPTION_LOCATOR)).text.upper()
                # açıklama paragrafının kelimelerine ayırıyoruz
                seperated_description_text = description_text.split(' ')
                # ilaç olduğunu anlamak için paragraf içinde arattığımız kelime listesi
                keywords = ['DRUG', 'TREAT', 'TREATMENT', 'CURE', 'REMEDY']
                if any(i in keywords for i in
                       seperated_description_text):  # açıklama kısmında istenen kelimelerden biri bulunursa dosyaya yazdırıyor
                    print('found on description ' + chemical)
                    self.drugList.append(chemical)
                    file = open("drugs.txt", "a", encoding='UTF - 8')
                    file.write(chemical + '\n')
                    continue
                # aynı işlemleri indikasyon kısmı için de tekrarlıyoruz
                indication_text = wait.until(EC.presence_of_element_located(INDICATION_LOCATOR)).text.upper()
                seperated_indication_text = indication_text.split(' ')
                if any(i in keywords for i in seperated_indication_text):
                    print('found on indication ' + chemical)
                    self.drugList.append(chemical)
                    file = open("drugs.txt", "a", encoding='UTF - 8')
                    file.write(chemical + '\n')
            except:
                continue
        print(self.drugList)
        browser.quit()  # fonksiyon tamamlandığında tarayıcıyı kapatacak
