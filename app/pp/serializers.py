from rest_framework import serializers
from django.db import transaction
from . import models


class CharacterClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["url", "classname", "label"]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Image
        fields = ["url", "id", "label", "jpg", "tif", "jpg_md5", "tif_md5", "web_url"]


class BookFlatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = ["url", "eebo", "label", "vid", "publisher", "title", "pdf"]


class SpreadFlatSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Spread
        fields = ["url", "id", "label", "sequence", "image"]


class PageFlatSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = models.Page
        fields = ["url", "id", "label", "spread", "spread_sequence", "side", "image"]


class LineFlatSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = models.Line
        fields = ["url", "id", "label", "sequence", "image"]


class CharacterFlatSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = models.Character
        fields = ["url", "id", "label", "sequence", "image", "character_class"]


class PageRunListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.PageRun
        fields = [
            "url",
            "id",
            "label",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "label",
        ]


class PageRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookFlatSerializer(many=False)

    class Meta:
        model = models.PageRun
        fields = [
            "url",
            "id",
            "label",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
            "pages",
            "label",
        ]


class PageRunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PageRun
        fields = [
            "url",
            "id",
            "label",
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
            "label",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class LineRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookFlatSerializer(many=False)

    class Meta:
        model = models.LineRun
        fields = [
            "url",
            "id",
            "label",
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
            "label",
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
            "label",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class LineGroupRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookFlatSerializer(many=False)

    class Meta:
        model = models.LineGroupRun
        fields = [
            "url",
            "id",
            "label",
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
            "label",
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
            "label",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class CharacterRunDetailSerializer(serializers.HyperlinkedModelSerializer):
    book = BookFlatSerializer(many=False)

    class Meta:
        model = models.CharacterRun
        fields = [
            "url",
            "id",
            "label",
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
            "label",
            "book",
            "params",
            "script_path",
            "script_md5",
            "date_started",
        ]


class CharacterDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)
    book = BookFlatSerializer(many=False)
    spread = SpreadFlatSerializer(many=False)
    page = PageFlatSerializer(many=False)
    line = LineFlatSerializer(many=False)

    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "book",
            "spread",
            "page",
            "line",
            "sequence",
            "image",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
        ]


class CharacterListSerializer(serializers.HyperlinkedModelSerializer):
    book = BookFlatSerializer()
    spread = SpreadFlatSerializer()
    page = PageFlatSerializer()
    line = LineFlatSerializer()
    image = ImageSerializer()

    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "book",
            "spread",
            "page",
            "line",
            "sequence",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "image",
        ]


class CharacterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
            "label",
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
            "label",
            "created_by_run",
            "page",
            "sequence",
            "image",
            "y_min",
            "y_max",
            "most_recent_characters",
            "characters",
            "most_recent_linegroups",
            "linegroups",
        ]


class LineListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Line
        fields = ["url", "id", "label", "created_by_run", "page", "sequence", "y_min", "y_max"]


class LineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "page",
            "sequence",
            "y_min",
            "y_max",
            "image",
        ]


class PageListSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "spread",
            "spread_sequence",
            "side",
            "x_min",
            "x_max",
            "image",
        ]


class PageDetailSerializer(serializers.HyperlinkedModelSerializer):
    created_by_run = PageRunListSerializer(many=False)
    lines = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="line-detail",
        read_only=True,
        help_text="All Line instances ever produced from this Page, under any run.",
    )
    most_recent_lines = LineFlatSerializer(many=True)
    image = ImageSerializer(many=False)
    book = BookFlatSerializer(many=False)
    spread = SpreadFlatSerializer(many=False)

    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "book",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
            "most_recent_lines",
            "lines",
        ]


class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "spread",
            "side",
            "x_min",
            "x_max",
            "image",
        ]


class SpreadListSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = models.Spread
        fields = ["url", "id", "book", "sequence", "image"]


class SpreadDetailSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)
    pages = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="page-detail",
        read_only=True,
        help_text="All Page instances ever produced from this spread, under any run.",
    )
    most_recent_pages = PageFlatSerializer(
        many=True,
        read_only=True,
        help_text="Pages processed for this spread during the most recent page run processed for this book.",
    )

    class Meta:
        model = models.Spread
        fields = [
            "url",
            "id",
            "label",
            "book",
            "sequence",
            "image",
            "most_recent_pages",
            "pages",
        ]


class SpreadCreateSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "book", "sequence", "image"]


class BookListSerializer(serializers.HyperlinkedModelSerializer):
    cover_page = PageFlatSerializer(many=False)

    class Meta:
        model = models.Book
        fields = [
            "url",
            "eebo",
            "vid",
            "label",
            "publisher",
            "title",
            "pdf",
            "n_spreads",
            "cover_page",
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["url", "eebo", "label", "vid", "publisher", "title", "pdf"]


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
    most_recent_pages = PageFlatSerializer(
        many=True,
        help_text="Ordered pages from the most recent page segmentation run",
        read_only=True,
    )
    cover_page = PageFlatSerializer(many=False, read_only=True)

    class Meta:
        model = models.Book
        fields = [
            "url",
            "eebo",
            "label",
            "vid",
            "publisher",
            "title",
            "pdf",
            "cover_page",
            "n_spreads",
            "spreads",
            "most_recent_runs",
            "all_runs",
            "most_recent_pages",
        ]


class LineGroupListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "label", "page", "created_by_run", "lines"]


class LineGroupDetailSerializer(serializers.HyperlinkedModelSerializer):
    lines = LineListSerializer(many=True)

    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "label", "page", "created_by_run", "lines"]


class LineGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "label", "page", "created_by_run", "lines"]

