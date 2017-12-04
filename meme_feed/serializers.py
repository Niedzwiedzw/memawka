from rest_framework import serializers, exceptions
from meme_feed.models import GroupPost, Author


class AuthorSmallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'display_name')


class MemeSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSmallSerializer(many=False, read_only=True)

    class Meta:
        model = GroupPost
        fields = ('creation', 'message', 'reaction_count', 'image_url', 'facebook_id', 'author')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    memes = MemeSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'display_name', 'memes', 'reaction_sum')

