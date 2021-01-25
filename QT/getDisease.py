import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import dataFromExcel


class Test(unittest.TestCase, dataFromExcel.GetDataFromExcel):
    """
    Selenium kütüphanesi ile birlikte site içerisinde gezinerek hastalık id'lerinin karşılıklarını buluyoruz
    """

    def getDisease(self):  # excel dosyasından alınan hastalık ID'lerin karşıklarını bulan fonksiyon
        diseaseList = self.getDiseaseFromExcel("MESH")
        diseaseListRange = len(diseaseList)
        browser = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        for i in range(0, diseaseListRange):  # liste uzunluğu boyunca site içerisinde gezinecek
            wait = WebDriverWait(browser, 10)
            browser.get('https://www.ncbi.nlm.nih.gov/medgen/?term=' + diseaseList[i])
            content = browser.page_source.__contains__(
                "Search results")  # birden çok sonuç getirdiğinde izlenecek senaryo
            if content:
                browser.get('https://meshb.nlm.nih.gov/record/ui?ui=' + diseaseList[i])
                diseaseName = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "dl > .ng-binding"))).text
                time.sleep(1)
                browser.get('https://www.ncbi.nlm.nih.gov/medgen/?term=' + diseaseName)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title > a"))).click()
                diseaseClass = browser.page_source.__contains__(
                    "Neoplastic Process")  # getirilen sonucun istenen sonuç olduğunun kontrolü
                if diseaseClass:
                    diseaseName = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MedGenTitleText"))).text
                    time.sleep(1)
                    print(diseaseName)
            else:  # tek sonuç getirdiğinde izlenecek senaryo
                diseaseClass = browser.page_source.__contains__(
                    "Neoplastic Process")  # getirilen sonucun istenen sonuç olduğunun kontrolü
                if diseaseClass:
                    diseaseName = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MedGenTitleText"))).text
                    time.sleep(1)
                    print(diseaseName)
                else:
                    continue
        browser.quit()  # fonksiyon bittiğinde tarayıcıyı kapatacak
