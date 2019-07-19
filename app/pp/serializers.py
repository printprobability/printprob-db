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
            "id",
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
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "pages",
        ]


class PageRunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PageRun
        fields = [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class LineRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineRun
        fields = [
            "url",
            "id",
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
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "lines",
        ]


class LineRunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineRun
        fields = [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class LineGroupRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineGroupRun
        fields = [
            "url",
            "id",
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
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "linegroups",
        ]


class LineGroupRunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineGroupRun
        fields = [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class CharacterRunListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CharacterRun
        fields = [
            "url",
            "id",
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
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "characters",
        ]


class CharacterRunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterRun
        fields = [
            "url",
            "id",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class CharacterClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["url", "classname"]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Image
        fields = ["url", "id", "jpg", "tif", "jpg_md5", "tif_md5"]


class CharacterDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
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
            "id",
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


class CharacterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
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
    characters = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="character-detail",
        read_only=True,
        help_text="All Character instances ever produced from this line, under any run.",
    )
    most_recent_characters = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="character-detail",
        read_only=True,
        help_text="Characters processed for this line during the most recent character run processed for this book.",
    )
    linegroups = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="linegroup-detail",
        read_only=True,
        help_text="All LineGroup instances ever produced containing this Line, under any run.",
    )
    most_recent_linegroups = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="linegroup-detail",
        read_only=True,
        help_text="LineGroups processed containing this line during the most recent line group run processed for this book.",
    )

    class Meta:
        model = models.Line
        fields = [
            "url",
            "id",
            "created_by_run",
            "page",
            "sequence",
            "image",
            "y_min",
            "y_max",
            "pref_image_url",
            "most_recent_characters",
            "characters",
            "most_recent_linegroups",
            "linegroups",
        ]


class LineListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Line
        fields = ["url", "id", "created_by_run", "page", "sequence", "y_min", "y_max"]


class LineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = [
            "url",
            "id",
            "created_by_run",
            "page",
            "sequence",
            "y_min",
            "y_max",
            "image",
        ]


class PageListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
            "pref_image_url",
        ]


class PageDetailSerializer(serializers.HyperlinkedModelSerializer):
    created_by_run = PageRunListSerializer(many=False)
    lines = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="line-detail",
        read_only=True,
        help_text="All Line instances ever produced from this Page, under any run.",
    )
    most_recent_lines = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="line-detail",
        read_only=True,
        help_text="Lines processed for this Page during the most recent page run processed for this book.",
    )
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
            "pref_image_url",
            "most_recent_lines",
            "lines",
        ]


class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
        ]


class SpreadListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "book", "sequence", "image", "pref_image_url"]


class SpreadDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)
    pages = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="page-detail",
        read_only=True,
        help_text="All Page instances ever produced from this spread, under any run.",
    )
    most_recent_pages = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="page-detail",
        read_only=True,
        help_text="Pages processed for this spread during the most recent page run processed for this book.",
    )

    class Meta:
        model = models.Spread
        fields = [
            "url",
            "id",
            "book",
            "sequence",
            "image",
            "pref_image_url",
            "most_recent_pages",
            "pages",
        ]


class SpreadCreateSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "book", "sequence", "image"]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["url", "estc", "vid", "publisher", "title", "pdf"]


class BookRunsSerializer(serializers.Serializer):
    page = PageRunDetailSerializer(many=False)
    line = LineRunDetailSerializer(many=False)
    linegroup = LineGroupRunDetailSerializer(many=False)
    character = CharacterRunDetailSerializer(many=False)


class BookAllRunsSerializer(serializers.Serializer):
    pages = serializers.HyperlinkedRelatedField(
        many=True, view_name="pagerun-detail", read_only=True
    )
    lines = serializers.HyperlinkedRelatedField(
        many=True, view_name="linerun-detail", read_only=True
    )
    linegroups = serializers.HyperlinkedRelatedField(
        many=True, view_name="linegrouprun-detail", read_only=True
    )
    characters = serializers.HyperlinkedRelatedField(
        many=True, view_name="characterrun-detail", read_only=True
    )


class BookDetailSerializer(serializers.HyperlinkedModelSerializer):
    spreads = SpreadListSerializer(many=True)
    most_recent_runs = BookRunsSerializer()
    all_runs = BookAllRunsSerializer()

    class Meta:
        model = models.Book
        fields = [
            "url",
            "estc",
            "vid",
            "publisher",
            "title",
            "pdf",
            "n_spreads",
            "spreads",
            "most_recent_runs",
            "all_runs",
        ]


class LineGroupListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "page", "created_by_run", "lines"]


class LineGroupDetailSerializer(serializers.HyperlinkedModelSerializer):
    lines = LineListSerializer(many=True)

    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "page", "created_by_run", "lines"]


class LineGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "page", "created_by_run", "lines"]

