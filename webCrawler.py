#!/usr/bin/python
# -*- encoding: utf-8 -*-
# import requests as rs
from urllib.request import Request, urlopen

import bs4
import time
# JSON을 위한 라이브러리
import json
from io import StringIO
# <meta property="og:title" content="구글 조립형 스마트폰 `아라` 실물 공개.. &quot;내년 출시 예정&quot;">
# <meta property="og:type" content="article">
# <meta property="og:url" content="http://news.naver.com/main/read.nhn?mode=LSD&amp;mid=sec&amp;oid=030&amp;aid=0002480868&amp;sid1=001">
# <meta property="og:image" content="http://imgnews.naver.net/image/origin/030/2016/05/22/2480868.jpg">
# <meta property="og:description" content="구글이 마치 레고처럼 모듈 방식으로 기능을 추가할 수 있는 조립식 스마트폰 `아라`의 개발자 버전 실물을 올해 가을에 내놓고 내년부터 판매한다는 계획을 ...">
# <meta property="og:article:author" content="전자신문 | 네이버 뉴스">
from operator import itemgetter
from datetime import datetime, date, timedelta
from jobjangDTO import Information
class Crawling:
    def getDateInNews(self, date):
        """
        기사에서 받은 날짜(YYYY-MM-DD)를 YYYYMMDD 문자열로 반환한다.
        """
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        return "" + year + month + day

    def getDate(self, d):
        """
        날짜 데이터를 YYYYMMDD 형식으로 뽑아준다
        """
        today = str(d.year)
        mon = ""
        if len(str(d.month)) < 2:
            mon = "0" + str(d.month)
        else:
            mon = str(d.month)
        today = today + mon
        day = ""
        if len(str(d.day)) < 2:
            day = "0" + str(d.day)
        else:
            day = str(d.day)
        today = today + day
        return today

    def getContent(self, list, wordlist):
        """
        BS4로 추출된 기사URL에서 내용물을 뽑아낸다.
        반환형 : Information 클래스 리스트
        words : Tag 리스트
        result : 결과값
        """
        words = []
        result = []
        for word in wordlist:
            words.append([word[0], word[1], 0])
        # print(words)
        count = 0
        for index, url in enumerate(list):
            if url.count("sid1=105") > 0:
                high_tag = 'IT'
            elif url.count("sid1=101") > 0:
                high_tag = '경제'
            else:
                continue
            news_url = url
            print(news_url)
            response = Request(news_url)
            html_content = urlopen(response).read()
            navigator = bs4.BeautifulSoup(html_content, 'html5lib')
            contents = navigator.find("div", id="main_content")
            # 기사 입력일 추출
            date = navigator.find("span", {"class": "t11"})
            if date is not None:
                datetext = self.getDateInNews(date.get_text()).strip().replace("\"\r\n\t", '')
                # 기사 제목 추출
                header = contents.h3.get_text().strip().replace("\"\r\n\t", '')
                # 기사 내용 추출

                text = ""
                content = contents.find("div", id="articleBodyContents")
                if content.find("table") is None:
                    text = content.get_text()
                else:
                    # 봇이 쓴 기사는 제외
                    continue
                # else:
                #     tables = content.find_all("table")
                #     for table in tables:
                #         tbodies = table.find_all("tbody")
                #         for tbody in tbodies:
                #             trs = tbody.find_all("tr")
                #             for tr in trs:
                #                 tds = tr.find_all("td")
                #                 tds = [ele.text for ele in tds]
                #                 tds = [ele for ele in tds if ele]
                #                 for td in tds:
                #                     text += td
                print(text)
                text = text.strip().replace("\"\r\n\t", '')
                total = header.upper() + " " + text.upper()
                # 기사 내용과 키워드 매칭 & 카운트(TAG)
                trigger = False
                tags = "["
                for word in words:
                    if word[0] == high_tag:
                        word[2] = total.count("" + word[1].upper())
                        if word[2] is not 0:
                            tags += "{\"" + word[1] + "\":" + str(word[2]) + "},"
                            trigger = True
                if trigger is True:
                    tags = tags[:-1]
                    count += 1
                else:
                    continue
                tags += "]"
                if high_tag is '사회':
                    high_tag = '경제'
                # 기사 표현을 위한 og meta 태그 추출
                og_title = navigator.find("meta", property="og:title")
                og_type = navigator.find("meta", property="og:type")
                og_url = navigator.find("meta", property="og:url")
                og_image = navigator.find("meta", property="og:image")
                og_description = navigator.find("meta", property="og:description")
                metas = str(og_title) + str(og_type) + str(og_url) + str(og_image) + str(og_description)
                # 내용물 SET
                info = Information()
                info.url(news_url.replace('&', '%26'))
                info.title(header)
                info.content(text)
                info.pDate(datetext)
                info.high(high_tag)
                info.low(tags)
                info.meta(metas.replace('&', '%26'))
                result.append(info)
                print('[%d개] ' % (count) + str(info) + ' Original')
        return result

    def getUrl(self, high, SPAN):
        """
        네이버 뉴스 기사가 표현하는 모든 항목별, 날짜별, 페이지별 URL들을 각각 생성해 반환한다.
        """
        # sid2=731 : 모바일
        sid1s = [["IT", 105], ["경제", 101]]
        sid2s_it = [["모바일", 731], ["인터넷/SNS", 226], ["통신/뉴미디어", 227], \
                    ["IT일반", 230], ["보안/해킹", 732], ["컴퓨터", 283], \
                    ["게임/리뷰", 229], ["과학 일반", 228]]
        sid2s_ec = [["금융", 259], ["증권", 258], ["산업/재계", 261], ["중기/벤쳐", 771], \
                    ["부동산", 260], ["글로벌경제", 262], ["생활경제", 310], ["경제일반", 263]]
        d = datetime.today()
        urls = []
        # SPAN은 현재날짜에서 뺀 날짜까지 긁어올 수
        for i in range(SPAN):
            date = self.getDate(d - timedelta(i))
            for sid1 in sid1s:
                if sid1[0] == high:
                    for sid2 in sid2s_it if sid1[0] is "IT" else sid2s_ec:
                        url = "http://news.naver.com/main/list.nhn?sid2=" + str(sid2[1]) + "&sid1=" + str(sid1[1]) + "&mid=shm&mode=LS2D&date=" + date
                        pages = self.getPage(url + "&page=1")
                        for page in range(pages):
                            # 최종 URL(sid1, sid2, date, page별 URL)을 배열에 저장
                            final_url = url + "&page=" + str(page + 1)
                            urls.append(final_url)
        return urls

    def getPage(self, url):
        """
        날짜별 표현된 뉴스기사가 20개 이상인 URL은 별도의 페이지로 나누어 표현되는데,
        이를 인식하고 페이지를 카운트하여 반환한다.
        """
        response = Request(url)
        html_content = urlopen(response).read()
        navigator = bs4.BeautifulSoup(html_content, 'html5lib')
        pages = navigator.find("div", {"class": "paging"})
        if pages is not None:
            page_nums = pages.find_all('a')
            page_num = [item.get_text() for item in page_nums]
            return 1 + len(page_num)
        return 1

    def getNews(self, high, SPAN):
        """
        BS4, request를 활용하여 URL별 존재하는 헤드라인 10개, 비헤드라인 10개 기사의
        주소를 리스팅한다.
        """
        # 기사들 주소를 담을 변수
        url_lists = []
        naver_urls = self.getUrl(high, SPAN)
        len_urls = len(naver_urls)
        for i in range(len_urls):
            naver_url = naver_urls[i]
            # 요청
            response = Request(naver_url)
            # 응답으로 부터 HTML 추출
            html_content = urlopen(response).read()
            # HTML 파싱
            navigator = bs4.BeautifulSoup(html_content, 'html5lib')
            # 네비게이터를 이용해 원하는 링크 리스트 가져오기
            # 헤드라인 10개
            headLineTags = navigator.find("ul", {"class": "type06_headline"})
            # 헤드라인이 존재하는지 확인
            if headLineTags is not None:
                headLineTag = headLineTags.find_all("dt")
                resultList = [item.a for item in headLineTag]
            # 비헤드라인 10개
            normalTags = navigator.find("ul", {"class": "type06"})
            # 비헤드라인이 존재하는지 확인
            if normalTags is not None:
                normalTag = normalTags.find_all("dt")
                for item in normalTag:
                    resultList.append(item.a)

            # 링크 추출 (중복 링크 포함)
            url_lists = url_lists + [item['href'] for item in resultList]

            # 중복 링크 제거
            url_lists = list(set(url_lists))
            # time.sleep(0.000001)
        # URL 출력
        for index, url_list in enumerate(url_lists):
            resultText = '[%d개] %s' % (index + 1, url_list)
            print(resultText)
        return url_lists
