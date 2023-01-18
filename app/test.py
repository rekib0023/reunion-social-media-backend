from django.contrib.auth.hashers import make_password
from django.test import Client, TestCase

from user.models import User


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.users = User.objects.bulk_create(
            [
                User(
                    email="Test1@example.com",
                    username="TestUser1",
                    password=make_password("Password@1"),
                ),
                User(
                    email="Test2@example.com",
                    username="TestUser2",
                    password=make_password("Password@1"),
                ),
                User(
                    email="Test3@example.com",
                    username="TestUser3",
                    password=make_password("Password@1"),
                ),
                User(
                    email="Test4@example.com",
                    username="TestUser4",
                    password=make_password("Password@1"),
                ),
            ]
        )
        cls.client = Client()
