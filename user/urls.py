from user.views import UserViewSet, FollowViewSet
from django.urls import path

urlpatterns = [
    path("authenticate", UserViewSet.as_view({"post": "authenticate"})),
    path("user", UserViewSet.as_view({"get": "get"})),
    path("follow/<user_id>", FollowViewSet.as_view({"post": "follow"})),
    path("unfollow/<user_id>", FollowViewSet.as_view({"post": "unfollow"})),
]
