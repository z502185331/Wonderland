# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0006_remove_message_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='hash',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
