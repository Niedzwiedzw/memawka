from django.core.management.base import BaseCommand, CommandError
from time import sleep

from meme_feed.models import GroupPost, Author, FacebookGroup
from koparka_memow.koparka_memow import KoparkaMemow
from meme_feed.models import GroupPost



class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):
        for facebook_group in FacebookGroup.objects.all():
            if not facebook_group.deep_scanned:
                koparka = KoparkaMemow(limit=50, facebook_group=facebook_group)
                print('######### scanning: ', facebook_group.name)
                i = 0
                while True:
                    for post in koparka.posts:
                        if not post.image_url:
                            continue
                        print('.', end='')
                        post.facebook_group = facebook_group
                        GroupPost.create_from_raw(post)
                    print(i, ' ')
                    if not koparka.next():
                        facebook_group.deep_scanned = True
                        facebook_group.save()
                        exit(0)
                    i += 1
