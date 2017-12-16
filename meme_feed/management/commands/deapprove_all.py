from django.core.management.base import BaseCommand

from meme_feed.models import FacebookGroup

from django.utils import timezone


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):

        for facebook_group in FacebookGroup.objects.all():
            print("##### DEAPPROVING: ", facebook_group.name)
            for post in facebook_group.posts.filter(approved=True):
                post.approved = False
                post.save()
            facebook_group.deep_validated = False
            facebook_group.save()
            print('...done')