from django.urls import path

from posts.views import PostDetailViewSet, PostLikeCommentViewSet, PostViewSet

urlpatterns = [
    path(
        "posts",
        PostViewSet.as_view({"post": "create"}),
        name="create_post",
    ),
    path(
        "all_posts",
        PostViewSet.as_view({"get": "list"}),
        name="list_posts",
    ),
    path(
        "posts/<pk>",
        PostDetailViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="post_detail",
    ),
    path(
        "like/<pk>",
        PostLikeCommentViewSet.as_view({"post": "like"}),
        name="like_post",
    ),
    path(
        "unlike/<pk>",
        PostLikeCommentViewSet.as_view({"post": "unlike"}),
        name="unlike_post",
    ),
    path(
        "comment/<pk>",
        PostLikeCommentViewSet.as_view({"post": "comment"}),
        name="comment_post",
    ),
]
