from django.db import models
from koparka_memow.models import Author as AuthorRaw
from koparka_memow.models import GroupPost as GroupPostRaw


class Author(models.Model):
    id = models.IntegerField(verbose_name='Facebook user ID', unique=True, primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Facebook name')

    @property
    def posts(self):
        return GroupPost.objects.filter(author__id=self.id)

    @classmethod
    def create_from_raw(cls, raw_author: AuthorRaw):
        return cls.objects.create(**raw_author.__dict__)


class GroupPost(models.Model):
    id = models.IntegerField(verbose_name='Facebook post ID', unique=True, primary_key=True)
    creation = models.DateTimeField(verbose_name="Facebook post creation date")
    author = models.ForeignKey(Author, verbose_name='Facebook post Author', related_name='author')
    message = models.TextField(verbose_name='Facebook post message')
    reaction_count = models.IntegerField(verbose_name='Number of likes')
    image_url = models.CharField(max_length=300)

    date_discovered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def create_from_raw(cls, raw_group_post: GroupPostRaw):
        return cls.objects.create(**raw_group_post.__dict__)



