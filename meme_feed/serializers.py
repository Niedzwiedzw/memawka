from rest_framework import serializers, exceptions
from meme_feed.models import GroupPost, Author, GroupPostComment


class GroupPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPostComment
        fields = ('id', 'message', 'author', 'created', 'commented_object')


class AuthorSmallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'display_name', 'display_avatar')


class GroupPostCommentSerializerWithAuthor(serializers.HyperlinkedModelSerializer):
    author = AuthorSmallSerializer(many=False, read_only=True)

    class Meta:
        model = GroupPostComment
        fields = ('id', 'message', 'author', 'created')


class MemeSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSmallSerializer(many=False, read_only=True)
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        ordered_queryset = obj.comments.order_by('-created')
        return GroupPostCommentSerializerWithAuthor(ordered_queryset, many=True).data

    class Meta:
        model = GroupPost
        fields = (
            'id',
            'created',
            'message',
            'reaction_count',
            'image_url',
            'facebook_id',
            'author',
            'comments')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    memes = MemeSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id',
                  'display_name',
                  'display_avatar',
                  'memes',
                  'reaction_sum')
