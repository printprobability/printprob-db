from django.test import TestCase
from django.core.management import call_command
from pp import models
import tempfile
import json

# Create your tests here.


class RootViewTest(TestCase):
    fixtures = ["test.json"]

    def test_bulk_update(self):
        with tempfile.TemporaryDirectory() as tdir:
            pages = {
                "pages": [
                    {
                        "id": "0a6da1e8-7d73-419f-8edc-367af9560e13",
                        "label": "(60468) New most build detail we week ... p. 0-r",
                        "tif": "/baby/keep/piece/actually.tif",
                        "sequence": 5,
                        "side": "r",
                        "x": 21.0,
                        "y": 458.0,
                        "w": 1.0,
                        "h": 257.0,
                        "rot1": 441.0,
                        "rot2": 349.0,
                        "created_by_run": "20f9a4ac-17d3-4b6d-80c7-2388617891bb",
                        "filename": "/billion/cause/throughout/respond.tif",
                    },
                    {
                        "id": "1bd244dc-ed08-4f81-a29d-886301054693",
                        "label": "(273837) Police these rich stage throug... p. 2-r",
                        "tif": "/food/discover/pressure/break.tif",
                        "sequence": 8,
                        "side": "r",
                        "x": 291.0,
                        "y": 391.0,
                        "w": 346.0,
                        "h": 404.0,
                        "rot1": 27.0,
                        "rot2": 409.0,
                        "created_by_run": "27b3f412-3852-4403-af97-266d362b94e7",
                        "filename": "/billion/cause/throughout/respond.tif",
                    },
                ]
            }

            json.dump(pages, open(tdir + "/pages.json", "w"))

            lines = {
                "lines": [
                    {
                        "id": "03b7d45e-b92f-4f5f-948a-7574c442f92a",
                        "label": "(24668) Collection eat social wear cau... p. 2-r l. 1",
                        "page_id": "1bd244dc-ed08-4f81-a29d-886301054693",
                        "sequence": 5,
                        "y_start": 250,
                        "y_end": 6,
                        "created_by_run": "0c821b81-9076-4de9-a518-878662b95ef9",
                    }
                ]
            }

            json.dump(lines, open(tdir + "/lines.json", "w"))

            characters = {
                "chars": [
                    {
                        "id": "09d02aa1-3247-4651-9ace-6df521a907b5",
                        "label": "(24668) Collection eat social wear cau... p. 2-l l. 2 c. 0",
                        "line_id": "03b7d45e-b92f-4f5f-948a-7574c442f92a",
                        "sequence": 0,
                        "x_start": 264,
                        "x_end": 243,
                        "y_start": None,
                        "y_end": None,
                        "character_class": "l",
                        "human_character_class": None,
                        "logprob": 0.08064489626573179,
                        "created_by_run": "2936e490-f669-4f45-8afd-6f70f46e9dc0",
                        "exposure": 0,
                        "offset": 0,
                        "damage_score": 0.08,
                        "breakage_types": [],
                    },
                    {
                        "id": "0b1f25f9-e2d0-484a-ab52-7301fdbc76c8",
                        "label": "(24668) Collection eat social wear cau... p. 2-r l. 2 c. 1",
                        "line_id": "03b7d45e-b92f-4f5f-948a-7574c442f92a",
                        "sequence": 1,
                        "x_start": 550,
                        "x_end": 220,
                        "y_start": None,
                        "y_end": None,
                        "character_class": "E",
                        "human_character_class": None,
                        "logprob": 0.03945806088182946,
                        "created_by_run": "2936e490-f669-4f45-8afd-6f70f46e9dc0",
                        "exposure": 0,
                        "offset": 0,
                        "damage_score": 0.24,
                        "breakage_types": [],
                    },
                ]
            }

            json.dump(characters, open(tdir + "/chars.json", "w"))

            self.assertEqual(
                models.Page.objects.get(
                    id="0a6da1e8-7d73-419f-8edc-367af9560e13"
                ).sequence,
                1,
            )
            self.assertEqual(
                models.Page.objects.get(
                    id="1bd244dc-ed08-4f81-a29d-886301054693",
                ).sequence,
                5,
            )
            call_command(
                "bulk_update", book_id="4d4b67c8-70a7-431c-9fe2-abaef50217cd", json=tdir
            )
            self.assertEqual(
                models.Page.objects.get(
                    id="0a6da1e8-7d73-419f-8edc-367af9560e13"
                ).sequence,
                5,
            )
            self.assertEqual(
                models.Page.objects.get(
                    id="1bd244dc-ed08-4f81-a29d-886301054693",
                ).sequence,
                8,
            )
