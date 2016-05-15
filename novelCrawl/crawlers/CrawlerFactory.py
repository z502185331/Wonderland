#!/usr/bin/env python
#-*-coding:utf-8 -*-

from qidianCrawler import QidianCrawler

crawler_dict = {'起点中文网' : QidianCrawler()}

class CrawlerFactory:
    
    def getCrawler(self, source):
        global crawler_dict
        return crawler_dict[source]
    
if __name__ == '__main__' :
    c = CrawlerFactory()
    print c.getCrawler('起点中文网')