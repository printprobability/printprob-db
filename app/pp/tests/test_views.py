from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from pp import models
import re

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
    OBJCOUNT = models.Run.objects.count()
    OBJ1 = models.Run.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()), ["pk", "date_started", "notes"]
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
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
        self.assertEqual(res.data["pk"], self.STR1)
        self.assertEqual(res.data["pages_created"][0]["created_by_run"], self.OBJ1)
        self.assertEqual(res.data["lines_created"][0]["created_by_run"], self.OBJ1)
        self.assertEqual(res.data["characters_created"][0]["created_by_run"], self.OBJ1)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        res = self.client.post(self.ENDPOINT, data={"notes": "foobar"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(list(res.data.keys()), ["pk", "date_started", "notes"])
        self.assertEqual(res.data["notes"], "foobar")

    def test_noaccess(self):
        noaccess(self)


class BookViewTest(TestCase):
    """Test suite for Book views"""

    fixtures = ["test.json"]

    ENDPOINT = "/books/"
    OBJCOUNT = models.Book.objects.count()
    OBJ1 = models.Book.objects.first().estc
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            ["estc", "vid", "publisher", "title", "pdf"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            ["estc", "vid", "publisher", "title", "pdf", "spreads"],
        )
        self.assertEqual(res.data["estc"], self.OBJ1)
        self.assertIsInstance(res.data["spreads"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        res = self.client.post(
            self.ENDPOINT, data={"estc": 101, "vid": 202, "title": "foobar"}
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()), ["estc", "vid", "publisher", "title", "pdf"]
        )

    def test_noaccess(self):
        noaccess(self)

class SpreadViewTest(TestCase):
    """Test suite for Spread views"""

    fixtures = ["test.json"]

    ENDPOINT = "/spreads/"
    OBJCOUNT = models.Spread.objects.count()
    OBJ1 = models.Spread.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            ["pk", "book", "sequence", "pref_image_url"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            ["pk", "book", "sequence", "primary_image", "pref_image_url", "pages"],
        )
        self.assertEqual(res.data["pk"], self.STR1)
        self.assertIsInstance(res.data["pages"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        book = models.Book.objects.first().pk
        image = models.Image.objects.first().pk
        res = self.client.post(
            self.ENDPOINT, data={"book": book, "sequence": 100, "primary_image": image}
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()), ["pk", "book", "sequence", "primary_image", "pref_image_url"]
        )

    def test_noaccess(self):
        noaccess(self)
