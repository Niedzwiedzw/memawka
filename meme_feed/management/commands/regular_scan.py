from django.core.management.base import BaseCommand, CommandError
from time import sleep

from meme_feed.models import GroupPost, Author, FacebookGroup
from koparka_memow.koparka_memow import KoparkaMemow
from meme_feed.models import GroupPost


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):
        for facebook_group in FacebookGroup.objects.all():
            koparka = KoparkaMemow(limit=50, facebook_group=facebook_group)
            i = 0

            for post in koparka.posts:
                print('.', end='')
                post.facebook_group = facebook_group
                group_post, _ = GroupPost.create_from_raw(post)

                group_post.check_for_approval_and_approve()

            print(i, ' ')

