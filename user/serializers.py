from user.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "followers", "followings")

    def get_followers(self, obj):
        return obj.followers_set.count()

    def get_followings(self, obj):
        return obj.followings_set.count()
