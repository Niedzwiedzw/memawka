from rest_framework import viewsets, views
from rest_framework import exceptions
from rest_framework.decorators import api_view

from meme_feed.models import GroupPost, Author
from meme_feed.serializers import MemeSerializer, AuthorSerializer


class MemeViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Api endpoint for viewing dem sweet memes
    '''
    queryset = GroupPost.objects.order_by('-reaction_count')
    serializer_class = MemeSerializer


class AuthorsViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Api endpoint for viewing dem sweet memes
    '''

    def list(self, request):
        raise exceptions.PermissionDenied(detail="You can't list users", code=403)

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
