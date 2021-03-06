"""Wonderland URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Load page
    url(r'^$', views.bookIndex, name = 'bookIndex'), 
    url(r'^details', views.getDetails, name = 'bookDetails'),
    url(r'^chapters', views.chapterPage, name = 'bookChapters'),
    url(r'^content', views.contentPage),

    # Action
    url(r'^search', views.search, name = 'search'),
    url(r'^getChapters', views.getChapters),
#     url(r'^getContent',)
    
]
