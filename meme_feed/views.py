from django.shortcuts import render, redirect
from jwt import ExpiredSignatureError
from rest_framework import viewsets, views, status
from rest_framework import exceptions

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view

from django.http import JsonResponse

from allauth.socialaccount import models as authModels
from django.contrib.auth.models import User
from django.contrib.auth import settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from meme_feed.models import Author, GroupPostComment

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import jwt_get_username_from_payload, jwt_decode_handler

from meme_feed.models import GroupPost, Author, GroupPostComment
from meme_feed.serializers import MemeSerializer, AuthorSerializer, GroupPostCommentSerializer, \
    GroupPostCommentSerializerWithAuthor

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class MemeViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Api endpoint for viewing dem sweet memes
    '''
    queryset = GroupPost.objects.filter(approved=True).order_by('-reaction_count')
    serializer_class = MemeSerializer


class AuthorsViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Api endpoint for viewing dem sweet memes authors
    '''

    def list(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied(detail="You can't list users", code=403)

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


def facebook_login(request):
    user = request.user
    facebook_account = authModels.SocialAccount.objects.get(user_id=user.id)

    author_account, created = Author.objects.get_or_create(facebook_id=facebook_account.extra_data['id'])
    author_account.facebook_profile = facebook_account
    author_account.save()
    response = redirect(settings.CLIENT_ADDRESS + '/#/profile/' + str(author_account.id) + '#')

    response.set_cookie('meme-token', jwt_encode_handler(jwt_payload_handler(user)), max_age=5*60)  # TODO: Set to one day

    return response


def jwt_get_owner(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    if token == 'undefined':
        return JsonResponse(data={'success': False}, status=401)
    try:
        username = jwt_get_username_from_payload(jwt_decode_handler(token))
        author = Author.get_by_username(username=username)
        return JsonResponse({'author': {
            'name': author.name,
            'id': author.id
        }})
    except ExpiredSignatureError as e:
        print(e)
        return JsonResponse({'author': None})


def toggle_real_photo(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    if token == 'undefined':
        return JsonResponse(data={'success': False}, status=401)
    try:
        username = jwt_get_username_from_payload(jwt_decode_handler(token))
        author = Author.get_by_username(username=username)
        author.avatar_displayed = not author.avatar_displayed
        author.save()
        success = True
    except ExpiredSignatureError as e:
        print(e)
        success = False

    return JsonResponse(data={'success': success}, status=200 if success else 400)


def toggle_real_name(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    if token == 'undefined':
        return JsonResponse(data={'success': False}, status=401)
    try:
        username = jwt_get_username_from_payload(jwt_decode_handler(token))
        author = Author.get_by_username(username=username)
        author.name_displayed = not author.name_displayed
        author.save()
        success = True
    except ExpiredSignatureError as e:
        print(e)
        success = False

    return JsonResponse(data={'success': success}, status=200 if success else 400)


class CommentViewSet(viewsets.ModelViewSet):
    # serializer_class = GroupPostCommentSerializer
    # permission_classes = IsAuthenticatedOrReadOnly

    def get_serializer_class(self):
        return GroupPostCommentSerializer

    def get_queryset(self):
        meme_id = self.request.query_params.get('meme_id', None)
        if meme_id is not None:
            return GroupPostComment.objects.all().filter(commented_object__id=meme_id).order_by('-created')
        return GroupPostComment.objects.none()

    def perform_create(self, serializer):
        author = Author.get_from_request(self.request)
        serializer.save(
            author=author,
            commented_object=GroupPost.objects.get(
                id=self.request.parser_context['kwargs']['parent_lookup_commented_object']
            )
        )
        # def create(self, request, *args, **kwargs):
        #     pass
        #
        # def post(self, request):
        #     serializer = GroupPostCommentSerializer(
        #         data=request
        #     )
        #
        #     if serializer.is_valid():
        #         comment = GroupPostComment(serializer)
        #         comment.author = Author.objects.get(user=request.user)
        #         comment.save()
        #         return JsonResponse(data=GroupPostCommentSerializer(comment).data,
        #                             status=status.HTTP_201_CREATED)
        #     return JsonResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
