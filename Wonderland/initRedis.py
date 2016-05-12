'''
Created on May 8, 2016

@author: lieyongzou
'''

from chatroom.models import Chatroom
from django.core.cache import cache

class StartupMiddleware(object):
    def __init__(self):
        print 'init redis'
        chatRooms = Chatroom.objects.all().order_by('-publishTime')
        for room in chatRooms:
            key = 'chatroom(%d)' % (room.id)
            if cache.get(key) == None:
                cache.set(key, 0, timeout = None)
            
        
        
    