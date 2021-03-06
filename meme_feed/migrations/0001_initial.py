# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_id', models.CharField(max_length=200, unique=True, verbose_name='Facebook user ID')),
                ('name', models.CharField(max_length=200, verbose_name='Facebook name')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_id', models.CharField(max_length=200, unique=True, verbose_name='Facebook post ID')),
                ('creation', models.DateTimeField(verbose_name='Facebook post creation date')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Facebook post message')),
                ('reaction_count', models.IntegerField(verbose_name='Number of likes')),
                ('image_url', models.CharField(blank=True, max_length=300, null=True)),
                ('date_discovered', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='meme_feed.Author', verbose_name='Facebook post Author')),
            ],
        ),
    ]
