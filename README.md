News Crawler with PySpark(Apache Spark 1.6.1 - Hadoop 2.6)
=========================
크롤링을 통해 네이버 뉴스기사들을 긁어오고, 아파치 스파크(pyspark)의 K-means 클러스터링으로 IT부분의 네이버 뉴스 기사들을 키워드별로 라벨링하는 코드입니다.
Naver IT News Crawler and clustering algorithm(K-MEANS) for keyword labelling with Apache-Spark(Pyspark).

Contents
--------

### main.py
You can select what this app does on `main.py`.

### application.py
Connect this app to DB based Mysql and act like DAO with jabjangDTO.py

### jabjangDTO.py
this is DTO for Mysql and K_menas clustering.

### K_MEANS.py
With `PySpark 1.6.1`, clustering and labeling crawled news in mysql by already cherry-picked tags.

FYI, this isn't optimized method for effective clustering
