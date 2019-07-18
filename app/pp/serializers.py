from rest_framework import serializers
from django.db import transaction
from . import models


class RunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Run
        fields = ["url", "pk", "date_started", "notes"]


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["classname"]


class BadCaptureSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.BadCapture
        fields = ["pk", "image", "date_entered"]
        read_only_fields = ["pk", "date_entered"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ["pk", "notes", "jpg", "tif"]


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
            "pref_image_url",
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
            "pref_image_url",
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
            "pref_image_url",
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
            "pref_image_url",
        ]


# Pages ----


class PageListSerializer(serializers.ModelSerializer):
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


class SpreadListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "pk", "book", "sequence", "pref_image_url"]


class SpreadDetailSerializer(serializers.HyperlinkedModelSerializer):
    primary_image = ImageSerializer(many=False)

    class Meta:
        model = models.Spread
        fields = [
            "url",
            "pk",
            "book",
            "sequence",
            "primary_image",
            "pref_image_url",
            "pages",
        ]


class SpreadSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "primary_image", "pref_image_url"]


class BookListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = ["url", "estc", "vid", "publisher", "title", "pdf"]


class BookDetailSerializer(serializers.HyperlinkedModelSerializer):
    spreads = SpreadListSerializer(many=True)

    class Meta:
        model = models.Book
        fields = ["url", "estc", "vid", "publisher", "title", "pdf", "spreads"]


class RunDetailSerializer(serializers.HyperlinkedModelSerializer):
    pages_created = PageListSerializer(many=True)
    lines_created = LineListSerializer(many=True)
    characters_created = CharacterListSerializer(many=True)

    class Meta:
        model = models.Run
        fields = [
            "url",
            "pk",
            "date_started",
            "notes",
            "pages_created",
            "lines_created",
            "characters_created",
        ]

