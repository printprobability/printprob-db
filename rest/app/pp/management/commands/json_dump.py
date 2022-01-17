from django.core.management.base import BaseCommand
from pp import models, serializers
from rest_framework.renderers import JSONRenderer
import json
from tqdm import tqdm
from uuid import UUID


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
            ch_ser = serializers.CharacterDetailSerializer(
                instance=char, context={"request": None}
            ).data
            ch_ser["groupings"] = [
                serializers.CharacterGroupingDetailSerializer(
                    instance=g, context={"request": None}
                ).data
                for g in char.charactergroupings.all()
            ]
            all_char_data.append(ch_ser)
        with open(f"{OUTPUT_PATH}/characters.json", "w") as dumpfile:
            json.dump(all_char_data, dumpfile, cls=UUIDEncoder, indent=2)

        all_class_data = []
        for cc in tqdm(char_classes, desc="Serializing character classes..."):
            cc_ser = {
                "classname": cc.classname,
                "characters": [
                    serializers.CharacterDetailSerializer(
                        instance=c, context={"request": None}
                    ).data
                    for c in chars.filter(character_class=cc)
                ],
            }
            all_class_data.append(cc_ser)
        with open(f"{OUTPUT_PATH}/classes.json", "w") as dumpfile:
            json.dump(all_class_data, dumpfile, cls=UUIDEncoder, indent=2)

        all_book_data = []
        for book in tqdm(books, desc="Serializing books..."):
            bk_ser = serializers.BookDetailSerializer(
                book, context={"request": None}
            ).data
            bk_ser["characters"] = [
                serializers.CharacterDetailSerializer(
                    instance=c, context={"request": None}
                ).data
                for c in chars.filter(created_by_run__book=book)
            ]
            all_book_data.append(bk_ser)
        with open(f"serialized_json/books.json", "w") as dumpfile:
            json.dump(all_book_data, dumpfile, cls=UUIDEncoder, indent=2)

        all_grouping_data = []
        for grouping in tqdm(groupings, desc="Serializing groupings..."):
            group_ser = serializers.CharacterGroupingDetailSerializer(
                instance=grouping, context={"request": None}
            ).data
            group_ser["characters"] = [
                serializers.CharacterDetailSerializer(
                    instance=c, context={"request": None}
                ).data
                for c in chars.filter(charactergroupings=grouping)
            ]
            all_grouping_data.append(group_ser)
        with open(f"serialized_json/groupings.json", "w") as dumpfile:
            json.dump(all_grouping_data, dumpfile, cls=UUIDEncoder, indent=2)

        # create full list of images
        all_images = {}
        for c in all_char_data:
            page_url = c["page"]["image"]["iiif_base"]
            identifier = c["page"]["id"]
            if identifier not in all_images:
                all_images[identifier] = {
                    "url": page_url,
                    "identifier": page_url.replace(
                        "https://printprobdb.psc.edu/iiif//", ""
                    ),
                    "custom_tiles": [],
                }
            character_tile = {
                "region_x": c["absolute_coords"]["x"],
                "region_y": c["absolute_coords"]["y"],
                "region_w": c["absolute_coords"]["w"],
                "region_h": c["absolute_coords"]["h"],
            }
            thumbnail_tile = {
                "region_x": c["absolute_coords"]["x"],
                "region_y": c["absolute_coords"]["y"],
                "region_w": c["absolute_coords"]["w"],
                "region_h": c["absolute_coords"]["h"],
                "size_w": 500,
            }
            buffer_tile = {
                "region_x": max(c["absolute_coords"]["x"] - 50, 0),
                "region_y": max(c["absolute_coords"]["y"] - 50, 0),
                "region_w": c["absolute_coords"]["w"] + 100,
                "region_h": c["absolute_coords"]["h"] + 100,
                "size_w": 150,
            }
            all_images[identifier]["custom_tiles"].append(character_tile)
            all_images[identifier]["custom_tiles"].append(thumbnail_tile)
            all_images[identifier]["custom_tiles"].append(buffer_tile)
        list_images = [v for k, v in all_images.items()]
        with open(f"serialized_json/converter.json", "w") as dumpfile:
            json.dump(list_images, dumpfile, cls=UUIDEncoder, indent=2)
