from pickletools import read_long1
from rest_framework import serializers
from . import models


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["classname", "label", "group"]


class CroppedImageSerializer(serializers.Serializer):
    web_url = serializers.URLField(read_only=True)
    thumbnail = serializers.URLField(read_only=True)


class PageFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ["id", "label", "sequence", "side", "image", "height", "width"]


class BookListSerializer(serializers.ModelSerializer):
    cover_page = PageFlatSerializer(many=False, read_only=True)
    n_spreads = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Book
        fields = [
            "id",
            "eebo",
            "vid",
            "tcp",
            "estc",
            "label",
            "pp_publisher",
            "pp_author",
            "pq_publisher",
            "pq_title",
            "pq_url",
            "pq_author",
            "pq_year_verbatim",
            "pq_year_early",
            "pq_year_late",
            "n_spreads",
            "cover_page",
            "is_eebo_book",
            "repository",
            "pp_printer",
            "colloq_printer",
            "pp_notes",
        ]


class CharacterGroupingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterGrouping
        fields = ["id", "label", "notes"]


class CharacterListSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )
    book = serializers.PrimaryKeyRelatedField(queryset=models.Book.objects.all())
    page = PageFlatSerializer(many=False, read_only=True)

    class Meta:
        model = models.Character
        fields = [
            "id",
            "label",
            "sequence",
            "character_class",
            "class_probability",
            "book",
            "page",
            "image",
            "absolute_coords",
        ]
