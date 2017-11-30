from django.db import models
from django.utils.safestring import mark_safe

from koparka_memow.models import Author as AuthorRaw
from koparka_memow.models import GroupPost as GroupPostRaw


class Author(models.Model):
    facebook_id = models.CharField(verbose_name='Facebook user ID', unique=True, max_length=200)
    name = models.CharField(max_length=200, verbose_name='Facebook name')

    @property
    def posts(self):
        return GroupPost.objects.filter(author__id=self.id)

    @classmethod
    def create_from_raw(cls, raw_author: AuthorRaw):
        return cls.objects.get_or_create(**raw_author.__dict__)

    def __str__(self):
        return f'[{self.facebook_id}] {self.name}'

    def __eq__(self, other) -> bool:
        return self.facebook_id == other.facebook_id and self.id == other.id


class GroupPost(models.Model):
    facebook_id = models.CharField(verbose_name='Facebook post ID', unique=True, max_length=200)
    creation = models.DateTimeField(verbose_name="Facebook post creation date", )
    author = models.ForeignKey(Author, verbose_name='Facebook post Author', related_name='author')
    message = models.TextField(verbose_name='Facebook post message', blank=True, null=True)
    reaction_count = models.IntegerField(verbose_name='Number of likes')
    image_url = models.CharField(max_length=300, blank=True, null=True)

    date_discovered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image_url}" width="auto" height="400" />')

    image_tag.short_description = 'Image'

    @classmethod
    def create_from_raw(cls, raw_group_post: GroupPostRaw):
        raw_group_post.author, _ = Author.create_from_raw(raw_group_post.author)
        post = cls.objects.get_or_create(**raw_group_post.__dict__)
        return post

    def __str__(self):
        return f'[{self.facebook_id}]Post by [{self.author.name}], ({self.reaction_count} reactions)'

    def __eq__(self, other) -> bool:
        return self.facebook_id == other.facebook_id and self.id == other.id
