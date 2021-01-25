# FarmakogenetikVeriAnalizi
Bu çalışma, kanser üzerine farmakogenetik verilerin manipülasyonunu ve analizini kapsar.

Comperative Toxicogenomics Database' den erişilen veri setleri üzerine çalışmalar yapılmıştır. Üzerine yoğunlaşılan veri seti, kimyasal (cause / cure), hastalık çeşidi ve gen bilgileri barındırır. Veri setine şuradan ulaşılabilir: http://ctdbase.org/detail.go;jsessionid=C20ABCF6087A4AAA7F7D61D20BB9A449?type=disease&acc=MESH%3aD009385&view=chem

Proje, Python 3.7.1 ile kodlanmış ve arayüz geliştirmede QT kullanılmıştır.

Kullanılan veri setinin "Chemical Name" değerleri hastalığa sebep olan ve hastalığı tedavi eden kimyasalları birarada bulundurmaktadır. Ön işleme aşamasında, DrugBank'ten faydalanılarak bu değerlerden tedavide kullanılanlar (ilaçlar) saklanmış -bu değerler drugs.txt dosyası ile lokale kaydedilmiştir- diğer satırlar silinerek tablo güncellenmiştir. İhtiyaca göre manipüle edilerek veri seti eğitime hazır hale getirilmiştir. 

DrugBank sorguları ve dosya işlemleri uzun sürdüğünden, hazır dosyalar kullanılabilir. drug_gene_disease.csv, veri setinin eğitime hazır hale getirilmiş versiyonudur.

Eğitimde 2 farklı yapay öğrenme algoritması kullanılmıştır. Bunlar kümeleme (clustering) algoritmaları olan K-Prototypes ve K-Modes'tur. Eğitilmiş veri seti, küme bilgisi eklenerek "trained_" prefixiyle kaydedilmiştir. Bu dosyalara bakılarak eğitim sonuçları incelenebilir.

Arayüz bu çalışmalarla beraber proje süresince uğraşılan modülleri de kapsar. Bu modüller disease ve chemical id'lerini decode etmeye yönelik yazılmıştır.


## Gereksinimler
-- çalıştırılan cihaza uyumlu chromedriver.exe dosyası (selenium ile yapılan işlemler için)
--KProtoypes 
--Kmodes 
--sklearn 
--PyQt5
