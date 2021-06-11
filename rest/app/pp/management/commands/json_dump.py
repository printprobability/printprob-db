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
        chars = models.Character.objects.filter(charactergroupings__isnull=False)
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
                    for c in chars.filter(character_class=cc).distinct()
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
                for c in chars.filter(created_by_run__book=book).distinct()
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
                for c in grouping.characters.all()
            ]
            all_grouping_data.append(group_ser)
        with open(f"serialized_json/groupings.json", "w") as dumpfile:
            json.dump(all_grouping_data, dumpfile, cls=UUIDEncoder, indent=2)