from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from posts.models import Posts, PostLike, PostComment
from posts.serializers import BasePostSerializer, PostSerializer


class PostViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = BasePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(
            {
                "error": None,
                "msg": "Post created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        posts = Posts.objects.filter(created_by=request.user).all()
        serializer = PostSerializer(posts, many=True)
        return Response(
            {
                "error": None,
                "msg": "OK",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class PostDetailViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk):
        try:
            post = get_object_or_404(Posts, pk=pk)
            serializer = PostSerializer(post, many=False)
            return Response(
                {
                    "error": None,
                    "msg": "OK",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            return Response(
                {
                    "error": str(err),
                    "msg": "Not Found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, pk):
        try:
            post = get_object_or_404(Posts, pk=pk, created_by=request.user)
            post.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as err:
            return Response(
                {
                    "error": str(err),
                    "msg": "Not Found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class PostLikeCommentViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def like(self, request, pk):
        try:
            post = get_object_or_404(Posts, pk=pk)
            post_like = PostLike(post=post, user=request.user)
            post_like.save()
            return Response(
                status=status.HTTP_201_CREATED,
            )
        except Exception as err:
            return Response(
                {
                    "error": str(err),
                    "msg": "Not Found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def unlike(self, request, pk):
        try:
            post_like = get_object_or_404(PostLike, pk=pk, user=request.user)
            post_like.delete()
            return Response(
                status=status.HTTP_201_CREATED,
            )
        except Exception as err:
            return Response(
                {
                    "error": str(err),
                    "msg": "Not Found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def comment(self, request, pk):
        try:
            post = get_object_or_404(Posts, pk=pk)
            msg = request.data.pop("comment")
            comment = PostComment(post=post, comment=msg, commented_by=request.user)
            comment.save()
            comment.refresh_from_db()
            return Response(
                {
                    "error": None,
                    "msg": "Commented successfully",
                    "data": {"comment_id": comment.pk},
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as err:
            return Response(
                {
                    "error": str(err),
                    "msg": "Not Found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
