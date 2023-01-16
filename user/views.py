from rest_framework import viewsets, status
from user.models import User, Followings
from user.serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException


class UserViewSet(viewsets.ViewSet):
    def authenticate(self, request):
        data = request.data
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            return Response(
                {
                    "error": "No user found with this email address",
                    "msg": "User not found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if not check_password(data["password"], user.password):
            return Response(
                {
                    "error": "Invalid credentials",
                    "msg": "Unauthorized",
                    "data": None,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "error": None,
                "msg": "Authenticated Successfully",
                "data": user.token,
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(
            {
                "error": None,
                "msg": "Ok",
                "data": serializer.data,
            }
        )


class FollowViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def follow(self, request, user_id):
        if request.user.pk == user_id:
            return Response(
                {
                    "error": "Cannot follow self",
                    "msg": "Bad Request",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            following = Followings(user_id=request.user.pk, following_id=user_id)
            following.save()
        except Exception as err:
            raise APIException(
                {
                    "error": str(err),
                    "msg": "Internal Server Error",
                    "data": None,
                }
            )
        return Response(
            {
                "error": None,
                "msg": "Followed successfully",
                "data": None,
            }
        )

    def unfollow(self, request, user_id):
        following = Followings.objects.filter(user_id=request.user.pk, following_id=user_id).first()
        if not following:
            return Response(
                {
                    "error": f"You are not following user {user_id}",
                    "msg": "Not found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            following.delete()
        except Exception as err:
            raise APIException(
                {
                    "error": str(err),
                    "msg": None,
                    "data": None,
                }
            )
        return Response(
            {
                "error": None,
                "msg": "Unfollowed successfully",
                "data": None,
            }
        )