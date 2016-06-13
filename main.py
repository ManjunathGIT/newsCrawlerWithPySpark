#!/usr/bin/python
#-*- coding: utf-8 -*-
import unittest
import time
# PySpark
import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row, HiveContext
#from pyspark.sql import HiveContext, Row
from pyspark.sql.types import DataType, IntegerType
# mllib for clustering
from pyspark.mllib.linalg import Vectors, DenseMatrix
from pyspark.mllib.clustering import GaussianMixture, KMeansModel, KMeans
from application import Storage
from webCrawler import Crawling
from jobjangDTO import Information
from K_MEANS import pyK
class TestSuite(unittest.TestCase):
    def test(self):
        storage = Storage()
        crawling = Crawling()
        K = pyK()
        while True:
            print("Welcome to JobJang Crawler!")
            print("1. Crawling")
            print("2. Calculating K-Group")
            print("3. exit")
            cmd = input("무엇을 할까요?(숫자 입력)")
            if cmd == '1':
                #getNews에 들어가는 매개변수는 기사를 긁어오는 범위다. (15면 15일치 기사들을 모두 긁음.)
                days = input("몇일치 기사를 긁어올까요?")
                print("1. IT")
                print("2. 경제")
                high = input("상위태그는 뭘로할까요?")
                if high == '1':
                    tag = "IT"
                else:
                    tag = "경제"
                results = crawling.getContent(crawling.getNews(tag, int(days)), storage.getTags());
                storage.setInfo(results, 1)
                entries = storage.getInfo()
                for index, entry in enumerate(entries):
                    e = entry
                    print('[%d개] ' % (index+1) + e.toString() + ' From DB')
                #time.sleep(5)
            elif cmd == '2':
                print("1. IT")
                print("2. 경제")
                high = input("상위태그는 뭘로할까요?")
                if high == '1':
                    tag = "IT"
                else:
                    tag = "경제"
                labels = K.calKGroup(tag, sc)
                storage.setKGroup(labels)
            elif cmd == '3':
                break
            else: continue

def main():
    unittest.main()
    unittest.close()

if __name__ == "__main__":
    main()
