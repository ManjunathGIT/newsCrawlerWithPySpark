#!/usr/bin/python
# -*- coding: utf-8 -*-


class Information:
    def __init__(self, url="", high="", low="", title="", content="", click_num=0, aType="", kGroup=0, pDate="", meta=""):
        self.url = url
        self.high = high
        self.low = low
        self.title = title
        self.content = content
        self.click_num = click_num
        self.aType = aType
        self.kGroup = kGroup
        self.pDate = pDate
        self.meta = meta

    @property
    def url(self):
        return self.__url

    @property
    def high(self):
        return self.__high

    @property
    def low(self):
        return self.__low

    @property
    def title(self):
        return self.__title

    @property
    def content(self):
        return self.__content

    @property
    def click_num(self):
        return self.__click_num

    @property
    def aType(self):
        return self.__aType

    @property
    def kGroup(self):
        return self.__kGroup

    @property
    def pDate(self):
        return self.__pDate

    @property
    def meta(self):
        return self.__meta

    def __str__(self):
        return "Infomation [high=" + str(self.high) + " url=" + str(self.url) + ", tag=" + str(self.low) + ", title=" + str(self.title) + \
            ", pDate=" + str(self.pDate) + "]"
