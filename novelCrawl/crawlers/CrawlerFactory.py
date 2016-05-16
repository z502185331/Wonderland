#!/usr/bin/env python
#-*-coding:utf-8 -*-

from QidianCrawler import QidianCrawler
from QuanbenCrawler import QuanbenCrawler


class CrawlerFactory:
    
    def __init__(self):
        self.crawler_dict = {
            '起点中文网' : QidianCrawler(),
            '全本小说网' : QuanbenCrawler()
        }
    
    def getCrawler(self, source):
        return self.crawler_dict[source]
    
if __name__ == '__main__' :
    c = CrawlerFactory()
    print c.getCrawler('起点中文网')