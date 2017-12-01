from rest_framework import serializers
from meme_feed.models import GroupPost


class MemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupPost
        fields = ('creation', 'message', 'reaction_count', 'image_url', 'facebook_id',)
