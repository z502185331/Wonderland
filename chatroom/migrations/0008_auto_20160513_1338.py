# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0007_chatroom_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='hash',
            field=models.CharField(max_length=30),
        ),
    ]
