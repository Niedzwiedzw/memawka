from django.core.management.base import BaseCommand, CommandError
from time import sleep

from meme_feed.models import GroupPost, Author
from koparka_memow.koparka_memow import KoparkaMemow


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):
        koparka = KoparkaMemow(limit=50)
        for i in range(10):
            sleep(1)
            for post in koparka.posts:
                print(type(post.author))
                print('.', end='')
                GroupPost.create_from_raw(post)
            print()
            koparka.next()
