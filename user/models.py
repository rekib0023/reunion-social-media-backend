from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=150, null=False)
    username = models.CharField(max_length=150, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token


class Followings(models.Model):
    user = models.ForeignKey(
        "User", related_name="followings_set", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        "User", related_name="followers_set", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'], name='follower_following_unique')
        ]