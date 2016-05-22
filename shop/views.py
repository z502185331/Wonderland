from django.shortcuts import render

# Create your views here.

def shopIndex(request):
    return render(request, 'page/shopIndex.html', {})