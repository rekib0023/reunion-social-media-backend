from rest_framework import serializers

from posts.models import PostComment, Posts


class BasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ("id", "title", "description", "created_at")


class PostSerializer(BasePostSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta(BasePostSerializer.Meta):
        fields = BasePostSerializer.Meta.fields + ("comments", "likes")

    def get_comments(self, obj):
        serializer = PostCommentSerializer(obj.comments_set.all(), many=True)
        return serializer.data

    def get_likes(self, obj):
        return obj.likes_set.count()


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ("id", "comment", "commented_by", "created_at")
