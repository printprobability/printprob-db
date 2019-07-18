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
            list(res.data.keys()),
            ["pk", "book", "sequence", "primary_image", "pref_image_url"],
        )

    def test_noaccess(self):
        noaccess(self)


class PageViewTest(TestCase):
    """Test suite for Page views"""

    fixtures = ["test.json"]

    ENDPOINT = "/pages/"
    OBJCOUNT = models.Page.objects.count()
    OBJ1 = models.Page.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            [
                "pk",
                "created_by_run",
                "spread",
                "book_title",
                "side",
                "x_min",
                "x_max",
                "pref_image_url",
            ],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "created_by_run",
                "spread",
                "book_title",
                "side",
                "x_min",
                "x_max",
                "lines",
                "primary_image",
                "pref_image_url",
            ],
        )
        self.assertEqual(res.data["pk"], self.STR1)
        self.assertIsInstance(res.data["lines"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        spread = models.Spread.objects.first()
        image = models.Image.objects.first().pk
        run = models.Run.objects.first().pk
        # Posting an existing page fails
        failres = self.client.post(
            self.ENDPOINT,
            data={
                "spread": spread.pk,
                "side": "l",
                "primary_image": image,
                "x_min": 0,
                "x_max": 0,
            },
        )
        self.assertEqual(failres.status_code, 400)
        # Delete it and then try again
        getextant = self.client.get(
            self.ENDPOINT, params={"book": spread.book.pk, "spread": spread.pk}
        )
        delres = self.client.delete(
            self.ENDPOINT + str(getextant.data["results"][0]["pk"]) + "/"
        )
        self.assertEqual(delres.status_code, 204)
        res = self.client.post(
            self.ENDPOINT,
            data={
                "spread": spread.pk,
                "created_by_run": run,
                "side": "l",
                "primary_image": image,
                "x_min": 0,
                "x_max": 0,
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "created_by_run",
                "spread",
                "side",
                "x_min",
                "x_max",
                "primary_image",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class LineViewTest(TestCase):
    """Test suite for Page views"""

    fixtures = ["test.json"]

    ENDPOINT = "/lines/"
    OBJCOUNT = models.Line.objects.count()
    OBJ1 = models.Line.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            ["pk", "created_by_run", "page", "sequence", "y_min", "y_max"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "created_by_run",
                "page",
                "sequence",
                "primary_image",
                "characters",
                "y_min",
                "y_max",
                "pref_image_url",
            ],
        )
        self.assertEqual(res.data["pk"], self.STR1)
        self.assertIsInstance(res.data["characters"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        page = models.Page.objects.first().pk
        image = models.Image.objects.first().pk
        run = models.Run.objects.first().pk
        # Posting an existing page fails
        res = self.client.post(
            self.ENDPOINT,
            data={
                "page": page,
                "created_by_run": run,
                "sequence": 100,
                "primary_image": image,
                "y_min": 0,
                "y_max": 0,
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "created_by_run",
                "page",
                "sequence",
                "y_min",
                "y_max",
                "primary_image",
                "pref_image_url",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class CharacterViewTest(TestCase):
    """Test suite for Page views"""

    fixtures = ["test.json"]

    ENDPOINT = "/characters/"
    OBJCOUNT = models.Character.objects.count()
    OBJ1 = models.Character.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            [
                "pk",
                "created_by_run",
                "line",
                "sequence",
                "x_min",
                "x_max",
                "character_class",
                "class_probability",
                "primary_image",
                "pref_image_url",
            ],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "created_by_run",
                "line",
                "sequence",
                "primary_image",
                "x_min",
                "x_max",
                "character_class",
                "class_probability",
                "pref_image_url",
            ],
        )
        self.assertEqual(res.data["pk"], self.STR1)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        line = models.Line.objects.first().pk
        image = models.Image.objects.first().pk
        run = models.Run.objects.first().pk
        char_class = models.CharacterClass.objects.first().pk
        res = self.client.post(
            self.ENDPOINT,
            data={
                "line": line,
                "created_by_run": run,
                "sequence": 100,
                "primary_image": image,
                "x_min": 0,
                "x_max": 0,
                "character_class": char_class,
                "class_probability": 0.7,
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "pk",
                "created_by_run",
                "line",
                "sequence",
                "x_min",
                "x_max",
                "character_class",
                "class_probability",
                "primary_image",
                "pref_image_url",
            ],
        )

    def test_noaccess(self):
        noaccess(self)
