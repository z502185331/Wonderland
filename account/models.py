from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name = 'info')
    friend = models.ManyToManyField(User, related_name = 'friends')
    icon = models.ImageField(upload_to = 'userIcon', default = '/static/media/userIcon/user_pic.jpeg')
