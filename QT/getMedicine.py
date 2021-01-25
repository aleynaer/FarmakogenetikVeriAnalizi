import time
import unittest

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import dataFromExcel


class Test(unittest.TestCase, dataFromExcel.GetDataFromExcel):
    """
        selenium kütüphanesi ile birlikte excel'den alınan ilaç ID'lerinin site içerisinde gezilerek karşılıklarının
        bulunması için oluşturulan sınıf
    """

    def getMedicine(self):  # ilaç id'lerinin site içerisinde gezinerek karşılıklarını bulan fonksiyon
        druglist = self.getDrugNameFromExcel()
        druglistRange = len(druglist)
        browser = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        for i in range(0, druglistRange):  # ilaç listenin uzunluğu kadar çalışacak fonksiyon
            wait = WebDriverWait(browser, 10)
            browser.get('https://go.drugbank.com/drugs/' + druglist[i])
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.content-header.d-sm-flex.align-items-center > h1")))
            drugName = browser.find_element_by_css_selector('div.content-header.d-sm-flex.align-items-center > h1')
            print(drugName.text)  # bulunan ilacın karşılığının basılması
        browser.quit()  # fonksiyon bitiminde tarayıcı kapatılacak

    def searchForMedicine(self,
                          medicineName):  # aratılan anahtara karşılık gelen ilaçların listesini döndüren fonksiyon
        browser = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        wait = WebDriverWait(browser, 10)
        browser.get("https://go.drugbank.com/")
        search_input = browser.find_element_by_id("query")  # anahtarın aratıldığı kısım
        search_input.send_keys(medicineName)
        search_input.send_keys(Keys.RETURN)
        page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page_info"))).text
        seperated_page = page.split(sep=" ")  # sayfa sayısını bularak dönen ilaç liste sayısını hesaplıyoruz
        num1 = int(seperated_page[4])
        numb2 = int(seperated_page[6])
        page_number = int(numb2 / num1)
        for i in range(0, page_number + 1):  # ilaç sayfası kadar döngüyü devam ettiriyoruz
            time.sleep(1)  # beautiful soup kütüphanesi ile sayfadaki ilaçların isimlerini aldığımız döngü
            url = browser.current_url
            headers = {'User-Agent':
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 "
                           "Safari/537.36"}
            drugbank = requests.get(url, headers=headers)
            print(drugbank.status_code)
            pageSource = drugbank.content  # sayfanın içeriğinin alındığı kısım
            soup = BeautifulSoup(pageSource, "html.parser")
            drugName = soup.findAll("h2", {"class": "hit-link"})
            for j in range(0, len(drugName)):
                print(drugName[j].text)
                time.sleep(0.1)
            if len(drugName) == 25:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "next"))).click()
                # sayfadaki eleman sayısı max 25 olduğu için 25 olmaması durumunda son sayfada olduğumuzu anlıyoruz
            else:
                pass
        browser.quit()  # fonksiyon tamamlandığında tarayıcı kapanıyor.
