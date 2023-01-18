from unittest.mock import ANY

from django.urls import reverse

from app.test import BaseTestCase


class UserViewTests(BaseTestCase):
    def test_user_authentication(self):
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test1@example.com", "password": "Password@1"},
        )
        self.assertEqual(response.status_code, 200)
        expected = {"error": None, "msg": "Authenticated Successfully", "data": ANY}
        self.assertEqual(response.json(), expected)

    def test_invalid_credentials(self):
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test1@example.com", "password": "Password"},
        )
        self.assertEqual(response.status_code, 401)

    def test_not_existing_user(self):
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "NoTest@example.com", "password": "Password"},
        )
        self.assertEqual(response.status_code, 404)

    def test_follow_unfollow_user(self):
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test1@example.com", "password": "Password@1"},
        )
        self.assertEqual(response.status_code, 200)
        auth_headers_u0 = {
            "HTTP_AUTHORIZATION": "Bearer " + response.json()["data"],
        }

        # User 0 follows user 1 & 2
        response = self.client.post(
            reverse("follow_user", args=[self.users[1].pk]), **auth_headers_u0
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("follow_user", args=[self.users[2].pk]), **auth_headers_u0
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("get_user_detail"), **auth_headers_u0)
        self.assertEqual(response.status_code, 200)
        expected = {
            "error": None,
            "msg": "Ok",
            "data": {
                "id": self.users[0].pk,
                "username": self.users[0].username,
                "followers": 0,
                "followings": 2,
            },
        }
        self.assertEqual(response.json(), expected)

        # user 0 unfollows user 1
        response = self.client.post(
            reverse("unfollow_user", args=[self.users[2].pk]), **auth_headers_u0
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("get_user_detail"), **auth_headers_u0)
        self.assertEqual(response.status_code, 200)

        expected = {
            "error": None,
            "msg": "Ok",
            "data": {
                "id": self.users[0].pk,
                "username": self.users[0].username,
                "followers": 0,
                "followings": 1,
            },
        }
        self.assertEqual(response.json(), expected)

        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test2@example.com", "password": "Password@1"},
        )
        self.assertEqual(response.status_code, 200)
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + response.json()["data"],
        }

        # user 1 follows user 0
        response = self.client.post(
            reverse("follow_user", args=[self.users[0].pk]), **auth_headers
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("get_user_detail"), **auth_headers_u0)
        self.assertEqual(response.status_code, 200)

        expected = {
            "error": None,
            "msg": "Ok",
            "data": {
                "id": self.users[0].pk,
                "username": self.users[0].username,
                "followers": 1,
                "followings": 1,
            },
        }
        self.assertEqual(response.json(), expected)

    def test_unfollow_not_following_user(self):
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test1@example.com", "password": "Password@1"},
        )
        self.assertEqual(response.status_code, 200)
        auth_headers_u0 = {
            "HTTP_AUTHORIZATION": "Bearer " + response.json()["data"],
        }
        response = self.client.post(
            reverse("unfollow_user", args=[self.users[2].pk]), **auth_headers_u0
        )
        self.assertEqual(response.status_code, 404)
        expected = {
            "error": f"You are not following user {self.users[2].pk}",
            "msg": "Not found",
            "data": None,
        }
        self.assertEqual(response.json(), expected)

    def test_following_self(self):
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test1@example.com", "password": "Password@1"},
        )
        self.assertEqual(response.status_code, 200)
        auth_headers_u0 = {
            "HTTP_AUTHORIZATION": "Bearer " + response.json()["data"],
        }
        response = self.client.post(
            reverse("follow_user", args=[self.users[0].pk]), **auth_headers_u0
        )
        self.assertEqual(response.status_code, 400)
        expected = {
            "error": "Cannot follow self",
            "msg": "Bad Request",
            "data": None,
        }
        self.assertEqual(response.json(), expected)
