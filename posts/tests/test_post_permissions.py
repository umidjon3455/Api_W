from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ContentCreationPermissionTests(APITestCase):
    def test_anonymous_user_cannot_create_post(self):
        response = self.client.post(
            reverse("post-list-create"),
            {"title": "Test post", "content": "Test content"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_create_comment(self):
        response = self.client.post(
            reverse("comment-list-create", kwargs={"post_id": 1}),
            {"content": "Test comment"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
