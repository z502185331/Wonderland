from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        rooms = cache.keys("chatroom(*)")
        
        for room in rooms:
            cache.set(room, len(cache.keys(room + '_user*')))
            
        