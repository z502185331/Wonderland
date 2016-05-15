#!/usr/bin/env python
#-*-coding:utf-8 -*-

from lxml import html
import requests
import json
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import re
import uniout

'''
Data format:
    (1) Search result:[{'title':.., 'author':..., 'cover':..., 'description':..., 'bookurl':...}]
    (2) Detailed result: {{'title':.., 'author':..., 'cover':..., 'description':..., 'chapter':..., 'metadata': {......}}
'''


search_template = 'http://sosu.qidian.com/searchresult.aspx?keyword=%s'
detail_url_template = 'http://www.qidian.com/Book/%s.aspx'

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
            'searchtype' : '综合',
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
    
    
    def search(self, keyword, startid):
        '''
        A method to search a keyword and return a list of related books
        '''
        result = []
        self.searchRequest['keyword'] = keyword
        self.searchRequest['start'] = startid * 10
        pattern = re.compile('http://www.qidian.com/Book/(.*?).aspx') # Reg to extract the bookid
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
            url = book['bookurl'].encode('utf-8')
            m = pattern.match(url)
            if m:
                info['bookurl'] = m.group(1)
            else:
                info['bookurl'] = url
            result.append(info)
        return result
    
    
    def getDetails(self, link):
        '''
        A method to get details information about the book
        '''
        global detail_url_template
        r = requests.get(detail_url_template % link)
        tree = html.fromstring(r.content)
        title = tree.xpath('//h1[@itemprop="name"]/text()')[0]  # title of book
        author = tree.xpath('//span[@itemprop="author"]//span[@itemprop="name"]/text()')[0] # author of book
        description = tree.xpath('//span[@itemprop="description"]/text()') # detailed description of book
        description = ''.join(description)
        cover = tree.xpath('//div[@class="book_pic"]//img[@itemprop="image"]/@src')[0] # the src of book cover
        chapters = tree.xpath('//div[@class="opt"]//a[@itemprop="url"]/@href')[0] # the url to the chapter information
        
        # Get metatdata for the book, which is customized
        labels = tree.xpath('//div[@class="other"]//div[@class="labels"]//a[@target="_blank"]/text()') # get the labels of the book
        metadata = {'labels' : labels}
        
        # pack all the detailed information
        result = {}
        result['title'] = title
        result['author'] = author
        result['description'] = description
        result['cover'] = cover
        result['chapters'] = chapters
        result['metadata'] = metadata
        return result
    


if __name__ == '__main__':
    c = QidianCrawler()
    print c.getDetails('http://www.qidian.com/Book/2418955.aspx')
#     r = requests.get('http://www.qidian.com/Book/2217895.aspx')
#     print r.content
#     tree = html.fromstring(r.content)
#     boxdiv = tree.xpath('//h1[@itemprop="name"]/text()')
#     print boxdiv
