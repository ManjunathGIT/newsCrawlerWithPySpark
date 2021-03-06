#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import flask
# 데이터베이스를 위한 라이브러리
import re
import pymysql
# JSON을 위한 라이브러리
import json
import collections
# Apache-Spark를 위한 라이브러리
# 크롤링을 위한 라이브러리
from jobjangDTO import Information
from webCrawler import Crawling
application = flask.Flask(__name__)
application.debug = True
@application.route('/')
def hello_world():
    storage = Storage()
    storage.populate()
    row = storage.row()
    return "Are you OK %d!" % row
class Storage():
    def __init__(self):
        self.db = pymysql.connect(
            user = os.getenv('MYSQL_USERNAME', ''),
            passwd = os.getenv('MYSQL_PASSWORD', ''),
            db = os.getenv('MYSQL_INSTANCE_NAME', ''),
            host = os.getenv('MYSQL_PORT_3306_TCP_ADDR', ''),
            port = int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306')),
            charset ='utf8',
            use_unicode=False,
            init_command='SET NAMES UTF8'
            )
        cur = self.db.cursor()
        print("connection success!!")
        print(sys.stdin.encoding)
    def stripslashes(self, s):
        r = re.sub(r"\\(n|r)", "\n", s)
        r = re.sub(r"\\", "", r)
        return r
    def escape(self, s):
        '''
        따옴표, 쌍따옴표 등 SQL 쿼리문에서 문자로 처리되어야 할 것들에 ESCAPE문을 걸어준다.
        '''
        if s is None: return None
        return pymysql.escape_string(s)
    def getTags(self):
        '''
        태그 DB를 모두 받아온다.
        '''
        cur = self.db.cursor()
        cur.execute('SELECT * FROM tags')
        row = cur.fetchall()
        total = len(row)
        entries = []
        if total < 1:
            print('No Tag entries')
        else:
            for record in range(total):
                temp1 = row[record][0].decode('utf8', 'surrogatepass')
                temp2 = row[record][1].decode('utf8', 'surrogatepass')
                entries.append([temp1, temp2])
        return entries
    def getInfo(self):
        """
        기사, 채용정보를 DB에서 모두 받아온다.
        """
        cur = self.db.cursor()
        sql = """SELECT * FROM information"""
        cur.execute(sql)
        #self.db.commit()
        row = cur.fetchall()
        total = len(row)
        entries = []
        if total < 1:
            print('No Infomation entries')
        else:
            for record in range(total):
                entry = Information()
                entry.setUrl(row[record][1].decode('utf8', 'surrogatepass'))
                entry.setHigh(row[record][2].decode('utf8', 'surrogatepass'))
                #json_obj = json.loads(row[record][3].decode('utf8', 'surrogatepass'), encoding="utf-8", object_pairs_hook=collections.OrderedDict)
                #json_obj = json.dumps(row[record][3], ensure_ascii=False, sort_keys=False, separators=(',', ':')).encode('utf-8')
                entry.setLow(row[record][3].decode('utf8', 'surrogatepass'))
                entry.setTitle(row[record][4].decode('utf8', 'surrogatepass'))
                entry.setContent(row[record][5].decode('utf8', 'surrogatepass'))
                entry.setClickNum(row[record][6])
                entry.setAType(row[record][7].decode('utf8', 'surrogatepass'))
                entry.setKGroup(row[record][8])
                entry.setPDate(row[record][9].decode('utf8', 'surrogatepass'))
                entry.setMeta(row[record][10].decode('utf8', 'surrogatepass'))
                entries.append(entry)
        return entries

    def setInfo(self, infos, t):
        '''
        기사, 채용정보를 DB에 저장한다.
        TAG는 JSON 타입으로 저장한다.
        '''
        cur = self.db.cursor()
        sql = ""
        for index, info in enumerate(infos):
            #tags = json.dumps(info.getLow(), ensure_ascii=False, sort_keys=False)
            if t is 1:
                sql = "INSERT INTO information (url, high, low, title, content, click_num, a_type, k_group, p_date, meta) "\
                      "SELECT %s, %s, %s, %s, %s, 0, %s, 0, %s, %s FROM DUAL "\
                      "WHERE NOT EXISTS (SELECT url FROM information WHERE url=%s)"
                values = (info.url, info.high, info.low, info.title, info.content, \
                          "Article", info.pDate(), info.meta(), info.url
                cur.execute(sql, values)
                self.db.commit()
                print("[%d]Information Insertion Success!" % (index+1))

    def setKGroup(self, labels):
        '''
        K-MEANS 알고리즘으로 K-Group을 라벨링한다.
        '''
        cur = self.db.cursor()
        sql = ""
        for index, label in enumerate(labels):
            sql = "UPDATE information SET k_group=%s WHERE PK_aid=%s"
            values = (label[1], label[0])
            cur.execute(sql, values)
            self.db.commit()
            print("[%d]K-Group Insertion Success!" % (index+1))

    def get_hash_tag(pk_aid):
        sql = "SELECT low FROM information WHERE PK_aid = %s"
        values = (pk_aid)
        cur.execute(sql, values)
        row = cur.fetchall()
        json_obj = json.loads(row[0].decode('utf8', 'surrogatepass'), encoding="utf-8")
        conn.commit()
        return temps

    def populate(self):
        cur = self.db.cursor()
        cur.execute("INSERT INTO rows(row) VALUES(520)")

    def getArticle(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM article")
        row = cur.fetchall()
        return row


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=3300)
