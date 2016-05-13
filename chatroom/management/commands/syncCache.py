from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
import re

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        rooms = cache.keys("chatroom(*)_owner_*")
        p = re.compile('chatroom\((.*?)\)_owner')
        
        for room in rooms:
            m = p.match(room)
            if m:
                hash = m.group(1)
                key = 'chatroom(%s)_user_*' % (hash)
                cache.set(room, len(cache.keys(key)))
            
        