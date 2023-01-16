from django.urls import path

from posts.views import PostDetailViewSet, PostViewSet, PostLikeCommentViewSet

urlpatterns = [
    path("posts", PostViewSet.as_view({"post": "create"})),
    path("all_posts", PostViewSet.as_view({"get": "list"})),
    path("posts/<pk>", PostDetailViewSet.as_view({"get": "retrieve"})),
    path("posts/<pk>", PostDetailViewSet.as_view({"delete": "destroy"})),
    path("like/<pk>", PostLikeCommentViewSet.as_view({"post": "like"})),
    path("unlike/<pk>", PostLikeCommentViewSet.as_view({"post": "unlike"})),
    path("comment/<pk>", PostLikeCommentViewSet.as_view({"post": "comment"})),
]
