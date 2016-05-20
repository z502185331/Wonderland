#!/usr/bin/env python
#-*-coding:utf-8 -*-

'''
Data source : 全本小说网 <http://big5.quanben5.com>
Data format:
    (1) Search result:[{'title':.., 'author':..., 'cover':..., 'description':..., 'bookurl':...}]
    (2) Detailed result: {{'title':.., 'author':..., 'cover':..., 'description':..., 'chapters':..., 'metadata': {......}}
    (3) Chapters result: {'title':..., 'author':..., 'chapters': [{'subtitle':..., 'chapters':{'chapter':..., 'url':...}}]}
    (4) Content result: {'title':..., 'chapter':..., 'content': ...}
'''


import requests
from lxml.html import fromstring
import uniout
import re
from django.template.defaultfilters import title
from langconv import *

search_url_template = 'http://big5.quanben5.com/index.php?c=book&a=search&keywords=%s'
resource_url_template = 'http://big5.quanben5.com%s'
book_url_template = 'http://big5.quanben5.com/n/%s/'
book_url_pattern = '/n/(.*?)/(.*?).html'

content_url_template = '/wonderland/book/content?url=%s&source=全本小说网'




class QuanbenCrawler:
    
    def search(self, keyword, startid):
        '''
        A method to search related books by keyword
        '''
        result = []
        if startid != 0:
            return result
        
        global search_url_template, resource_url_template
        r = requests.get(search_url_template % keyword)
        tree = fromstring(r.content)
        
        books = tree.xpath('//div[@class="content"]/div[@class="pic_txt_list"]')
        for book in books:
            info = {}
            info['cover'] = resource_url_template % self.locateData(book, 'div[@class="pic"]/img/@src', 0)
            info['title'] = ''.join(book.xpath('h3/a/span/descendant-or-self::text()')) # Join the <span> and <b>
            info['author'] = self.locateData(book, 'p[@class="info"]/span/text()', 0)
            info['bookurl'] = self.extract('/n/(.*?)/', self.locateData(book, 'h3/a/@href', 0), 1)
            info['description'] = ' '.join((self.locateData(book, 'p[@class="description"]/text()', 0)).split())
            result.append(info)
        return result
    
    
    def getDetails(self, link):
        '''
        A method to get details information about the book
        '''
        global book_url_template, resource_url_template
        link = book_url_template % link
        r = requests.get(link)
        tree = fromstring(r.content)
        info = {}
        
        info['title'] = self.locateData(tree, '//div[@class="pic_txt_list"]/h3/span/text()', 0)
        info['author'] = self.locateData(tree, '//div[@class="pic_txt_list"]/p[@class="info"]/span/text()', 0)
        info['cover'] = resource_url_template % \
                                self.locateData(tree, '//div[@class="pic_txt_list"]/div[@class="pic"]/img/@src', 0)
        info['description'] = self.locateData(tree, '//div[@class="description"]/p/text()', 0)
        info['chapters'] = self.locateData(tree, '//div[@class="tool_button"]/a/@href', 0)
        
        # metadata
        metadata = {}
        metadata['类别'] = self.locateData(tree, '//div[@class="pic_txt_list"]/p[@class="info"]/span/text()', 1)
        metadata['状态'] = self.locateData(tree, '//div[@class="pic_txt_list"]/p[@class="info"]/span/text()', 2)
        info['metadata'] = metadata
        return info
        

    def getChapters(self, link):
        '''
        A method to get the chapter list
        '''
        global resource_url_template, content_url_template, book_url_pattern
        link = resource_url_template % link

        info = {}
        r = requests.get(link)
        tree = fromstring(r.content)
        
        info['title'] = self.locateData(tree, '//div[@class="pic_txt_list"]/h3/span/text()', 0)
        info['author'] = self.locateData(tree, '//div[@class="pic_txt_list"]/p[@class="info"]/span/text()', 0)
        info['chapters'] = []
        
        
        boxes = tree.xpath('//div[@class="row"]//div[@class="box"]')
        for box in boxes[2:]:
            package = {}
            package['subtitle'] = self.locateData(box, 'h2[@class="title"]/span/text()', 0)
            package['chapters'] = []
            clist = box.xpath('ul[@class="list"]/li') # get chapters in the section
            for chapter in clist:
                item = {}
                item['chapter'] = self.locateData(chapter, 'a/span/text()', 0)
                item['url'] = content_url_template % self.locateData(chapter, 'a/@href', 0)
                package['chapters'].append(item)
            
            info['chapters'].append(package)
        return info
    
    
    def getNeighbors(self, link):
        '''
        A method to get the url of previous chapter and next chapter
        '''
        result = []
        global book_url_pattern, content_url_template
        bookid = self.extract(book_url_pattern, link, 1)
        chapterid = int(self.extract(book_url_pattern, link, 2))
        
        result.append(content_url_template % ('/n/%s/%d.html' % (bookid, chapterid - 1)))
        result.append(content_url_template % ('/n/%s/%d.html' % (bookid, chapterid + 1)))
        return result
    
    
    def getContent(self, link):
        '''
        A method to get the content of the chapters
        '''
        global resource_url_template
        link = resource_url_template % link
        r = requests.get(link)
        tree = fromstring(r.content)
        info = {}
        
        info['title'] = self.locateData(tree, '//div[@class="row"]/span/text()', 0)
        info['chapter'] = self.locateData(tree, '//div[@class="content"]/h1[@class="title1"]/text()', 0)
        info['content'] = '<p>' + '</p><p>'.join(tree.xpath('//div[@id="content"]/p/text()'))
        return info
    
    
    def locateData(self, tree, path, index):
        '''
        Locate the data by xpath, clean the data and return it
        '''
        l = tree.xpath(path)
        if l:
            return l[index]
        else:
            return ''
    
    def extract(self, pattern, target, index):
        '''
        A method to extract information by using regix
        '''
        result = None
        p = re.compile(pattern)
        m = p.match(target)
        if m:
            result = m.group(index)
        else:
            result = target
        return result
    
if __name__ == '__main__':
    c = QuanbenCrawler()
#     c.search('神奇', 0)
#     print c.getDetails('doushentianxia')
#     c.getChapters('/n/anyingjie/xiaoshuo.html')
#     c.getContent('/n/anheiwangzuo/26125.html')
    print c.getNeighbors('/n/anyingjie/19209.html')
        
        