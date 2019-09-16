from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.management import call_command
from pp import models

# Create your tests here.


def noaccess(self):
    """Expect no unauthorized access to the endpoint"""
    self.assertEqual(self.client.get(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.post(self.ENDPOINT).status_code, 403)
    self.assertEqual(self.client.delete(self.ENDPOINT).status_code, 403)


def as_auth(username="root"):
    def as_auth_name(func):
        """
        Run a test using an APIClient authorized with a particular username. Defaults to "root"
        """
        def auth_client(self):
            token = Token.objects.get(user__username=username)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
            return func(self)
        return auth_client
    return as_auth_name

class RootViewTest(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = reverse("api-root")

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)

    def test_noaccess(self):
        noaccess(self)


class PageRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = reverse("pagerun-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.PageRun.objects.count()
        cls.OBJ1 = models.PageRun.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["pages"], list)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = reverse("linerun-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.LineRun.objects.count()
        cls.OBJ1 = models.LineRun.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["lines"], list)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineGroupRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = reverse("linegrouprun-list")

    @classmethod
    def setUp(cls):
        cls.OBJCOUNT = models.LineGroupRun.objects.count()
        cls.OBJ1 = models.LineGroupRun.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["linegroups"], list)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class CharacterRunTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = reverse("characterrun-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.CharacterRun.objects.count()
        cls.OBJ1 = models.CharacterRun.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["book"], dict)
        self.assertIsInstance(res.data["characters"], list)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class BookViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = reverse("book-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Book.objects.count()
        cls.OBJ1 = models.Book.objects.first().eebo
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("jpg", res.data["results"][0]["cover_page"]["image"])

    @as_auth()
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
            "label",
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

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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

    ENDPOINT = reverse("spread-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Spread.objects.count()
        cls.OBJ1 = models.Spread.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "book", "sequence", "image"]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("jpg", res.data["results"][0]["image"])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["pages"], list)
        self.assertIn("jpg", res.data["most_recent_pages"][0]["image"])

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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

    ENDPOINT = reverse("page-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Page.objects.count()
        cls.OBJ1 = models.Page.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("jpg", res.data["results"][0]["image"])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data.keys())
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["lines"], list)
        self.assertIn("jpg", res.data["image"])

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
    def test_post(self):
        spread = models.Spread.objects.first()
        image = models.Image.objects.first().pk
        run = spread.pages.first().created_by_run.pk
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
            self.ENDPOINT,
            {
                "book": spread.book.pk,
                "spread_sequence": spread.sequence,
                "created_by_run": run,
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
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = reverse("line-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Line.objects.count()
        cls.OBJ1 = models.Line.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "created_by_run", "page", "sequence", "y_min", "y_max"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["characters"], list)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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
        for k in [
            "url",
            "id",
            "created_by_run",
            "page",
            "sequence",
            "y_min",
            "y_max",
            "image",
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class LineGroupViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = reverse("linegroup-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.LineGroup.objects.count()
        cls.OBJ1 = models.LineGroup.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "page", "created_by_run", "lines"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in ["url", "id", "page", "created_by_run", "lines"]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)
        self.assertIsInstance(res.data["lines"], list)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
    def test_post(self):
        page = models.Page.objects.first()
        image = models.Image.objects.first().pk
        run = models.LineGroupRun.objects.first().pk
        lines = page.lines.all()[:1]
        res = self.client.post(
            self.ENDPOINT,
            data={
                "page": page.pk,
                "created_by_run": run,
                "lines": [l.pk for l in lines],
            },
        )
        self.assertEqual(res.status_code, 201)
        for k in ["url", "id", "page", "created_by_run", "lines"]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class CharacterViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = reverse("character-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Character.objects.count()
        cls.OBJ1 = models.Character.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data["results"][0])
        self.assertIn("eebo", res.data["results"][0]["book"])
        self.assertIn("sequence", res.data["results"][0]["spread"])
        self.assertIn("side", res.data["results"][0]["page"])
        self.assertIn("sequence", res.data["results"][0]["line"])

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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
            "label",
        ]:
            self.assertIn(k, res.data)

    def test_noaccess(self):
        noaccess(self)


class ImageViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = reverse("image-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Image.objects.count()
        cls.OBJ1 = models.Image.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5", "web_url"]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["id"], self.STR1)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
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

    ENDPOINT = reverse("characterclass-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.CharacterClass.objects.count()
        cls.OBJ1 = models.CharacterClass.objects.first().pk
        cls.STR1 = str(cls.OBJ1)

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "classname"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in ["url", "classname"]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["classname"], self.STR1)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
    def test_post(self):
        res = self.client.post(self.ENDPOINT, data={"classname": "zed"})
        self.assertEqual(res.status_code, 201)
        for k in ["url", "classname"]:
            self.assertIn(k, res.data)
        constrainres = self.client.post(self.ENDPOINT, data={"classname": "a"})
        self.assertEqual(constrainres.status_code, 400)

    def test_noaccess(self):
        noaccess(self)

class DocTestCase(TestCase):
    fixtures = ["test.json"]

    ENDPOINT = reverse("schema-redoc")

    def test_get_docs(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)


class CharacterGroupingClassViewTest(TestCase):

    fixtures = ["test.json"]

    ENDPOINT = reverse("charactergrouping-list")

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.CharacterGrouping.objects.count()
        cls.SUSANCOUNT = models.CharacterGrouping.objects.filter(created_by__username="susan").count()
        cls.OBJ1 = models.CharacterGrouping.objects.first()
        cls.STR1 = str(cls.OBJ1.pk)
        cls.CHARS_1 = models.Character.objects.all()[1:5].values_list("id", flat=True)
        cls.CHARS_2 = models.Character.objects.all()[6:8].values_list("id", flat=True)
        cls.CHARS_ORIG = cls.OBJ1.characters.all().values_list("id", flat=True)

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "label", "created_by", "date_created", "notes", "characters"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
    def test_get_filter(self):
        res = self.client.get(self.ENDPOINT + "?created_by=susan")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.SUSANCOUNT)
        for k in ["url", "id", "label", "created_by", "date_created", "notes"]:
            self.assertIn(k, res.data["results"][0])
        for entry in res.data["results"]:
            self.assertEqual(entry["created_by"], "susan")

    @as_auth()
    def test_get(self):
        res = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], self.OBJCOUNT)
        for k in ["url", "id", "label", "created_by", "date_created", "notes"]:
            self.assertIn(k, res.data["results"][0])

    @as_auth()
    def test_get_detail(self):
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        for k in ["url", "id", "label", "created_by", "date_created","notes", "characters"]:
            self.assertIn(k, res.data)
        self.assertIsInstance(res.data["characters"][0], dict)

    @as_auth()
    def test_delete(self):
        res = self.client.delete(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 204)
        delres = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(delres.status_code, 404)

    @as_auth()
    def test_post_root(self):
        res = self.client.post(self.ENDPOINT, data={"label": "foo", "notes": "bar", "characters": self.CHARS_1})
        self.assertEqual(res.status_code, 201)
        for k in ["url", "id", "label", "created_by", "date_created","notes", "characters"]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["created_by"], "root")
        for char_id in res.data["characters"]:
            self.assertIn(char_id, self.CHARS_1)

    @as_auth(username="susan")
    def test_post_susan(self):
        res = self.client.post(self.ENDPOINT, data={"label": "foo", "notes": "bar", "characters": self.CHARS_2})
        self.assertEqual(res.status_code, 201)
        for k in ["url", "id", "label", "created_by", "date_created","notes", "characters"]:
            self.assertIn(k, res.data)
        self.assertEqual(res.data["created_by"], "susan")
        for char_id in res.data["characters"]:
            self.assertIn(char_id, self.CHARS_2)

    @as_auth()
    def test_add_chars(self):
        patch_res = self.client.patch(self.ENDPOINT + self.STR1 + "/add_characters/", data = {"characters": self.CHARS_2})
        self.assertEqual(patch_res.status_code, 200)
        res = self.client.get(self.ENDPOINT + self.STR1 + "/")
        self.assertEqual(res.status_code, 200)
        #print([a["id"] for a in res.data["characters"]])
        all_ids = [char["id"] for char in res.data["characters"]]
        target_ids = [str(i) for i in list(self.CHARS_ORIG) + list(self.CHARS_2)]
        for char_id in all_ids:
            self.assertIn(char_id, target_ids)

    def test_noaccess(self):
        noaccess(self)


class DocTestCase(TestCase):
    fixtures = ["test.json"]

    @classmethod
    def setUpTestData(cls):
        cls.OBJCOUNT = models.Image.objects.count()

    def test_wipe_hanging_images(self):
        call_command("wipe_hanging_images")
        self.assertLess(models.Image.objects.count(), self.OBJCOUNT)
