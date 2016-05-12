# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatroom', '0004_auto_20160508_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chatroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('publishTime', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(related_name='chatrooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postTime', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=100)),
                ('channel', models.ForeignKey(related_name='messages', to='chatroom.Chatroom', null=True)),
                ('receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('sender', models.ForeignKey(related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
