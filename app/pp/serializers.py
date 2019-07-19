from rest_framework import serializers
from django.db import transaction
from . import models


class BookListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = ["url", "estc", "vid", "publisher", "title", "pdf", "n_spreads"]


class PageRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PageRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class PageRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookListSerializer(many=False)

    class Meta:
        model = models.PageRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "pages",
        ]


class PageRunCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PageRun
        fields = ["book", "params", "script_path", "script_md5"]


class LineRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class LineRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookListSerializer(many=False)

    class Meta:
        model = models.LineRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "lines",
        ]


class LineRunCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineRun
        fields = ["book", "params", "script_path", "script_md5"]


class LineGroupRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineGroupRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class LineGroupRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookListSerializer(many=False)

    class Meta:
        model = models.LineGroupRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "line_groups",
        ]


class LineGroupRunCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineGroupRun
        fields = ["book", "params", "script_path", "script_md5"]


class CharacterRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CharacterRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class CharacterRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookListSerializer(many=False)

    class Meta:
        model = models.CharacterRun
        fields = [
            "url",
            "pk",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "characters",
        ]


class CharacterRunCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CharacterRun
        fields = ["book", "params", "script_path", "script_md5"]


class CharacterClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["url", "classname"]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Image
        fields = ["url", "pk", "jpg", "tif"]


class CharacterDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Character
        fields = [
            "url",
            "pk",
            "created_by_run",
            "line",
            "sequence",
            "image",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "pref_image_url",
        ]


class CharacterListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Character
        fields = [
            "url",
            "pk",
            "created_by_run",
            "line",
            "sequence",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "image",
            "pref_image_url",
        ]


class CharacterCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Character
        fields = [
            "created_by_run",
            "line",
            "sequence",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "image",
        ]


class LineDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Line
        fields = [
            "url",
            "pk",
            "created_by_run",
            "page",
            "sequence",
            "image",
            "characters",
            "y_min",
            "y_max",
            "pref_image_url",
        ]
        read_only_fields = ["characters"]


class LineListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Line
        fields = ["url", "pk", "created_by_run", "page", "sequence", "y_min", "y_max"]


class LineCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Line
        fields = ["created_by_run", "page", "sequence", "y_min", "y_max", "image"]


class PageListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Page
        fields = [
            "url",
            "pk",
            "created_by_run",
            "spread",
            "book_title",
            "side",
            "x_min",
            "x_max",
            "pref_image_url",
        ]


class PageDetailSerializer(serializers.HyperlinkedModelSerializer):
    created_by_run = PageRunListSerializer(many=False)
    lines = LineListSerializer(many=True)
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Page
        fields = [
            "url",
            "pk",
            "created_by_run",
            "spread",
            "book_title",
            "side",
            "x_min",
            "x_max",
            "lines",
            "image",
            "pref_image_url",
        ]


class PageCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Page
        fields = ["created_by_run", "spread", "side", "x_min", "x_max", "image"]


class SpreadListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "pk", "book", "sequence", "pref_image_url"]


class SpreadDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Spread
        fields = ["url", "pk", "book", "sequence", "image", "pref_image_url", "pages"]


class SpreadCreateSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["book", "sequence", "image"]


class BookCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = ["url", "estc", "vid", "publisher", "title", "pdf"]


class BookRunsSerializer(serializers.Serializer):
    page = PageRunDetailSerializer(many=False)
    line = LineRunDetailSerializer(many=False)
    line_group = LineGroupRunDetailSerializer(many=False)
    character = CharacterRunDetailSerializer(many=False)


class BookDetailSerializer(serializers.HyperlinkedModelSerializer):
    spreads = SpreadListSerializer(many=True)
    most_recent_runs = BookRunsSerializer()

    class Meta:
        model = models.Book
        fields = [
            "estc",
            "vid",
            "publisher",
            "title",
            "pdf",
            "n_spreads",
            "spreads",
            "most_recent_runs",
        ]


class LineGroupListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "pk", "page", "created_by_run"]


class LineGroupDetailSerializer(serializers.HyperlinkedModelSerializer):
    lines = LineListSerializer(many=True)

    class Meta:
        model = models.LineGroup
        fields = ["url", "pk", "page", "created_by_run", "lines"]

