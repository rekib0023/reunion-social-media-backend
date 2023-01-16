from posts.models import Posts
from rest_framework import serializers


class BasePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ("username", "followers", "followings", "created_at")

