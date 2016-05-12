# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0005_chatroom_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='channel',
        ),
    ]
