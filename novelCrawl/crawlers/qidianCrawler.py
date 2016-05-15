#!/usr/bin/env python
#-*-coding:utf-8 -*-

from lxml.html import fromstring
import requests
import json
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import re
import uniout
from django.template.defaultfilters import title

'''
Data format:
    (1) Search result:[{'title':.., 'author':..., 'cover':..., 'description':..., 'bookurl':...}]
    (2) Detailed result: {{'title':.., 'author':..., 'cover':..., 'description':..., 'chapter':..., 'metadata': {......}}
'''


search_template = 'http://sosu.qidian.com/searchresult.aspx?keyword=%s'
detail_url_template = 'http://www.qidian.com/Book/%s.aspx'
detail_url_pattern = 'http://www.qidian.com/Book/(.*?).aspx'
chapter_url_template = 'http://read.qidian.com/BookReader/%s.aspx'
chapter_url_pattern = 'http://read.qidian.com/BookReader/(.*?).aspx'
content_url_pattern = 'http://read.qidian.com/BookReader/.*?,(.*?).aspx'

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
        global detail_url_pattern
        result = []
        self.searchRequest['keyword'] = keyword
        self.searchRequest['start'] = startid * 10
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
            info['bookurl'] = self.extract(detail_url_pattern, book['bookurl'].encode('utf-8'))
            result.append(info)
        return result
    
    
    def getDetails(self, link):
        '''
        A method to get details information about the book
        '''
        global detail_url_template, chapter_url_pattern
        
        r = requests.get(detail_url_template % link)
        tree = fromstring(r.content)
        
        # Get basic detailed information of a book
        title = tree.xpath('//h1[@itemprop="name"]/text()')[0]  # title of book
        author = tree.xpath('//span[@itemprop="author"]//span[@itemprop="name"]/text()')[0] # author of book
        description = tree.xpath('//span[@itemprop="description"]/text()') # detailed description of book
        description = ''.join(description)
        cover = tree.xpath('//div[@class="book_pic"]//img[@itemprop="image"]/@src')[0] # the src of book cover
        chapters = self.extract(chapter_url_pattern, 
                                tree.xpath('//div[@class="opt"]//a[@itemprop="url"]/@href')[0]) # the url to the chapter information
        
        
        # Get metatdata for the book, which is customized
        labels = tree.xpath('//div[@class="other"]//div[@class="labels"]//a[@target="_blank"]/text()') # get the labels of the book
        labels = ','.join(labels)
        total_click = tree.xpath('//div[@class="intro"]/div[@class="data"]/table/tr/td/text()')[1]
        total_recommation = tree.xpath('//div[@class="intro"]/div[@class="data"]/table/tr/td/text()')[5]
        total_word = tree.xpath('//div[@class="intro"]/div[@class="data"]/table/tr/td/text()')[7]
        metadata = {'标签' : labels, '总点击' : total_click, "总推荐" : total_recommation, "总字数" : total_word}
        
        # pack all the detailed information
        result = {}
        result['title'] = title
        result['author'] = author
        result['description'] = description
        result['cover'] = cover
        result['chapters'] = chapters
        result['metadata'] = metadata
        return result
    
    def getChapters(self, link):
        '''
        A method to get the chapter list
        '''
        result = {}
        bookid = link
        global chapter_url_template, content_url_pattern
        link = chapter_url_template % link
        r = requests.get(link)
        tree = fromstring(r.content)
        
        # Get the basic information and chapters from a book
        title = tree.xpath('//div[@class="booktitle"]/h1/text()')[0]
        author = tree.xpath('//div[@class="booktitle"]/span/a/text()')[0]
        subtitles = tree.xpath('//div[@id="content"]/div[@class="box_title"]/div[@class="title"]/b/text()')
        chapters = tree.xpath('//div[@id="content"]/div[@class="box_cont"]/div[@class="list"]')
        
        # Clean the subtitles:
        cleaned_st = []
        for i in range(len(subtitles)):
            if subtitles[i] == ']':
                continue
            if subtitles[i][-1:] == '[':
                cleaned_st.append(subtitles[i] + 'VIP]')
            elif subtitles[i].strip():
                cleaned_st.append(subtitles[i])

        # Arrange the subchapters to its chapters
        chapterlist = []
        for i in range(len(chapters)):
            package = {}
            package['subtitle'] = cleaned_st[i]
            package['chapters'] = []
            clist = chapters[i].xpath('ul/li/a/span/text()')
            if not clist:  # For VIP chapters
                clist = chapters[i].xpath('ul/li/a/text()')
                
            urllist = chapters[i].xpath('ul/li/a/@href')
            for j in range(len(clist)):
                package['chapters'].append({'chapter': clist[j], 
                                            'url': self.extract(content_url_pattern, urllist[j])
                                            })
                    
                
            chapterlist.append(package)
        
        # pack the data
        result['title'] = title
        result['author'] = author
        result['bookid'] = bookid
        result['chapters'] = chapterlist
        return result
    
        
    def extract(self, pattern, target):
        '''
        A method to extract information by using regix
        '''
        result = None
        p = re.compile(pattern)
        m = p.match(target)
        if m:
            result = m.group(1)
        else:
            result = target
        return result

if __name__ == '__main__':
    c = QidianCrawler()
#     print c.getDetails('2217895')
    print c.getChapters('Y10wqB5vJdk1')
    
    
