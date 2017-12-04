from django.core.management.base import BaseCommand, CommandError
from time import sleep

from meme_feed.models import GroupPost, Author
from koparka_memow.koparka_memow import KoparkaMemow


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):
        koparka = KoparkaMemow(limit=50)
        i = 0
        while True:
            for post in koparka.posts:
                print('.', end='')
                GroupPost.create_from_raw(post)
            print(i)
            koparka.next()
            i += 1
