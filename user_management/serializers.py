from django.contrib.auth.models import User
from blog.models import Post, Comments
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comments-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'comments', 'post']
