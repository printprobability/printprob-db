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
    self.assertEqual(self.client.delete(self.ENDPOINT).status_code, 403)


def as_auth(func):
    def auth_client(self):
        token = Token.objects.get(user__username="root")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        return func(self)

    return auth_client


class RootViewTest(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)

    def test_noaccess(self):
        noaccess(self)


class PageRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/pages/"
    OBJCOUNT = models.PageRun.objects.count()
    OBJ1 = models.PageRun.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
                "pages",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
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
        res = self.client.post(
            self.ENDPOINT,
            data={
                "book": book,
                "params": "foo",
                "script_path": "bar",
                "script_md5": "c08fa2dc-6ebc-4c0e-a48e-efdcea56ba45",
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class LineRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/lines/"
    OBJCOUNT = models.LineRun.objects.count()
    OBJ1 = models.LineRun.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
                "lines",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["lines"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        book = models.Book.objects.first().pk
        res = self.client.post(
            self.ENDPOINT,
            data={
                "book": book,
                "params": "foo",
                "script_path": "bar",
                "script_md5": "c08fa2dc-6ebc-4c0e-a48e-efdcea56ba45",
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class LineGroupRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/line_groups/"
    OBJCOUNT = models.LineGroupRun.objects.count()
    OBJ1 = models.LineGroupRun.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
                "linegroups",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["linegroups"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        book = models.Book.objects.first().pk
        res = self.client.post(
            self.ENDPOINT,
            data={
                "book": book,
                "params": "foo",
                "script_path": "bar",
                "script_md5": "c08fa2dc-6ebc-4c0e-a48e-efdcea56ba45",
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class CharacterRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/characters/"
    OBJCOUNT = models.CharacterRun.objects.count()
    OBJ1 = models.CharacterRun.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
                "characters",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["characters"], list)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        book = models.Book.objects.first().pk
        res = self.client.post(
            self.ENDPOINT,
            data={
                "book": book,
                "params": "foo",
                "script_path": "bar",
                "script_md5": "c08fa2dc-6ebc-4c0e-a48e-efdcea56ba45",
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "params",
                "script_path",
                "script_md5",
                "date_started",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class BookViewTest(TestCase):

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
            ["url", "estc", "vid", "publisher", "title", "pdf", "n_spreads"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "estc",
                "vid",
                "publisher",
                "title",
                "pdf",
                "n_spreads",
                "spreads",
                "most_recent_runs",
                "all_runs",
            ],
        )
        self.assertEqual(res.data["estc"], self.OBJ1)
        self.assertIsInstance(res.data["spreads"], list)
        self.assertIsInstance(res.data["most_recent_runs"], dict)
        self.assertIsInstance(res.data["all_runs"], dict)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        res = self.client.post(
            self.ENDPOINT,
            data={"estc": 101, "vid": 202, "title": "foobar", "pdf": "foobar"},
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()), ["url", "estc", "vid", "publisher", "title", "pdf"]
        )

    def test_noaccess(self):
        noaccess(self)


class SpreadViewTest(TestCase):
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
            ["url", "id", "book", "sequence", "image", "pref_image_url"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "book",
                "sequence",
                "image",
                "pref_image_url",
                "most_recent_pages",
                "pages",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
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
            self.ENDPOINT, data={"book": book, "sequence": 100, "image": image}
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()), ["url", "id", "book", "sequence", "image"]
        )

    def test_noaccess(self):
        noaccess(self)


class PageViewTest(TestCase):

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
                "url",
                "id",
                "created_by_run",
                "spread",
                "side",
                "x_min",
                "x_max",
                "image",
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
                "url",
                "id",
                "created_by_run",
                "spread",
                "side",
                "x_min",
                "x_max",
                "image",
                "pref_image_url",
                "most_recent_lines",
                "lines",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
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
        run = models.PageRun.objects.first().pk
        # Posting an existing page fails
        failres = self.client.post(
            self.ENDPOINT,
            data={
                "spread": spread.pk,
                "created_by_run": run,
                "side": "l",
                "image": image,
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
            self.ENDPOINT + str(getextant.data["results"][0]["id"]) + "/"
        )
        self.assertEqual(delres.status_code, 204)
        res = self.client.post(
            self.ENDPOINT,
            data={
                "spread": spread.pk,
                "created_by_run": run,
                "side": "l",
                "image": image,
                "x_min": 0,
                "x_max": 0,
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "created_by_run",
                "spread",
                "side",
                "x_min",
                "x_max",
                "image",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class LineViewTest(TestCase):

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
            ["url", "id", "created_by_run", "page", "sequence", "y_min", "y_max"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "created_by_run",
                "page",
                "sequence",
                "image",
                "y_min",
                "y_max",
                "pref_image_url",
                "most_recent_characters",
                "characters",
                "most_recent_linegroups",
                "linegroups",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)
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
        run = models.LineRun.objects.first().pk
        res = self.client.post(
            self.ENDPOINT,
            data={
                "page": page,
                "created_by_run": run,
                "sequence": 100,
                "image": image,
                "y_min": 0,
                "y_max": 0,
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()),
            [
                "url",
                "id",
                "created_by_run",
                "page",
                "sequence",
                "y_min",
                "y_max",
                "image",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class CharacterViewTest(TestCase):

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
                "url",
                "id",
                "created_by_run",
                "line",
                "sequence",
                "x_min",
                "x_max",
                "character_class",
                "class_probability",
                "image",
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
                "url",
                "id",
                "created_by_run",
                "line",
                "sequence",
                "image",
                "x_min",
                "x_max",
                "character_class",
                "class_probability",
                "pref_image_url",
            ],
        )
        self.assertEqual(res.data["id"], self.STR1)

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
        run = models.CharacterRun.objects.first().pk
        char_class = models.CharacterClass.objects.first().pk
        res = self.client.post(
            self.ENDPOINT,
            data={
                "line": line,
                "created_by_run": run,
                "sequence": 100,
                "image": image,
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
                "url",
                "id",
                "created_by_run",
                "line",
                "sequence",
                "x_min",
                "x_max",
                "character_class",
                "class_probability",
                "image",
            ],
        )

    def test_noaccess(self):
        noaccess(self)


class ImageViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/images/"
    OBJCOUNT = models.Image.objects.count()
    OBJ1 = models.Image.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(
            list(res.data["results"][0].keys()),
            ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"],
        )

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()), ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"]
        )
        self.assertEqual(res.data["id"], self.STR1)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        res = self.client.post(
            self.ENDPOINT,
            data={
                "jpg": "/foo/bar.jpg",
                "tif": "/foo/bat.tiff",
                "jpg_md5": "c08fa2dc-6ebc-4c0e-a48e-efdcea56ba45",
                "tif_md5": "c08fa2dc-6ebc-4c0e-a48e-efdcea56ba45",
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            list(res.data.keys()), ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"]
        )

    def test_noaccess(self):
        noaccess(self)


class CharacterClassViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/character_classes/"
    OBJCOUNT = models.CharacterClass.objects.count()
    OBJ1 = models.CharacterClass.objects.first().pk
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        self.assertEqual(list(res.data["results"][0].keys()), ["url", "classname"])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.data.keys()), ["url", "classname"])
        self.assertEqual(res.data["classname"], self.STR1)

    @as_auth
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth
    def test_post(self):
        res = self.client.post(self.ENDPOINT, data={"classname": "zed"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(list(res.data.keys()), ["url", "classname"])
        constrainres = self.client.post(self.ENDPOINT, data={"classname": "a"})
        self.assertEqual(constrainres.status_code, 400)

    def test_noaccess(self):
        noaccess(self)
