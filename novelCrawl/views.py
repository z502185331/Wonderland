from django.shortcuts import render

# Create your views here.

def novelIndex(request):
    '''
    A method to show the index of novel page
    '''
    return render(request, 'page/novelIndex.html', {})