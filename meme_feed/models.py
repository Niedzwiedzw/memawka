from django.db import models

from django.db.models import Avg
from django.utils import timezone

from django.utils.safestring import mark_safe
from jwt import ExpiredSignatureError

from koparka_memow.token_manager.token_manager import TokenManager

from koparka_memow.models import Author as AuthorRaw
from koparka_memow.models import GroupPost as GroupPostRaw

from rest_framework_jwt.authentication import jwt_get_username_from_payload, jwt_decode_handler
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from django.conf import settings

from django.core.exceptions import ValidationError


def validate_minimal_quality_factor(value):
    if not (0 < value < 1):
        raise ValidationError("Number must be between 0 and 1")


class FacebookGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group_id = models.CharField(max_length=100, unique=True)

    deep_scanned = models.BooleanField(default=False)
    deep_validated = models.BooleanField(default=False)

    _minimal_quality_factor = models.FloatField(default=0.85, validators=[validate_minimal_quality_factor])
    _criteria_last_updated = models.DateTimeField(null=True, blank=True, default=None)
    _criteria_last_value = models.IntegerField(null=True, blank=True, default=None)

    _facebook_auth_key = models.CharField(max_length=100, blank=True, null=True, default=None)

    @property
    def posts_from_current_month(self):
        return self.posts_from_month(timezone.now().month)

    @property
    def posts_from_last_month(self):
        current = timezone.now().month
        last = current-1 if current != 1 else current+11
        return self.posts_from_month(last)

    def posts_from_month(self, month=None, year=None):
        if month is None:
            month = timezone.now().month
        if year is None:
            year = timezone.now().year

        return self.posts.filter(created__year=year, created__month=month)

    def monthly_top(self, month):
        return self.posts.filter(created__month=month).order_by('-reaction_count').first()

    def monthly_top_average_likes(self, month):
        posts = self.posts.filter(created__month=month).order_by('-reaction_count')
        top_percent = int(posts.count()/80)
        top_posts = posts[:top_percent]
        top_avg = list(top_posts.aggregate(Avg('reaction_count')).values())[0]
        return top_avg if top_avg else 0

    @property
    def current_month_minimum_like_criteria(self):
        if self._criteria_last_updated and self._criteria_last_updated.month == timezone.now().month:
            # print(self._criteria_last_value)
            return self._criteria_last_value

        initial_month = timezone.now().month-1
        number_of_months = 3

        months = list(range(initial_month - number_of_months + 1, initial_month + 1))
        months = [month+12 if month < 1 else month for month in months]

        average = int(sum([self.monthly_top_average_likes(month) for month in months])/number_of_months)

        self._criteria_last_value = int(average * self._minimal_quality_factor**4)
        self._criteria_last_updated = timezone.now()

        self.save()

        return self._criteria_last_value if self._criteria_last_value > 30 else 30

    @property
    def this_month_average(self):
        now = timezone.now()
        return self.posts.filter(created__month=now.month,
                                 created__year=now.year).aggregate(Avg('reaction_count')).values[0]

    @property
    def this_year_average(self):
        now = timezone.now()
        return self.posts.filter(created__month=now.year).aggregate(Avg('reaction_count')).values[0]

    @property
    def last_month_average(self):
        now = timezone.now()
        return self.posts.filter(
            created__month=now.month-1 if now.month != 1 else now.month + 11,
            created__year=now.year if now.month != 1 else now.year - 1).aggregate(Avg('reaction_count')).values[0]

    @property
    def last_year_average(self):
        now = timezone.now()
        return self.posts.filter(created__month=now.year-1).aggregate(Avg('reaction_count')).values[0]

    @property
    def all_time_average(self):
        return self.posts.aggregate(Avg('reaction_count')).values[0]

    @property
    def facebook_auth_key(self):
        return self._facebook_auth_key if self._facebook_auth_key else TokenManager.get_token()

    def __str__(self):
        return self.name


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
        return GroupPost.objects.filter(author__id=self.id, approved=True)

    @classmethod
    def create_from_raw(cls, raw_author: AuthorRaw):
        try:
            author = Author.objects.get(facebook_id=raw_author.facebook_id)
            return author, False
        except Author.DoesNotExist:
            return cls.objects.get_or_create(**raw_author.__dict__)

    def __str__(self):
        return f'[{self.facebook_id}] {self.name}'

    def __eq__(self, other) -> bool:
        return self.facebook_id == other.facebook_id and self.id == other.id


class GroupPost(models.Model):
    facebook_id = models.CharField(verbose_name='Facebook post ID', unique=True, max_length=200)
    created = models.DateTimeField(verbose_name="Facebook post creation date")
    author = models.ForeignKey(Author, verbose_name='Facebook post Author', related_name='author')
    message = models.TextField(verbose_name='Facebook post message', blank=True, null=True)
    reaction_count = models.IntegerField(verbose_name='Number of likes')
    image_url = models.CharField(max_length=300, blank=True, null=True)

    facebook_group = models.ForeignKey(FacebookGroup, related_name='posts')

    approved = models.BooleanField(default=False)

    date_discovered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def check_for_approval_and_approve(self):
        minimum_likes = self.facebook_group.current_month_minimum_like_criteria

        if self.reaction_count >= minimum_likes:
            self.approved = True
            self.save()
            return True

        growth_per_sec = 1 + int(self.reaction_count / (self.date_updated - self.created).seconds)

        if growth_per_sec >= int(minimum_likes/48*60*60) + 1:
            self.approved = True
            self.save()
            return True
        return False

    def image_tag(self):
        return mark_safe(f'<img src="{self.image_url}" width="auto" height="400"/>')

    image_tag.short_description = 'Image'

    @classmethod
    def create_from_raw(cls, raw_group_post: GroupPostRaw):
        try:
            post = GroupPost.objects.get(facebook_id=raw_group_post.facebook_id), False
            post[0].update_from_raw(raw_group_post)
        except GroupPost.DoesNotExist:
            raw_group_post.author, _ = Author.create_from_raw(raw_group_post.author)
            post = cls.objects.get_or_create(**raw_group_post.__dict__)
        return post

    def update_from_raw(self, raw_group_post: GroupPostRaw):
        self.reaction_count = raw_group_post.reaction_count
        self.save()

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


