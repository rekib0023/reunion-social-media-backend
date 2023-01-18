from django.urls import path

from user.views import FollowViewSet, UserDetailViewSet, UserViewSet

urlpatterns = [
    path(
        "authenticate",
        UserViewSet.as_view({"post": "authenticate"}),
        name="authenticate",
    ),
    path(
        "user", UserDetailViewSet.as_view({"get": "retrieve"}), name="get_user_detail"
    ),
    path(
        "follow/<user_id>",
        FollowViewSet.as_view({"post": "follow"}),
        name="follow_user",
    ),
    path(
        "unfollow/<user_id>",
        FollowViewSet.as_view({"post": "unfollow"}),
        name="unfollow_user",
    ),
]
