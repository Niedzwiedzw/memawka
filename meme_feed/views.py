from rest_framework import viewsets

from meme_feed.models import GroupPost
from meme_feed.serializers import MemeSerializer


class MemeViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Api endpoint for viewing dem sweet memes
    '''
    queryset = GroupPost.objects.order_by('-reaction_count')
    serializer_class = MemeSerializer
