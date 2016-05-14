#!/usr/bin/env python
#-*-coding:utf-8 -*-

from lxml import html
import requests
import json
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import uniout

'''
Data format:
    (1) Search result:[{'title':.., 'author':..., 'cover':..., 'description':..., 'bookurl':...}]
'''


search_template = 'http://sosu.qidian.com/searchresult.aspx?keyword=%s'

class QidianCrawler():
    
    def __init__(self):
        self.searchRequest = {
            'method' : 'Search',
            'keyword' : '',
            'range' : '',
            'ranker' : '',
            'n' : 10,
            'start' : '',
            'internalsiteid' : '',
            'categoryid' : '',
            'action_status' : '',
            'authortagid' : '',
            'sign_status' : '',
            'pricetypeid' : '',
            'rpid' : 10,
            'groupbyparams' : '',
            'impression' : '',
            'roleinfo' : '',
            'searchtype' : '',
            'timespan' : '',
            'noec' : ''
        }
        
        self.header = {
            'Host' : 'sosu.qidian.com',
            'Connection' : 'keep-alive',
            'Cache-Control' : 'max-age=0',
            'Accept' : 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With' : 'XMLHttpRequest',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Referer': 'http://sosu.qidian.com/searchresult.aspx?keyword=%E6%9A%97%E9%BB%91',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Cookie' : 'pgv_pvi=9399897088; pgv_si=s3466885120; stat_gid=7978187131; stat_sessid=33273497761; ASP.NET_SessionId=bd2qbd45vln0kg55bws2t0nj; stat_id24=0,-1,noimg; us=X; beacon_visit_count=3; refsite=-1'
        }
    
    
    def search(self, keyword):
        '''
        A method to search a keyword and return a list of related books
        '''
        result = []
        self.searchRequest['keyword'] = keyword
        r = requests.get(
            url = 'http://sosu.qidian.com/ajax/search.ashx',
            params = self.searchRequest,
            headers = self.header
        )
        response = r.json()
        books = response['Data']['search_response']['books']
        for book in books:
            info = {}
            info['title'] = book['bookname'].encode('utf-8')
            info['author'] = book['authorname'].encode('utf-8')
            info['description'] = book['description'].encode('utf-8')
            info['cover'] = book['coverurl'].encode('utf-8')
            info['bookurl'] = book['bookurl'].encode('utf-8')
            result.append(info)
        return result
        


if __name__ == '__main__':
    c = QidianCrawler()
    print c.search('暗黑')
    
