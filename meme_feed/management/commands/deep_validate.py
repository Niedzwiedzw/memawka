from django.core.management.base import BaseCommand

from meme_feed.models import FacebookGroup

from django.utils import timezone


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):

        for facebook_group in FacebookGroup.objects.all():
            top = int(facebook_group.posts.count()/100)+1
            for post in facebook_group.posts.order_by('-reaction_count')[:top]:
                post.approved = True
                post.save()

            now = timezone.now()
            current_month = now.month
            current_year = now.year

            while True:
                posts_from_month = facebook_group.posts_from_month(current_month, current_year)
                limit = int(posts_from_month.count() * 0.95)+1

                if posts_from_month.exists():
                    for post in posts_from_month[:limit]:
                        post.approved = True
                        post.save()
                    current_month -= 1
                    if current_month < 1:
                        current_year -= 1
                        current_month += 12
                else:
                    break
