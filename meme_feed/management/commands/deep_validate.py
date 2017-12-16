from django.core.management.base import BaseCommand

from meme_feed.models import FacebookGroup

from django.utils import timezone


class Command(BaseCommand):
    help = 'Pulls some posts from group into the database'

    def handle(self, *args, **options):

        for facebook_group in FacebookGroup.objects.all():
            if facebook_group.deep_validated:
                continue
            print("####### DEEP VALIDATING: ", facebook_group.name)
            monthly_top = input(f'Top posts of the month for {facebook_group.name[:10]}...? (Y/n)').lower()
            monthly_top = {'y': True, 'n': False}.get(monthly_top, False)

            top = int(facebook_group.posts.count()/250)+9
            for post in facebook_group.posts.filter(reaction_count__gte=30).order_by('-reaction_count')[:top]:
                post.approved = True
                post.save()

            now = timezone.now()
            current_month = now.month
            current_year = now.year

            if monthly_top:
                while True:
                    posts_from_month = facebook_group.posts_from_month(
                        current_month,
                        current_year)
                    limit = int(posts_from_month.count() * (1 - facebook_group._minimal_quality_factor**(1/4))) + 1

                    if posts_from_month.exists():
                        for post in posts_from_month.filter(reaction_count__gte=30)[:limit]:
                            post.approved = True
                            post.save()
                        current_month -= 1
                        if current_month < 1:
                            current_year -= 1
                            current_month += 12
                    else:
                        facebook_group.deep_validated = True
                        facebook_group.save()
                        break
