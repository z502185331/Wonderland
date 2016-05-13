from django.db import models
from django.contrib.auth.models import User
import hashlib

# Create your models here.
class Chatroom(models.Model):
    owner = models.ForeignKey(User, related_name = 'chatrooms')
    title = models.CharField(max_length = 20)
    publishTime = models.DateTimeField(auto_now = True)
    hash = models.CharField(max_length = 30)
    
    def getHash(self):
        return hashlib.md5(self.owner.username + ":" + self.title + ":" + str(self.publishTime)).hexdigest()
    
    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(self.owner.username + ":" + self.title + ":" + str(self.publishTime)).hexdigest()
        super(Chatroom, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.owner.username + ":" + self.title
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name = 'messages')
    receiver = models.ForeignKey(User, null = True)
    postTime = models.DateTimeField(auto_now_add = True)
    content = models.CharField(max_length = 100)