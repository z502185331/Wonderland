'''
Created on May 10, 2016

@author: lieyongzou
'''

from django.core.cache import cache
from django.contrib.auth.models import User
from account.models import UserInfo
from chatroom.models import Chatroom
import re

# the key template in the cache
user_prefix = 'chatroom(%s)_user_'
message_prefix = 'chatroom(%s)_msg_'
room_key = 'chatroom(%d)'
room_info_key = 'chatroom(%s)_info'

def readUsersFromCache(hash):
    '''
    A method to read a list of users in the chatroom from cache
    @param roomId: the id of the chatroom
    @return: a list of Userinfo of users in the chatroom
    '''
    global user_prefix
    it = cache.iter_keys(user_prefix % (hash) + '*')
    
    # Iterate all the user in the it
    result = []
    for key in it:
        username = cache.get(key)
        user = User.objects.get(username__exact = username)
        ui = UserInfo.objects.get(user = user)
        result.append(ui)
    return result


def readRecentMsgFromCache(hash, refreshTime):
    '''
    A method to read a list of message from cache since last refreshTime
    '''
    global message_prefix
    it = cache.iter_keys(message_prefix % (hash) + '*')

    # Iterate all the message in the cache
    result = []
    for key in it:
        metadata = cache.get(key)
        if long(metadata['time']) > long(refreshTime): # the msg is newer than the last refresh time
            result.append(metadata)
    return result

def readAllRoomsFromCache():
    '''
    A method to read a list of chatrooms sorted by how many users are in the room
    '''
    global room_info_key
    result = []
    it = cache.keys('chatroom(*)_owner_*')
    pattern = re.compile('chatroom\((.*?)\)')
    
    for key in it:
        m = pattern.match(key)
        if m:
            hash = m.group(1)
            count = cache.get(key)
            roominfo = cache.get(room_info_key % (hash))
            data = {
                'title' : roominfo['title'],
                'hash' : hash,
                'owner' : roominfo['owner'],
                'count' : count
            }
            result.append(data)
    result = sorted(result, key = lambda k : k['count'], reverse = True)
    return result
        
def readMyRoomsFromCache(user):
    '''
    A method to read a list of chatrooms owned by user and 
    sorted by how many users are in the room
    '''
    result = []
    it = cache.keys('chatroom(*)_owner_*')
    pattern = re.compile('chatroom\((.*?)\)_owner_(.*)')
    
    for key in it:
        m = pattern.match(key)
        if m:
            hash = m.group(1)
            name = m.group(2)
            count = cache.get(key)
            
            # Skip the rooms owned by other users
            if user.username != name:
                continue
            room = Chatroom.objects.get(hash = hash)
            data = {
                'title' : room.title,
                'hash' : hash,
                'count' : count,
                'owner' : room.owner,
                'count' : count
            }
            result.append(data)
    result = sorted(result, key = lambda k : k['count'], reverse = True)
    return result

        