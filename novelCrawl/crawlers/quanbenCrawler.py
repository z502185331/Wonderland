#!/usr/bin/env python
#-*-coding:utf-8 -*-

'''
Data source : 全本小说网 <http://big5.quanben5.com>
Data format:
    (1) Search result:[{'title':.., 'author':..., 'cover':..., 'description':..., 'bookurl':...}]
    (2) Detailed result: {{'title':.., 'author':..., 'cover':..., 'description':..., 'chapter':..., 'metadata': {......}}
'''
import requests
from lxml.html import fromstring
import uniout
import re

search_url_template = 'http://big5.quanben5.com/index.php?c=book&a=search&keywords=%s'
cover_url_template = 'http://big5.quanben5.com%s'
book_url_pattern = '/n/(.*?)/'



class QuanbenCrawler:
    
    def search(self, keyword, startid):
        '''
        A method to search related books by keyword
        '''
        result = []
        if startid != 0:
            return result
        
        global search_url_template, book_url_pattern, cover_url_template
        r = requests.get(search_url_template % keyword)
        tree = fromstring(r.content)
        
        books = tree.xpath('//div[@class="content"]/div[@class="pic_txt_list"]')
        for book in books:
            info = {}
            info['cover'] = cover_url_template % book.xpath('div[@class="pic"]/img/@src')[0]
            info['title'] = ''.join(book.xpath('h3/a/span/descendant-or-self::text()')) # Join the <span> and <b>
            info['author'] = book.xpath('p[@class="info"]/span/text()')[0]
            info['bookurl'] = self.extract(book_url_pattern, book.xpath('h3/a/@href')[0])
            
            des = book.xpath('p[@class="description"]/text()')
            if des:
                info['description'] = ' '.join((book.xpath('p[@class="description"]/text()')[0]).split())
            else:
                info['description'] = ''
            result.append(info)
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
    c = QuanbenCrawler()
    print c.search('神奇', 0)
#     print c.extract('/n/(.*?)/', '/n/anyingjie/')
        
        