from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponse, Http404
from crawlers.CrawlerFactory import CrawlerFactory
import json

# Create your views here

factory = CrawlerFactory()

@login_required
def bookIndex(request):
    '''
    A method to show the index of novel page
    '''
    global factory
    sources = factory.crawler_dict.keys()
    return render(request, 'page/search.html', {'sources' : sources})

@login_required
def search(request):
    '''
    A method to search a keyword
    '''
    if 'keyword' not in request.GET or not request.GET['keyword'] \
            or 'source' not in request.GET or not request.GET['source'] \
                    or 'startid' not in request.GET or not request.GET['startid']:
        raise Http404
    keyword = request.GET.get('keyword').encode('utf-8')
    source = request.GET['source'].encode('utf-8')
    startid = int(request.GET['startid'])
    
    global factory
    crawler = factory.getCrawler(source)
    books = crawler.search(keyword, startid)
    context = {'books' : books, 'startid' : startid, 'keyword' : keyword, 'source' : source}
    return render(request, 'json/books.json', context, content_type = 'application/json')


@login_required
def getDetails(request):
    '''
    A method to show the details of a book
    '''
    if 'source' not in request.GET or not request.GET['source'] \
            or 'url' not in request.GET or not request.GET['url']:
        raise Http404
    source = request.GET['source'].encode('utf-8')
    url = request.GET['url']
    
    global factory
    crawler = factory.getCrawler(source)
    info = crawler.getDetails(url)
    return render(request, 'page/bookdetails.html', {'info' : info, 'source' : source})


@login_required
def chapterPage(request):
    '''
    A method to open the page for the chapters
    '''
    if 'source' not in request.GET or not request.GET['source'] \
            or 'url' not in request.GET or not request.GET['url']:
        raise Http404
    url = request.GET['url']
    source = request.GET['source']
    return render(request, 'page/chapters.html', {'url' : url, 'source' : source})


@login_required
def getChapters(request):
    '''
    A method to get the chapter info from book
    '''
    if 'url' not in request.GET or not request.GET['url'] \
            or 'source' not in request.GET or not request.GET['source']:
        raise Http404
    url = request.GET['url']
    source = request.GET['source'].encode('utf-8')
    print url
    
    
    global factory
    crawler = factory.getCrawler(source)
    info = crawler.getChapters(url)
    print info
    return HttpResponse(json.dumps(info), content_type = 'application/json')


@login_required
def contentPage(request):
    '''
    A method to open the content page
    '''
    if 'url' not in request.GET or not request.GET['url'] \
            or 'source' not in request.GET or not request.GET['source']:
        raise Http404
    url = request.GET['url']
    source = request.GET['source'].encode('utf-8')
    context = {}
    
    global factory
    crawler = factory.getCrawler(source)
    info = crawler.getContent(url)
    context['info'] = info
    
    neighbors = crawler.getNeighbors(url)
    if 'pre_chapter' in neighbors:
        context['pre_chapter'] = neighbors['pre_chapter']
    if 'next_chapter' in neighbors:
        context['next_chapter'] = neighbors['next_chapter']
    
    return render(request, 'page/bookContent.html', context)

# @login_required
# def getContent(request):
    
    