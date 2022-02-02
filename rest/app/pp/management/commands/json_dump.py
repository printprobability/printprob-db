from django.conf import settings
from django.core.management.base import BaseCommand
from pp import models
from pp import static_serializers as serializers
import json
from tqdm import tqdm
from uuid import UUID

# Baseurl for static site
settings.IMAGE_BASEURL = "/img/iiif"


def to_camel_case(snake_str):
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])


def camel_keys(d: dict):
    """
    Rename all the keys in a dictionary from snake_case to camelCase
    """
    newdict = {}
    for k in d.keys():
        newkey = to_camel_case(k)
        newdict[newkey] = d[k]
        if isinstance(newdict[newkey], dict):
            newdict[newkey] = camel_keys(newdict[newkey])
    return newdict


class UUIDEncoder(json.JSONEncoder):
    """
    Get the string hex of the UUID when parsing into JSON
    from https://stackoverflow.com/a/48159596/3547541
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Command(BaseCommand):
    help = "Serialize data to JSON documents"

    def handle(self, *args, **options):
        OUTPUT_PATH = "serialized_json"

        groupings = models.CharacterGrouping.objects.all()
        chars = models.Character.objects.filter(
            charactergroupings__isnull=False
        ).order_by(
            "created_by_run__book__id",
            "line__page__sequence",
            "line__sequence",
            "sequence",
        )
        books = models.Book.objects.filter(
            characterruns__characters__in=chars
        ).distinct()
        char_classes = models.CharacterClass.objects.filter(
            assigned_to__in=chars
        ).distinct()
        print(chars.count())
        print(groupings.count())
        print(books.count())
        print(char_classes.count())

        all_char_data = []
        for char in tqdm(chars, desc="Serializing characters..."):
            ch_ser = serializers.CharacterListSerializer(
                instance=char, context={"request": None}
            ).data
            all_char_data.append(
                {"id": ch_ser["id"], "title": ch_ser["label"], "data": ch_ser}
            )
            with open(f"{OUTPUT_PATH}/characters/{char.id}.json", "w") as dumpfile:
                json.dump(camel_keys(ch_ser), dumpfile, cls=UUIDEncoder, indent=2)
        # with open(f"{OUTPUT_PATH}/characters.json", "w") as dumpfile:
        #     json.dump(all_char_data, dumpfile, cls=UUIDEncoder, indent=2)

        # all_class_data = []
        for cc in tqdm(char_classes, desc="Serializing character classes..."):
            cc_ser = serializers.CharacterClassSerializer(
                cc, context={"request": None}
            ).data
            # all_class_data.append(
            #     {
            #         "id": cc_ser["classname"],
            #         "title": cc_ser["classname"],
            #         "data": cc_ser,
            #     }
            # )
            with open(f"{OUTPUT_PATH}/classes/{cc.classname}.json", "w") as dumpfile:
                json.dump(camel_keys(cc_ser), dumpfile, cls=UUIDEncoder, indent=2)
        # with open(f"{OUTPUT_PATH}/classes.json", "w") as dumpfile:
        #     json.dump(all_class_data, dumpfile, cls=UUIDEncoder, indent=2)

        # all_book_data = []
        for book in tqdm(books, desc="Serializing books..."):
            bk_ser = serializers.BookListSerializer(
                book, context={"request": None}
            ).data
            # all_book_data.append(
            #     {"id": bk_ser["id"], "title": bk_ser["pq_title"], "data": bk_ser}
            # )
            with open(f"{OUTPUT_PATH}/books/{book.id}.json", "w") as dumpfile:
                json.dump(camel_keys(bk_ser), dumpfile, cls=UUIDEncoder, indent=2)
        # with open(f"{OUTPUT_PATH}/books.json", "w") as dumpfile:
        #     json.dump(all_book_data, dumpfile, cls=UUIDEncoder, indent=2)

        # all_grouping_data = []
        for grouping in tqdm(groupings, desc="Serializing groupings..."):
            group_ser = serializers.CharacterGroupingListSerializer(
                instance=grouping, context={"request": None}
            ).data
            group_ser["characters"] = list(
                grouping.characters.all().values_list("id", flat=True)
            )
            # all_grouping_data.append(
            #     {"id": group_ser["id"], "title": group_ser["label"], "data": group_ser}
            # )
            with open(f"{OUTPUT_PATH}/groupings/{grouping.id}.json", "w") as dumpfile:
                json.dump(camel_keys(group_ser), dumpfile, cls=UUIDEncoder, indent=2)
        # with open(f"serialized_json/groupings.json", "w") as dumpfile:
        #     json.dump(all_grouping_data, dumpfile, cls=UUIDEncoder, indent=2)

        # create full list of images
        all_images = {}
        for c in tqdm(all_char_data):
            # Make sure book cover page is captured
            char = models.Character.objects.get(id=c["id"])
            book = models.Book.objects.get(id=c["data"]["book"])
            book_cover_url = book.cover_page().image["iiif_base"]
            book_cover_identifier = book.cover_page().id
            if book_cover_identifier not in all_images:
                all_images[book_cover_identifier] = {
                    "url": book_cover_url.replace(
                        "/img/iiif/", "https://printprobdb.psc.edu/iiif/"
                    ),
                    "identifier": book_cover_url.replace("/img/iiif/", ""),
                    # add thumbnail image of cover
                    "custom_tiles": [{"size_w": 200}],
                }
            page_url = c["data"]["page"]["image"]["iiif_base"]
            identifier = c["data"]["page"]["id"]
            if identifier not in all_images:
                all_images[identifier] = {
                    "url": page_url.replace(
                        "/img/iiif/", "https://printprobdb.psc.edu/iiif/"
                    ),
                    "identifier": page_url.replace("/img/iiif/", ""),
                    "custom_tiles": [{"size_w": 200}],
                }
            character_tile = {
                "region_x": char.absolute_coords["x"],
                "region_y": char.absolute_coords["y"],
                "region_w": char.absolute_coords["w"],
                "region_h": char.absolute_coords["h"],
            }
            buffer_tile = {
                "region_x": max(char.absolute_coords["x"] - 50, 0),
                "region_y": max(char.absolute_coords["y"] - 50, 0),
                "region_w": char.absolute_coords["w"] + 100,
                "region_h": char.absolute_coords["h"] + 100,
                "size_w": 150,
            }
            all_images[identifier]["custom_tiles"].append(character_tile)
            all_images[identifier]["custom_tiles"].append(buffer_tile)
        list_images = [v for k, v in all_images.items()]
        with open(f"serialized_json/converter.json", "w") as dumpfile:
            json.dump(list_images, dumpfile, cls=UUIDEncoder, indent=2)
