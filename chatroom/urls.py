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
    url(r'^chatIndex$', views.chatIndex, name = 'chatIndex'),
    url(r'^chatroom/(?P<roomId>\d+)$', views.chatroom, name = 'chatroom'),
    
    # Action
    url(r'^newRoom/$', views.createRoom, name = 'newRoom'),
    url(r'^chatroom/leaveRoom/$', views.leaveRoom, name = 'leaveRoom'),
    url(r'^chatroom/enterRoom/$', views.enterRoom, name = 'enterRoom'),
    url(r'^chatroom/sendMsg/$', views.sendMsg, name = 'sendMsg'),
    
    # AJAX
    url(r'^myChatList/$', views.getMyRooms, name = 'myChatList'),
    url(r'^allChatList/$', views.getAllRooms, name = 'allChatList'),
    url(r'^chatroom/getUsers/(?P<roomId>\d+)$', views.getUsers, name = 'getUsers'),
    url(r'^chatroom/getMsg/(?P<roomId>\d+)/(?P<refreshTime>\d+)$', views.getMsg, name = 'getMsg'),
    
    
]
