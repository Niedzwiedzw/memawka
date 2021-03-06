# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_feed', '0002_author_facebook_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='display_name',
            field=models.CharField(default='Anon', max_length=40),
        ),
        migrations.AddField(
            model_name='author',
            name='facebook_authorized',
            field=models.BooleanField(default=False),
        ),
    ]
