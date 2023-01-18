import json
from unittest.mock import ANY

from django.urls import reverse

from app.test import BaseTestCase
from posts.models import PostComment, PostLike, Posts
from posts.serializers import PostCommentSerializer


class PostViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.posts = Posts.objects.bulk_create(
            [
                Posts(
                    title="Title 1",
                    description="This is a description",
                    created_by=cls.users[0],
                ),
                Posts(
                    title="Title 2",
                    description="This is a description",
                    created_by=cls.users[0],
                ),
                Posts(
                    title="Title 3",
                    description="This is a description",
                    created_by=cls.users[0],
                ),
            ],
        )

    def setUp(self) -> None:
        response = self.client.post(
            reverse("authenticate"),
            data={"email": "Test1@example.com", "password": "Password@1"},
        )
        self.assertEqual(response.status_code, 200)
        self.auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + response.json()["data"],
        }

    def test_post_create(self):
        body = {
            "title": "This is a title",
            "description": "This is a description",
        }
        response = self.client.post(
            reverse("create_post"), data=body, **self.auth_headers
        )

        self.assertEqual(response.status_code, 201)
        expected = {
            "error": None,
            "msg": "Post created successfully",
            "data": {
                "id": ANY,
                "title": "This is a title",
                "description": "This is a description",
                "created_at": ANY,
            },
        }
        self.assertEqual(response.json(), expected)

    def test_post_with_missing_fields(self):
        body = {
            "title": "This is a title",
        }
        response = self.client.post(
            reverse("create_post"), data=body, **self.auth_headers
        )

        self.assertEqual(response.status_code, 400)
        expected = {"description": ["This field is required."]}
        self.assertEqual(response.json(), expected)

    def test_get_all_posts(self):
        response = self.client.get(reverse("list_posts"), **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        expected = {
            "error": None,
            "msg": "OK",
            "data": list(
                sorted(
                    [
                        {
                            "id": p.pk,
                            "title": p.title,
                            "description": p.description,
                            "created_at": p.created_at.isoformat().replace(
                                "+00:00", "Z"
                            ),
                            "comments": [],
                            "likes": 0,
                        }
                        for p in self.posts
                    ],
                    key=lambda x: x["created_at"],
                    reverse=True,
                )
            ),
        }
        self.assertEqual(response.json(), expected)

    def test_retrieve_posts(self):
        response = self.client.get(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        expected = {
            "error": None,
            "msg": "OK",
            "data": {
                "id": self.posts[0].pk,
                "title": self.posts[0].title,
                "description": self.posts[0].description,
                "created_at": self.posts[0]
                .created_at.isoformat()
                .replace("+00:00", "Z"),
                "comments": [],
                "likes": 0,
            },
        }
        self.assertEqual(response.json(), expected)

        response = self.client.get(
            reverse("post_detail", args=[11]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_posts(self):
        response = self.client.delete(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 204)

    def test_like_unlike_post(self):
        response = self.client.get(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        expected = {
            "id": ANY,
            "title": ANY,
            "description": ANY,
            "created_at": ANY,
            "comments": ANY,
            "likes": 0,
        }
        self.assertEqual(response.json()["data"], expected)

        response = self.client.post(reverse("like_post", args=[1]), **self.auth_headers)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        expected = {
            "id": ANY,
            "title": ANY,
            "description": ANY,
            "created_at": ANY,
            "comments": ANY,
            "likes": 1,
        }
        self.assertEqual(response.json()["data"], expected)

        response = self.client.post(
            reverse("unlike_post", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        expected = {
            "id": ANY,
            "title": ANY,
            "description": ANY,
            "created_at": ANY,
            "comments": ANY,
            "likes": 0,
        }
        self.assertEqual(response.json()["data"], expected)

    def test_comment_post(self):
        response = self.client.get(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        expected = {
            "id": ANY,
            "title": ANY,
            "description": ANY,
            "created_at": ANY,
            "comments": [],
            "likes": ANY,
        }
        self.assertEqual(response.json()["data"], expected)

        response = self.client.post(
            reverse("comment_post", args=[1]),
            data={"comment": "this is a comment"},
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)
        expected = {"comment_id": ANY}
        self.assertEqual(response.json()["data"], expected)

    def test_get_posts_with_comment(self):
        post1 = self.posts[0]
        post2 = self.posts[1]
        comments = PostComment.objects.bulk_create(
            [
                PostComment(
                    post=post1,
                    comment="this is a comment",
                    commented_by=self.users[0],
                ),
                PostComment(
                    post=post1,
                    comment="this is a comment",
                    commented_by=self.users[1],
                ),
                PostComment(
                    post=post2,
                    comment="this is a comment",
                    commented_by=self.users[2],
                ),
                PostComment(
                    post=post2,
                    comment="this is a comment",
                    commented_by=self.users[3],
                ),
            ]
        )
        post1_comments = PostComment.objects.filter(post=self.posts[0]).all()
        post1_comments = json.dumps(
            PostCommentSerializer(post1_comments, many=True).data
        )
        response = self.client.get(
            reverse("post_detail", args=[1]), **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        expected = {
            "error": None,
            "msg": "OK",
            "data": {
                "id": self.posts[0].pk,
                "title": self.posts[0].title,
                "description": self.posts[0].description,
                "created_at": self.posts[0]
                .created_at.isoformat()
                .replace("+00:00", "Z"),
                "comments": json.loads(post1_comments),
                "likes": 0,
            },
        }
        self.assertEqual(response.json(), expected)
