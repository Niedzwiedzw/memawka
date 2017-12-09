from django.db import models
from django.utils.safestring import mark_safe
from jwt import ExpiredSignatureError

from koparka_memow.models import Author as AuthorRaw
from koparka_memow.models import GroupPost as GroupPostRaw

from rest_framework_jwt.authentication import jwt_get_username_from_payload, jwt_decode_handler
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from django.conf import settings


class Author(models.Model):
    facebook_id = models.CharField(verbose_name='Facebook user ID', unique=True, max_length=200)
    name = models.CharField(max_length=200, verbose_name='Facebook name')
    facebook_profile = models.ForeignKey(SocialAccount,
                                         blank=True,
                                         null=True,
                                         default=None,
                                         related_name='facebook_profile')

    facebook_authorized = models.BooleanField(default=False)
    name_displayed = models.BooleanField(default=False)
    avatar_displayed = models.BooleanField(default=False)

    @property
    def display_avatar(self):
        default = 'https://upload.wikimedia.org/wikipedia/commons/4/42/A_black_man%2C_Chicago._-_NARA_-_556149.jpg'
        return self.facebook_profile.get_avatar_url() if self.avatar_displayed else default

    @classmethod
    def get_by_user(cls, user):
        from pprint import pprint
        pprint(user)
        return cls.objects.get(facebook_profile__user=user)

    @classmethod
    def get_from_request(cls, request):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        if token == 'undefined':
            return cls.objects.none()
        try:
            username = jwt_get_username_from_payload(jwt_decode_handler(token))
            return cls.get_by_username(username=username)

        except ExpiredSignatureError as e:
            print(e)
            return cls.objects.none()

    @classmethod
    def get_by_username(cls, username: str):
        return cls.objects.get(facebook_profile__user=User.objects.get(username=username))

    @property
    def user(self):
        if self.facebook_profile is None:
            return None
        return self.facebook_profile.user

    @property
    def active_token(self):
        return

    @property
    def display_name(self):
        return self.name if self.name_displayed else settings.DEFAULT_NAME

    @property
    def reaction_sum(self):
        return self.memes.aggregate(models.Sum('reaction_count'))

    @property
    def memes(self):
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
    created = models.DateTimeField(verbose_name="Facebook post creation date", )
    author = models.ForeignKey(Author, verbose_name='Facebook post Author', related_name='author')
    message = models.TextField(verbose_name='Facebook post message', blank=True, null=True)
    reaction_count = models.IntegerField(verbose_name='Number of likes')
    image_url = models.CharField(max_length=300, blank=True, null=True)

    date_discovered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image_url}" width="auto" height="400"/>')

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


# Comments:
class BaseComment(models.Model):
    message = models.TextField(max_length=500)
    reported = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class GroupPostComment(BaseComment):
    author = models.ForeignKey(Author, related_name='my_group_post_comments')
    commented_object = models.ForeignKey(GroupPost, related_name='comments')


class AuthorComment(BaseComment):
    author = models.ForeignKey(Author, related_name='my_author_comments')
    commented_object = models.ForeignKey(Author, related_name='comments')


# Likes:
class BaseLike(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class GroupPostLike(BaseLike):
    author = models.ForeignKey(Author, related_name='my_group_post_likes')
    liked_object = models.ForeignKey(GroupPost, related_name='likes')


class AuthorLike(BaseLike):
    author = models.ForeignKey(Author, related_name='my_author_likes')
    liked_object = models.ForeignKey(Author, related_name='likes')
