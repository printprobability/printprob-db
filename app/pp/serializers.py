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
        fields = ["pk", "classname"]


class ClassAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassAssignment
        fields = [
            "pk",
            "created_by_run",
            "character",
            "character_class",
            "log_probability",
        ]


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
    images = ImageSerializer(many=True)
    class_assignments = ClassAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Character
        fields = [
            "pk",
            "created_by_run",
            "line",
            "sequence",
            "images",
            "x_min",
            "x_max",
            "class_assignments",
        ]


class CharacterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = ["pk", "created_by_run", "line", "sequence", "x_min", "x_max"]


# Lines ----


class LineDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Line
        fields = [
            "pk",
            "created_by_run",
            "page",
            "sequence",
            "images",
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
            "images",
        ]

    @transaction.atomic
    def create(self, validated_data):
        """
        Allow a list of image UUIDs to be associated with the line
        """
        images_data = validated_data.pop("images")
        line = models.Line.objects.create(**validated_data)
        for image in images_data:
            line.images.add(image)
        return line


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
    images = ImageSerializer(many=True)

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
            "images",
            "pref_image_url",
        ]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ["pk", "created_by_run", "spread", "side", "x_min", "x_max", "images"]

    @transaction.atomic
    def create(self, validated_data):
        """
        Allow a list of image UUIDs to be associated with the page
        """
        images_data = validated_data.pop("images")
        page = models.Page.objects.create(**validated_data)
        for image in images_data:
            page.images.add(image)
        return page


# Spreads ----


class SpreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "pref_image_url"]


class SpreadDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "images", "pref_image_url"]


class SpreadSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "images"]

    @transaction.atomic
    def create(self, validated_data):
        """
        Allow a list of image UUIDs to be associated with the spread
        """
        images_data = validated_data.pop("images")
        spread = models.Spread.objects.create(**validated_data)
        for image in images_data:
            spread.images.add(image)
        return spread


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

