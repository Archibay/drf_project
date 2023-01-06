from blog.models import Post, Comments
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='post_highlight', format='html')

    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'text', 'created_date', 'published', 'owner']


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='comments_highlight', format='html')

    class Meta:
        model = Comments
        fields = ['url', 'id', 'text', 'post', 'published', 'owner']
