# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20160510_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='icon',
            field=models.ImageField(default=b'/static/media/userIcon/user_pic.jpeg', upload_to=b'userIcon'),
        ),
    ]
