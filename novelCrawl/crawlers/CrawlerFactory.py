#!/usr/bin/env python
#-*-coding:utf-8 -*-

from qidianCrawler import QidianCrawler
from quanbenCrawler import QuanbenCrawler

crawler_dict = {'起点中文网' : QidianCrawler(),
                '全本小说网' : QuanbenCrawler()}

class CrawlerFactory:
    
    def getCrawler(self, source):
        global crawler_dict
        return crawler_dict[source]
    
if __name__ == '__main__' :
    c = CrawlerFactory()
    print c.getCrawler('起点中文网')