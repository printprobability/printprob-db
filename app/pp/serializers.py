from rest_framework import serializers
from . import models


class BadCaptureSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.BadCapture
        fields = ["pk", "image", "date_entered"]
        read_only_fields = ["pk", "date_entered"]


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageFile
        fields = ["filetype", "date_uploaded"]
        read_only_fields = ["filetype", "date_uploaded"]


class ImageSerializer(serializers.ModelSerializer):
    files = ImageFileSerializer(many=True)
    bad_capture = serializers.BooleanField()

    class Meta:
        model = models.Image
        fields = ["pk", "basename", "web_url", "files", "created_by_run", "bad_capture"]
        read_only_fields = ["pk", "basename", "web_file", "files", "web_url"]


class CharacterDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Character
        fields = ["pk", "line", "sequence", "images"]


class CharacterListSerializer(serializers.ModelSerializer):
    pref_image = ImageSerializer(many=False)

    class Meta:
        model = models.Character
        fields = ["pk", "line", "sequence", "pref_image"]


class LineDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    pref_image = ImageSerializer(many=False)

    class Meta:
        model = models.Line
        fields = ["pk", "page", "sequence", "images", "characters", "pref_image"]


class LineListSerializer(serializers.ModelSerializer):
    n_chars = serializers.IntegerField()
    pref_image = ImageSerializer(many=False)

    class Meta:
        model = models.Line
        fields = ["pk", "page", "sequence", "n_chars", "n_images", "pref_image"]


class PageDetailSerializer(serializers.ModelSerializer):
    lines = LineDetailSerializer(many=True)
    images = ImageSerializer(many=True)
    pref_image = ImageSerializer(many=False)

    class Meta:
        model = models.Page
        fields = [
            "pk",
            "spread__book",
            "book_title",
            "spread__sequence",
            "side",
            "images",
            "lines",
            "pref_image",
        ]


class PageListSerializer(serializers.ModelSerializer):
    n_lines = serializers.IntegerField()
    pref_image = ImageSerializer(many=False)

    class Meta:
        model = models.Page
        fields = ["pk", "book", "sequence", "side", "n_lines", "pref_image"]


class BookListSerializer(serializers.ModelSerializer):
    cover_page = PageListSerializer()

    class Meta:
        model = models.Book
        fields = ["pk", "title", "estc", "year_early", "n_pages", "cover_page"]


class BookDetailSerializer(serializers.ModelSerializer):
    cover_page = PageListSerializer()
    pages = PageListSerializer(many=True)

    class Meta:
        model = models.Book
        fields = ["pk", "title", "estc", "year_early", "n_pages", "pages", "cover_page"]
