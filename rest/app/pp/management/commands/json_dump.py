from django.core import management
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
        chars = models.Character.objects.filter(charactergroupings__label="test")
        books = models.Book.objects.filter(
            characterruns__characters__in=chars
        ).distinct()
        char_classes = models.CharacterClass.objects.filter(
            assigned_to__in=chars
        ).distinct()
        print(books.count())
        print(char_classes.count())
        for char in tqdm(chars, desc="Serializing characters..."):
            ch_ser = serializers.CharacterDetailSerializer(
                instance=char, context={"request": None}
            ).data
            with open(f"serialized_json/characters/{char.id}.md", "w") as dumpfile:
                dumpfile.write("---\n")
                json.dump(ch_ser, dumpfile, cls=UUIDEncoder, indent=2)
                dumpfile.write("\n---\n")
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
            with open(f"serialized_json/classes/{cc.classname}.md", "w") as dumpfile:
                dumpfile.write("---\n")
                json.dump(cc_ser, dumpfile, cls=UUIDEncoder, indent=2)
                dumpfile.write("\n---\n")
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
            with open(f"serialized_json/books/{book.id}.md", "w") as dumpfile:
                dumpfile.write("---\n")
                json.dump(bk_ser, dumpfile, cls=UUIDEncoder, indent=2)
                dumpfile.write("\n---\n")

