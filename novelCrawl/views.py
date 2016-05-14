from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from crawlers.qidianCrawler import QidianCrawler
from django.http.response import HttpResponse, Http404
# Create your views here.

@login_required
def bookIndex(request):
    '''
    A method to show the index of novel page
    '''
    return render(request, 'page/search.html', {})

@login_required
def search(request):
    '''
    A method to search a keyword
    '''
    if 'keyword' not in request.GET or not request.GET['keyword'] \
            or 'type' not in request.GET or not request.GET['type'] \
                    or 'startid' not in request.GET or not request.GET['startid']:
        raise Http404
    keyword = request.GET.get('keyword').encode('utf-8')
    type = request.GET['type'].encode('utf-8')
    startid = int(request.GET['startid'])
    
    crawler = QidianCrawler()
    books = crawler.search(keyword, startid)
    context = {'books' : books, 'startid' : startid, 'keyword' : keyword}
    return render(request, 'json/books.json', context, content_type = 'application/json')
    