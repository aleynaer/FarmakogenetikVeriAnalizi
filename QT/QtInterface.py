import sys

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QApplication, QLabel

import QT_dataManipulating
import QT_train_kPrototypes
import QT_train_kmodes
import QT_train_kmodes_genexdrug
import filterDrugs
import getDisease
import getMedicine


class window(QMainWindow, getDisease.Test, getMedicine.Test, filterDrugs.FilterDrugs,
             QT_dataManipulating.dataManipulating, QT_train_kPrototypes.kPrototypes,
             QT_train_kmodes_genexdrug.kModes_geneDrug, QT_train_kmodes.kModes):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def getDiseaseNames(self):  # kalıtım ile fonksiyon çağırmak için burada fonksiyon oluşturmamız gerekiyor.
        getDisease.Test.getDisease(self)

    def getMedicineNames(self):  # aynı işlem diğer fonksiyonlar için de gerekli
        getMedicine.Test.getMedicine(self)

    def searchMedicine(self, medicineName):
        getMedicine.Test.searchForMedicine(self, medicineName)

    def filterDrugs(self):
        filterDrugs.FilterDrugs.drugListUpdate(self)

    def dataPreparing(self):
        QT_dataManipulating.dataManipulating.prepareData(self)

    def kPrototypeTraining(self):
        QT_train_kPrototypes.kPrototypes.train_kProto(self)

    def kModesTrainingGenDrug(self):
        QT_train_kmodes_genexdrug.kModes_geneDrug.train_kModes_gd(self)

    def kModesTrainig(self):
        QT_train_kmodes.kModes.train_kModes(self)

    def initUI(self):
        self.setWindowTitle('Farmakogenetik Projesi')
        verticalBox = QVBoxLayout()  # dikeysel bir layout oluşturuyoruz
        horizontalBox = QHBoxLayout()  # yatay bir layout oluşturuyoruz.

        labelMerhaba = QLabel('Veri Boyutuna bağlı olarak süre uzun sürebilir !', self)
        horizontalBox5 = QHBoxLayout()
        horizontalBox5.addWidget(labelMerhaba)
        verticalBox.addLayout(horizontalBox5)

        dataPrepareButton = QPushButton("Veri ön işleme")
        dataPrepareButton.setFixedWidth(200)
        horizontalBox.addWidget(dataPrepareButton)
        verticalBox.addLayout(horizontalBox)
        dataPrepareButton.clicked.connect(lambda: self.dataPreparing())

        kPrototypeButton = QPushButton("kPrototype Eğitimi")
        kPrototypeButton.setFixedWidth(200)
        horizontalBox.addWidget(kPrototypeButton)
        kPrototypeButton.clicked.connect(lambda: self.kPrototypeTraining())

        horizontalBox4 = QHBoxLayout()

        kModesButton = QPushButton("kModes Eğitimi (ilaç ve gen)")
        kModesButton.setFixedWidth(200)
        horizontalBox4.addWidget(kModesButton)
        kModesButton.clicked.connect(lambda: self.kModesTrainingGenDrug())

        kModesButton2 = QPushButton("kModes Eğitimi")
        kModesButton2.setFixedWidth(200)
        horizontalBox4.addWidget(kModesButton2)
        kModesButton2.clicked.connect(lambda: self.kModesTrainig())

        verticalBox.addLayout(horizontalBox4)

        horizontalBox2 = QHBoxLayout()  # ikinci bir satır oluşturuyoruz.

        diseaseButton = QPushButton("Hastalıkları Topla")  # hastalıkları toplamak için oluşturulan buton
        diseaseButton.setFixedWidth(200)
        horizontalBox2.addWidget(diseaseButton)
        diseaseButton.clicked.connect(lambda: self.getDiseaseNames())  # butona tıkladığında fonksiyon çalışıyor.

        medicineButton = QPushButton("İlaçları Topla")  # ilaçları toplamak için oluşturulan buton
        medicineButton.setFixedWidth(200)
        horizontalBox2.addWidget(medicineButton)
        medicineButton.clicked.connect(lambda: self.getMedicineNames())

        verticalBox.addLayout(horizontalBox)
        horizontalBox3 = QHBoxLayout()

        searchMedicineButton = QPushButton("İlaç ara")  # ilaçları aramak için oluşturulan buton
        searchMedicineButton.setFixedWidth(200)
        horizontalBox3.addWidget(searchMedicineButton)
        searchMedicineButton.clicked.connect(lambda: self.searchMedicine("cancer"))

        filterDrugs = QPushButton("İlaçları filtrele")  # ilaçları filtrelemek için oluşturulan fonksiyon
        filterDrugs.setFixedWidth(200)
        horizontalBox3.addWidget(filterDrugs)
        filterDrugs.clicked.connect(lambda: self.filterDrugs())

        widget = QWidget()
        self.setCentralWidget(widget)  # butonları ortalıyoruz
        widget.setLayout(verticalBox)
        verticalBox.addLayout(horizontalBox2)
        verticalBox.addLayout(horizontalBox3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec())
