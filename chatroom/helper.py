'''
Created on May 10, 2016

@author: lieyongzou
'''

from django.core.cache import cache
from django.contrib.auth.models import User
from account.models import *

# the key template in the cache
user_prefix = 'chatroom(%s)_user_'
message_prefix = 'chatroom(%s)_msg_'
room_key = 'chatroom(%d)'

def readUsersFromCache(roomId):
    '''
    A method to read a list of users in the chatroom from cache
    @param roomId: the id of the chatroom
    @return: a list of Userinfo of users in the chatroom
    '''
    global user_prefix
    it = cache.iter_keys(user_prefix % (roomId) + '*')
    
    # Iterate all the user in the it
    result = []
    for key in it:
        username = cache.get(key)
        user = User.objects.get(username__exact = username)
        ui = UserInfo.objects.get(user = user)
        result.append(ui)
    return result


def readRecentMsgFromCache(roomId, refreshTime):
    '''
    A method to read a list of message from cache since last refreshTime
    '''
    global message_prefix
    it = cache.iter_keys(message_prefix % (roomId) + '*')

    # Iterate all the message in the cache
    result = []
    for key in it:
        metadata = cache.get(key)
        if long(metadata['time']) > long(refreshTime): # the msg is newer than the last refresh time
            result.append(metadata)
    return result

def readChatroomsFromCache(chatrooms):
    '''
    A method to read a list of chatrooms sorted by how many users are in the room
    '''
    global room_key
    
    result = []
    for room in chatrooms:
        count = cache.get(room_key % (room.id))
        data = {
                'title' : room.title,
                'id' : room.id,
                'count' : count
        }
        result.append(data)
    result = sorted(result, key = lambda k : k['count'], reverse = True)
    return result
        