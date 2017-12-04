from django.shortcuts import render, redirect
from rest_framework import viewsets, views
from rest_framework import exceptions
from rest_framework.decorators import api_view

from allauth.socialaccount import models as authModels
from django.contrib.auth.models import User
from django.contrib.auth import settings
from meme_feed.models import Author

from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

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


def facebook_login(request):
    user = request.user
    facebook_account = authModels.SocialAccount.objects.get(user_id=user.id)

    author_account, created = Author.objects.get_or_create(facebook_id=facebook_account.extra_data['id'])
    author_account.facebook_profile = facebook_account
    author_account.save()
    response = redirect(settings.CLIENT_ADDRESS)

    response.set_cookie('meme-token', jwt_encode_handler(jwt_payload_handler(user)), max_age=60)  # TODO: Set to one day

    return response
