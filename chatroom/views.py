from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.http.response import HttpResponse

from models import *
from helper import *

from datetime import datetime
# the global r for the redis

# the key template in the cache
user_prefix = 'chatroom(%s)_user_'
message_prefix = 'chatroom(%s)_msg_'
room_key = 'chatroom(%s)'

def chatIndex(request):
    '''
    A method to render the page to show the list of chatrooms
    '''
    return render(request, 'page/chatIndex.html', {})


def chatroom(request, roomId):
    '''
    A method to render the page for the chatroom
    The users enter the chatroom
    '''
    cr = Chatroom.objects.get(id = roomId)
    return render(request, 'page/chatroom.html', {'chatroom' : cr})
    
    
def getMyRooms(request):
    '''
    A method to list all my chatrooms
    '''
    chatrooms = readChatroomsFromCache(Chatroom.objects.filter(owner = request.user))
    return render(request, 'json/chatrooms.json', {'chatrooms':chatrooms}, content_type = 'application/json')


def getAllRooms(request):
    '''
    A method to list all the chatrooms
    '''
    chatrooms = readChatroomsFromCache(Chatroom.objects.all())
    return render(request, 'json/chatrooms.json', {'chatrooms':chatrooms}, content_type = 'application/json')

def createRoom(request):
    '''
    A method to create a chatroom with title
    '''
    if 'title' not in request.POST or not request.POST['title']:
        return redirect(reverse('chatIndex'))
    
    title = request.POST['title']
    chatroom = Chatroom(owner = request.user, title = title)
    chatroom.save()
    
    # Add chatroom to cache
    global room_key
    cache.set(room_key % (chatroom.id), 0, timeout = None)
    
    return redirect(reverse('chatIndex'))


def enterRoom(request):
    '''
    A method to increase the number of user in the chatroom,
    add user into the list, when user enter the chatroom
    '''
    if 'roomId' not in request.POST or not request.POST['roomId']:
        return redirect(reverse(chatIndex))
    
    roomId = request.POST['roomId']
    user = request.user
    
    print 'enter' + roomId
    # Add user to the cache, the number of user increased
    global room_key, user_prefix
    cache.incr(room_key % (roomId))
    cache.set(user_prefix % (roomId) + user.username, user.username, timeout = 10)
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
    

def getUsers(request, roomId):
    '''
    A method to display the user list in the chatroom
    '''
    users = readUsersFromCache(roomId) # read users from cache
    context = {'roomId' : roomId, 'users' : users}
    return render(request, 'json/users.json', context, content_type = 'application/json')
    
    
def sendMsg(request):
    '''
    A method to send a msg in chatroom
    '''
    if 'roomId' not in request.POST or not request.POST['roomId'] \
            or 'msg' not in request.POST or not request.POST['msg'] \
                or 'time' not in request.POST or not request.POST['time']:
        return redirect(reverse('chatIndex'))
    
    roomId = request.POST['roomId']
    msg = request.POST['msg']
    time = request.POST['time']
    user = request.user
    
    # The metadata of a msg
    metadata = {'chatroom': roomId, 'user': user, 'msg': msg, 'time': time}
    
    # write to the cache
    global message_prefix
    cache.set(message_prefix % (roomId) + str(hash(msg)), metadata)
    return HttpResponse('')
        

def getMsg(request, roomId, refreshTime):
    '''
    A method to get the msg posted in the chatroom from the last refreshTime
    '''
    msgs = readRecentMsgFromCache(roomId, refreshTime)
    context = {'roomId' : roomId, 'msgs' : msgs}
    user = request.user;
    
    # Refresh the ttl of user in cache
    cache.set(user_prefix % (roomId) + user.username, user.username, timeout = 10)
    return render(request, 'json/msgs.json', context, content_type = 'application/json')
    