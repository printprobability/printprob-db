from rest_framework import serializers
from . import models


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


class PageDetailSerializer(serializers.ModelSerializer):
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
            "images",
            "lines",
            "x_min",
            "x_max",
        ]


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ["pk", "created_by_run", "spread", "side", "x_min", "x_max"]


class SpreadSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["pk", "book", "sequence", "images"]


class BookLineHeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProposedBookLineHeight
        fields = ["pk", "created_by_run", "book", "line_height"]


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["estc", "vid", "publisher", "title"]


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


class RunListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Run
        fields = ["pk", "date_started", "notes"]
        read_only_fields = ["pk", "date_entered"]


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

