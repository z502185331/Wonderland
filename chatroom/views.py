from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.http.response import HttpResponse, Http404

from models import *
from helper import *

from datetime import datetime
# the global r for the redis

# the key template in the cache
user_prefix = 'chatroom(%s)_user_'
message_prefix = 'chatroom(%s)_msg_'
room_key = 'chatroom(%s)_owner_%s'
room_info_key = 'chatroom(%s)_info'

def chatIndex(request):
    '''
    A method to render the page to show the list of chatrooms
    '''
    return render(request, 'page/chatIndex.html', {})


def chatroom(request, hash):
    '''
    A method to render the page for the chatroom
    The users enter the chatroom
    '''
    global room_info_key
    info = cache.get(room_info_key % (hash))
    return render(request, 'page/chatroom.html', {'roomInfo' : info})
    
    
def getMyRooms(request):
    '''
    A method to list all my chatrooms
    '''
    chatrooms = readMyRoomsFromCache(request.user)
    return render(request, 'json/chatrooms.json', {'chatrooms':chatrooms}, content_type = 'application/json')


def getAllRooms(request):
    '''
    A method to list all the chatrooms
    '''
    chatrooms = readAllRoomsFromCache()
    return render(request, 'json/chatrooms.json', {'chatrooms':chatrooms}, content_type = 'application/json')


def createRoom(request):
    '''
    A method to create a chatroom with title
    '''
    if 'title' not in request.POST or not request.POST['title']:
        return redirect(reverse('chatIndex'))
    
    title = request.POST['title']
    user = request.user
    chatroom = Chatroom(owner = user, title = title)
    hash = chatroom.getHash()
    
#     chatroom.save()
    
    # Add chatroom to cache
    global room_key, room_info_key
    cache.set(room_key % (hash, user.username), 0, timeout = 300) # Cache count
    cache.set(room_info_key % (hash), 
              {'title' : title, 'owner' : user.username, 'hash' : hash}, timeout = 300) 
    
    return HttpResponse(hash)


def enterRoom(request):
    '''
    A method to increase the number of user in the chatroom,
    add user into the list, when user enter the chatroom
    '''
    if 'roomHash' not in request.POST or not request.POST['roomHash'] or \
            'roomOwner' not in request.POST or not request.POST['roomOwner']:
#         return redirect(reverse(chatIndex))
        raise Http404;
    
    hash = request.POST['roomHash']
    owner = request.POST['roomOwner']
    user = request.user

    # Add user to the cache, the number of user increased
    global room_key, user_prefix
    if cache.get(user_prefix % (hash) + user.username) == None:
        cache.incr(room_key % (hash, owner))
    cache.set(user_prefix % (hash) + user.username, user.username, timeout = 10)
    return HttpResponse('')


def leaveRoom(request):
    '''
    A method to decrease the number of user in the chatroom,
    remove the user in the list, when user leaves the chatroom
    '''
    if 'roomId' not in request.POST or not request.POST['roomId']:
        return redirect(reverse(chatIndex))
    
    roomId = request.POST['roomId']
    user = request.user
    print 'leave ' + roomId
    
    global room_key, user_prefix
    cache.decr(room_key % (roomId))
    cache.delete(user_prefix % (roomId) + user.username)
    return HttpResponse('')
    

def getUsers(request, roomHash):
    '''
    A method to display the user list in the chatroom
    '''
    users = readUsersFromCache(roomHash) # read users from cache
    context = {'users' : users}
    return render(request, 'json/users.json', context, content_type = 'application/json')
    
    
def sendMsg(request):
    '''
    A method to send a msg in chatroom
    '''
    if 'roomHash' not in request.POST or not request.POST['roomHash'] \
            or 'msg' not in request.POST or not request.POST['msg'] \
                or 'time' not in request.POST or not request.POST['time']:
        return redirect(reverse('chatIndex'))
    
    roomHash = request.POST['roomHash']
    msg = request.POST['msg']
    time = request.POST['time']
    user = request.user
    
    # The metadata of a msg
    metadata = {'chatroom': roomHash, 'user': user, 'msg': msg, 'time': time}
    
    # write to the cache
    global message_prefix
    cache.set(message_prefix % (roomHash) + str(hash(msg)), metadata)
    return HttpResponse('')
        

def getMsg(request, roomHash, refreshTime):
    '''
    A method to get the msg posted in the chatroom from the last refreshTime
    '''
    msgs = readRecentMsgFromCache(roomHash, refreshTime)
    context = {'roomHash' : roomHash, 'msgs' : msgs}
    user = request.user;
    
    # Refresh the ttl of user in cache
    cache.set(user_prefix % (roomHash) + user.username, user.username, timeout = 10)
    return render(request, 'json/msgs.json', context, content_type = 'application/json')
    