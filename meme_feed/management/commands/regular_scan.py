from django.core.management.base import BaseCommand, CommandError
from time import sleep

from meme_feed.models import GroupPost, Author, FacebookGroup
from koparka_memow.koparka_memow import KoparkaMemow
from meme_feed.models import GroupPost


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):
        for facebook_group in FacebookGroup.objects.all():
            print("## ", facebook_group.name)
            print("likes threshold: {}".format(facebook_group.current_month_minimum_like_criteria))

            koparka = KoparkaMemow(
                limit=1+facebook_group.posts_from_last_month.count()//10,
                facebook_group=facebook_group)

            added_count = 0
            approved_count = 0

            for post in koparka.posts:
                if not post.image_url:
                    continue

                post.facebook_group = facebook_group
                group_post, _created = GroupPost.create_from_raw(post)

                if _created:
                    print('.', end='')
                    added_count += 1

                _status = group_post.approved
                group_post.check_for_approval_and_approve()
                if _status != group_post.approved:
                    print('*', end='')
                    approved_count += 1

            print('Approved: ', approved_count, '\n')



