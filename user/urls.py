from django.urls import path

from user.views import FollowViewSet, UserDetailViewSet, UserViewSet

urlpatterns = [
    path("authenticate", UserViewSet.as_view({"post": "authenticate"})),
    path("user", UserDetailViewSet.as_view({"get": "retrieve"})),
    path("follow/<user_id>", FollowViewSet.as_view({"post": "follow"})),
    path("unfollow/<user_id>", FollowViewSet.as_view({"post": "unfollow"})),
]
