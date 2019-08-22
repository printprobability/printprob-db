from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from pp import models

# Create your tests here.


def noaccess(self):
    """Expect no unauthorized access to the endpoint"""
    self.assertEqual(self.client.get(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.post(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.delete(self.ENDPOINT).status_code, 403)


def as_auth(func):
    def auth_client(self):
        token = "e48806a81d59ef7495d25731d74486388d9be2f6"
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
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
    OBJCOUNT = 2
    STR1 = "3deb2d61-0997-4a0c-861a-e7df8b27e49e"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "pages",
        ]:
            self.assertIn(k, res.data)
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
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/lines/"
    OBJCOUNT = 2
    STR1 = "1fad0375-7b4f-4cb8-ba36-ea6db62a8991"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "lines",
        ]:
            self.assertIn(k, res.data)
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
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineGroupRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/linegroups/"
    OBJCOUNT = 2
    STR1 = "388054c9-154e-464c-bcc7-ccdeb8aeb026"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "linegroups",
        ]:
            self.assertIn(k, res.data)
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
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class CharacterRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/runs/characters/"
    OBJCOUNT = 3
    STR1 = "b878db65-e8ad-4a85-89c4-883a9904b85e"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "characters",
        ]:
            self.assertIn(k, res.data)
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
        for k in [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class BookViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/books/"
    OBJCOUNT = 2
    OBJ1 = 1234
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "eebo",
            "vid",
            "publisher",
            "title",
            "pdf",
            "n_spreads",
            "cover_page",
        ]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("jpg", res.data["results"][0]["cover_page"]["image"])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "eebo",
            "vid",
            "publisher",
            "title",
            "pdf",
            "n_spreads",
            "spreads",
            "most_recent_runs",
            "all_runs",
            "most_recent_pages",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["eebo"], self.OBJ1)
        self.assertIsInstance(res.data["spreads"], list)
        self.assertIsInstance(res.data["most_recent_runs"], dict)
        self.assertIsInstance(res.data["all_runs"], dict)
        self.assertIsInstance(res.data["most_recent_pages"], list)
        self.assertIsInstance(res.data["most_recent_pages"][0], dict)
        self.assertEquals(res.data["most_recent_pages"][0]["side"], "l")
        self.assertEquals(res.data["most_recent_pages"][1]["side"], "r")
        self.assertLess(
            res.data["most_recent_pages"][0]["spread_sequence"],
            res.data["most_recent_pages"][-1]["spread_sequence"],
        )
        self.assertIn("jpg", res.data["most_recent_pages"][0]["image"])

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
            data={"eebo": 101, "vid": 202, "title": "foobar", "pdf": "foobar"},
        )
        self.assertEqual(res.status_code, 201)
        for k in ["url", "eebo", "vid", "publisher", "title", "pdf"]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class SpreadViewTest(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = "/spreads/"
    OBJCOUNT = 4
    STR1 = "d8d28a21-bb26-4ed7-b89d-368f7e32b142"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "book", "sequence", "image"]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("jpg", res.data["results"][0]["image"])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "book",
            "sequence",
            "image",
            "most_recent_pages",
            "pages",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["pages"], list)
        self.assertIn("jpg", res.data["most_recent_pages"][0]["image"])

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
        for k in ["url", "id", "book", "sequence", "image"]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class PageViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/pages/"
    OBJCOUNT = 8
    STR1 = "2123a623-fd14-4b54-bada-060d117e5a68"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "id",
            "created_by_run",
            "spread",
            "spread_sequence",
            "side",
            "x_min",
            "x_max",
            "image",
        ]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("jpg", res.data["results"][0]["image"])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
            "most_recent_lines",
            "lines",
        ]:
            self.assertIn(k, res.data.keys())
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["lines"], list)
        self.assertIn("jpg", res.data["image"])

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
        run = spread.pages.first().created_by_run.pk
        # Posting an existing page fails
        failres = self.client.post(
            self.ENDPOINT,
            data={
                "spread": "d8d28a21-bb26-4ed7-b89d-368f7e32b142",
                "created_by_run": "41ddeb86-e83d-4768-96dd-f2ecfc2f80c5",
                "side": "l",
                "image": "044b10ec-61fc-438f-80c9-678e79c31169",
                "x_min": 0,
                "x_max": 0,
            },
        )
        self.assertEqual(failres.status_code, 400)
        # Delete it and then try again
        getextant = self.client.get(
            self.ENDPOINT,
            {
                "book": 1234,
                "spread_sequence": 0,
                "created_by_run": "41ddeb86-e83d-4768-96dd-f2ecfc2f80c5",
                "side": "l",
            },
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
        for k in [
            "url",
            "id",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/lines/"
    OBJCOUNT = 24
    STR1 = "8a9c2b46-f22f-4d21-8327-1078fb02dd4f"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "created_by_run", "page", "sequence", "y_min", "y_max"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
            "url",
            "id",
            "created_by_run",
            "page",
            "sequence",
            "image",
            "y_min",
            "y_max",
            "most_recent_characters",
            "characters",
            "most_recent_linegroups",
            "linegroups",
        ]:
            self.assertIn(k, res.data)
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
        res = self.client.post(
            self.ENDPOINT,
            data={
                "page": "2123a623-fd14-4b54-bada-060d117e5a68",
                "created_by_run": "1fad0375-7b4f-4cb8-ba36-ea6db62a8991",
                "sequence": 100,
                "image": "044b10ec-61fc-438f-80c9-678e79c31169",
                "y_min": 0,
                "y_max": 0,
            },
        )
        self.assertEqual(res.status_code, 201)
        for k in [
            "url",
            "id",
            "created_by_run",
            "page",
            "sequence",
            "y_min",
            "y_max",
            "image",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineGroupViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/linegroups/"
    OBJCOUNT = 16
    STR1 = "0f7c4848-82e3-4243-9ed3-52d78eae384e"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "page", "created_by_run", "lines"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in ["url", "id", "page", "created_by_run", "lines"]:
            self.assertIn(k, res.data)
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
        res = self.client.post(
            self.ENDPOINT,
            data={
                "page": "2123a623-fd14-4b54-bada-060d117e5a68",
                "created_by_run": "388054c9-154e-464c-bcc7-ccdeb8aeb026",
                "lines": ["8a9c2b46-f22f-4d21-8327-1078fb02dd4f"],
            },
        )
        self.assertEqual(res.status_code, 201)
        for k in ["url", "id", "page", "created_by_run", "lines"]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class CharacterViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/characters/"
    OBJCOUNT = 72
    STR1 = "dc722c25-e1ee-42c8-8e16-c04550b9ada4"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in [
            "url",
            "id",
            "created_by_run",
            "book",
            "spread",
            "page",
            "line",
            "sequence",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "image",
        ]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("eebo", res.data["results"][0]["book"])
        self.assertIn("sequence", res.data["results"][0]["spread"])
        self.assertIn("side", res.data["results"][0]["page"])
        self.assertIn("sequence", res.data["results"][0]["line"])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in [
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
        ]:
            self.assertIn(k, res.data)
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
                "line": "8a9c2b46-f22f-4d21-8327-1078fb02dd4f",
                "created_by_run": "b878db65-e8ad-4a85-89c4-883a9904b85e",
                "sequence": 100,
                "image": "044b10ec-61fc-438f-80c9-678e79c31169",
                "x_min": 0,
                "x_max": 0,
                "character_class": "a",
                "class_probability": 0.7,
            },
        )
        self.assertEqual(res.status_code, 201)
        for k in [
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
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class ImageViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/images/"
    OBJCOUNT = 108
    STR1 = "044b10ec-61fc-438f-80c9-678e79c31169"

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.data.keys()), ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5", "web_url"]
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
        for k in ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class CharacterClassViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = "/character_classes/"
    OBJCOUNT = 3
    OBJ1 = "a"
    STR1 = str(OBJ1)

    @as_auth
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "classname"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in ["url", "classname"]:
            self.assertIn(k, res.data)
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
        for k in ["url", "classname"]:
            self.assertIn(k, res.data)
        constrainres = self.client.post(self.ENDPOINT, data={"classname": "a"})
        self.assertEqual(constrainres.status_code, 400)

    def test_noaccess(self):
        noaccess(self)
