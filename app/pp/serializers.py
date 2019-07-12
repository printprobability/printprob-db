from rest_framework import serializers
from django.db import transaction
from . import models


class RunListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Run
        fields = ["pk", "date_started", "notes"]
        read_only_fields = ["pk", "date_entered"]


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["classname"]


class BadCaptureSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.BadCapture
        fields = ["pk", "image", "date_entered"]
        read_only_fields = ["pk", "date_entered"]


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageFile
        fields = ["pk", "parent_image", "filetype", "date_uploaded", "filepath"]
        read_only_fields = ["date_uploaded"]


class ImageSerializer(serializers.ModelSerializer):
    files = ImageFileSerializer(many=True, read_only=True)

    class Meta:
        model = models.Image
        fields = ["pk", "notes", "web_file", "files", "web_url"]
        read_only_fields = ["web_file"]


class QuickImageSerializer(serializers.Serializer):
    jpeg = serializers.CharField(
        max_length=2000,
        help_text="relative file path of the JPEG version of this image",
    )
    tiff = serializers.CharField(
        max_length=2000, help_text="relative file path of the TIF version of this image"
    )
    notes = serializers.CharField(
        max_length=500,
        help_text="Standard identifier using the printer/id/location schema, without any filetype name",
        required=False,
        default="",
    )


class CharacterDetailSerializer(serializers.ModelSerializer):
    primary_image = ImageSerializer(many=False)

    class Meta:
        model = models.Character
        fields = [
            "pk",
            "created_by_run",
            "line",
            "sequence",
            "primary_image",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
        ]


class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = [
            "pk",
            "created_by_run",
            "line",
            "sequence",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "primary_image",
        ]

# Lines ----


class LineDetailSerializer(serializers.ModelSerializer):
    primary_image = ImageSerializer(many=False)

    class Meta:
        model = models.Line
        fields = [
            "pk",
            "created_by_run",
            "page",
            "sequence",
            "primary_image",
            "characters",
            "y_min",
            "y_max",
        ]
        read_only_fields = ["characters"]


class LineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = ["pk", "created_by_run", "page", "sequence", "y_min", "y_max"]


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = [
            "pk",
            "created_by_run",
            "page",
            "sequence",
            "y_min",
            "y_max",
            "primary_image",
        ]


# Pages ----


class PageListSerializer(serializers.ModelSerializer):
    created_by_run = RunListSerializer(many=False)

    class Meta:
        model = models.Page
        fields = [
            "pk",
            "created_by_run",
            "spread",
            "book_title",
            "side",
            "x_min",
            "x_max",
            "pref_image_url",
        ]


class PageDetailSerializer(serializers.ModelSerializer):
    created_by_run = RunListSerializer(many=False)
    lines = LineDetailSerializer(many=True)
    primary_image = ImageSerializer(many=False)

    class Meta:
        model = models.Page
        fields = [
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
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = [
            "pk",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "primary_image",
        ]


# Spreads ----


class SpreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "pref_image_url"]


class SpreadDetailSerializer(serializers.ModelSerializer):
    primary_image = ImageSerializer(many=False)

    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "primary_image", "pref_image_url"]


class SpreadSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "primary_image"]


class BookLineHeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProposedBookLineHeight
        fields = ["pk", "created_by_run", "book", "line_height"]


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["estc", "vid", "publisher", "title", "pdf"]


class BookDetailSerializer(serializers.ModelSerializer):
    proposed_line_heights = BookLineHeightSerializer(many=True)

    class Meta:
        model = models.Book
        fields = [
            "estc",
            "vid",
            "publisher",
            "title",
            "spreads",
            "proposed_line_heights",
            "pdf",
        ]


class RunDetailSerializer(serializers.ModelSerializer):
    pages_created = PageListSerializer(many=True)
    lines_created = LineListSerializer(many=True)
    characters_created = CharacterListSerializer(many=True)

    class Meta:
        model = models.Run
        fields = [
            "pk",
            "date_started",
            "notes",
            "pages_created",
            "lines_created",
            "characters_created",
        ]

