from rest_framework import serializers
from rest_framework.reverse import reverse
from django.db import transaction
from django.contrib.auth.models import User
from . import models


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["url", "classname", "label"]


class CroppedImageSerializer(serializers.Serializer):
    web_url = serializers.URLField(read_only=True)
    thumbnail = serializers.URLField(read_only=True)


class SpreadFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "label", "sequence", "image"]


class PageFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ["url", "id", "label", "spread", "spread_sequence", "side", "image"]


class LineFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = ["url", "id", "label", "sequence", "image"]


class CharacterFlatSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )
    human_character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )

    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
            "label",
            "sequence",
            "image",
            "character_class",
            "human_character_class",
            "x_min",
            "x_max",
            "exposure",
            "offset",
            "image",
        ]


class BookListSerializer(serializers.ModelSerializer):
    cover_spread = SpreadFlatSerializer(many=False, read_only=True)
    n_spreads = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Book
        fields = [
            "url",
            "id",
            "eebo",
            "vid",
            "tcp",
            "estc",
            "zipfile",
            "zip_path",
            "label",
            "pp_publisher",
            "pq_publisher",
            "pq_title",
            "pq_url",
            "pq_author",
            "pq_year_verbatim",
            "pq_year_early",
            "pq_year_late",
            "tx_year_early",
            "tx_year_late",
            "date_early",
            "date_late",
            "pdf",
            "n_spreads",
            "cover_spread",
            "starred",
            "ignored",
        ]


class PageRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PageRun
        fields = ["url", "id", "label", "book", "date_started", "component_count"]
        read_only_fields = ["component_count", "label", "date_started", "id"]


class LineRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineRun
        fields = ["url", "id", "label", "book", "date_started", "component_count"]
        read_only_fields = ["component_count", "label", "date_started", "id"]


class LineGroupRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineGroupRun
        fields = ["url", "id", "label", "book", "date_started", "component_count"]
        read_only_fields = ["component_count", "label", "date_started", "id"]


class CharacterRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterRun
        fields = ["url", "id", "label", "book", "date_started", "component_count"]
        read_only_fields = ["component_count", "label", "date_started", "id"]


class LineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "page",
            "page_side",
            "sequence",
            "image",
            "y_min",
            "y_max",
        ]


class LineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "page",
            "page_side",
            "sequence",
            "y_min",
            "y_max",
            "image",
        ]


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
        read_only_fields = ["image"]


class PageListSerializer(serializers.ModelSerializer):
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
            "x",
            "y",
            "w",
            "h",
            "rot1",
            "rot2",
            "image",
        ]


class PageDetailSerializer(serializers.ModelSerializer):
    created_by_run = PageRunSerializer(many=False)
    lines = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="line-detail",
        read_only=True,
        help_text="All Line instances ever produced from this Page, under any run.",
    )
    most_recent_lines = LineFlatSerializer(many=True)
    book = BookListSerializer(many=False)
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
            "x",
            "y",
            "w",
            "h",
            "rot1",
            "rot2",
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
            "x",
            "y",
            "w",
            "h",
            "rot1",
            "rot2",
            "image",
        ]


class SpreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "label", "book", "sequence", "image"]


class SpreadDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False)
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


class BookAllRunsSerializer(serializers.Serializer):
    pages = PageRunSerializer(many=True)
    lines = LineRunSerializer(many=True)
    linegroups = LineGroupRunSerializer(many=True)
    characters = CharacterRunSerializer(many=True)


class BookDetailSerializer(serializers.ModelSerializer):
    spreads = SpreadListSerializer(many=True)
    cover_spread = SpreadListSerializer(many=False)
    all_runs = BookAllRunsSerializer()

    class Meta:
        model = models.Book
        fields = [
            "url",
            "id",
            "eebo",
            "label",
            "vid",
            "tcp",
            "estc",
            "zipfile",
            "zip_path",
            "pp_publisher",
            "pq_publisher",
            "pq_title",
            "pq_author",
            "pq_url",
            "pq_year_verbatim",
            "pq_year_early",
            "pq_year_late",
            "tx_year_early",
            "tx_year_late",
            "date_early",
            "date_late",
            "pdf",
            "spreads",
            "all_runs",
            "cover_spread",
            "starred",
            "ignored",
        ]


class LineGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "label", "page", "created_by_run", "lines"]


class LineGroupDetailSerializer(serializers.ModelSerializer):
    lines = LineListSerializer(many=True)

    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "label", "page", "created_by_run", "lines"]


class LineGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineGroup
        fields = ["url", "id", "label", "page", "created_by_run", "lines"]


class CharacterGroupingListSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = models.CharacterGrouping
        fields = ["url", "id", "label", "notes", "created_by", "date_created"]


class CharacterGroupingDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
    characters = CharacterFlatSerializer(many=True)

    class Meta:
        model = models.CharacterGrouping
        fields = fields = [
            "url",
            "id",
            "label",
            "notes",
            "created_by",
            "date_created",
            "characters",
        ]


class CharacterGroupingCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field="username",
        read_only=False,
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = models.CharacterGrouping
        fields = [
            "url",
            "id",
            "created_by",
            "date_created",
            "label",
            "notes",
            "characters",
        ]


class CharacterGroupingCharacterListSerializer(serializers.ModelSerializer):
    characters = serializers.PrimaryKeyRelatedField(
        queryset=models.Character.objects.all(), many=True
    )

    class Meta:
        model = models.CharacterGrouping
        fields = ["characters"]


class CharacterDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False)
    spread = SpreadFlatSerializer(many=False)
    page = PageFlatSerializer(many=False)
    line = LineFlatSerializer(many=False)
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )
    human_character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )

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
            "human_character_class",
            "exposure",
            "offset",
            "absolute_coords",
            "image",
        ]


class CharacterListSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )
    human_character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )

    class Meta:
        model = models.Character
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "sequence",
            "x_min",
            "x_max",
            "character_class",
            "class_probability",
            "image",
            "human_character_class",
            "exposure",
            "offset",
            "image",
        ]


class CharacterCreateSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )

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
            "exposure",
            "offset",
            "image",
        ]


class CharacterAnnotateSerializer(serializers.Serializer):
    characters = serializers.PrimaryKeyRelatedField(
        queryset=models.Character.objects.all(), many=True
    )
    human_character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all(), many=False, allow_null=True
    )

