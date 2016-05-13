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
            # Init the count
            key_count = 'chatroom(%s)_owner_%s' % (room.hash, room.owner.username) 
            if cache.get(key_count) == None:
                cache.set(key_count, 0, timeout = None)
                
            # Init the info
            key_info = 'chatroom(%s)_info' % (room.hash)
            if cache.get(key_info) == None:
                cache.set(key_info,
                          {'title' : room.title, 'owner' : room.owner.username, 'hash' : room.hash}, timeout = None)
        
    