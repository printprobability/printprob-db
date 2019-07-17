from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from pp import models

# Create your tests here.


def noaccess(self):
    """Expect no unauthorized access to the endpoint"""
    self.assertEqual(self.client.get(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.post(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.put(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.patch(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.delete(self.ENDPOINT).status_code, 403)


def as_auth(func):
    def auth_client(self):
        token = Token.objects.get(user__username="root")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        return func(self)

    return auth_client


class RootViewTest(TestCase):
    """Test suite for Root view"""

    fixtures = ["test.json"]

    ENDPOINT = "/"

    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "runs",
                "books",
                "spreads",
                "pages",
                "lines",
                "characters",
                "images",
                "character_classes",
            ],
        )

    def test_get_detail(self):
        pass

    def test_post(self):
        res = self.client.post(self.ENDPOINT)
        self.assertEqual(res.status_code, 405)

    def test_put(self):
        res = self.client.put(self.ENDPOINT)
        self.assertEqual(res.status_code, 405)

    def test_patch(self):
        res = self.client.patch(self.ENDPOINT)
        self.assertEqual(res.status_code, 405)

    def test_delete(self):
        res = self.client.delete(self.ENDPOINT)
        self.assertEqual(res.status_code, 405)


class RunViewTest(TestCase):
    """Test suite for Run views"""

    fixtures = ["test.json"]

    ENDPOINT = "/runs/"
    RUN1 = str(models.Run.objects.first().pk)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(
            list(res.data["results"][0].keys()), ["pk", "date_started", "notes"]
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.RUN1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "date_started",
                "notes",
                "pages_created",
                "lines_created",
                "characters_created",
            ],
        )
        self.assertEqual(res.data["pk"], self.RUN1)
        self.assertEqual(res.data["pages_created"][0]["created_by_run"], self.RUN1)
        self.assertEqual(res.data["lines_created"][0]["created_by_run"], self.RUN1)
        self.assertEqual(res.data["characters_created"][0]["created_by_run"], self.RUN1)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.RUN1)
        self.assertEqual(res.status_code, 200)
        delres = self.client.get(self.ENDPOINT + self.RUN1)
        self.assertEqual(res.status_code, 301)

    @as_auth
    def test_post(self):
        res = self.client.post(self.ENDPOINT, data={"notes": "foobar"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(list(res.data.keys()), ["pk", "date_started", "notes"])
        self.assertEqual(res.data["notes"], "foobar")

    def test_noaccess(self):
        noaccess(self)
