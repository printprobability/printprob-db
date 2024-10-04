from django.contrib.auth.models import User
from rest_framework import serializers

from . import models


class BreakageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BreakageType
        fields = ["url", "id", "label"]


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterClass
        fields = ["url", "classname", "label", "group"]


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
        fields = ["url", "id", "label", "sequence", "side", "image"]


class LineFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = ["url", "id", "label", "sequence", "image"]


class BookNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = [
            "id",
            "label",
        ]


class CharacterFlatSerializer(serializers.ModelSerializer):
    book = BookNameSerializer(many=False)
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
            "class_probability",
            "human_character_class",
            "damage_score",
            "x_min",
            "x_max",
            "y_min",
            "y_max",
            "exposure",
            "offset",
            "image",
            "created_by_run_id",
            "book",
        ]


class BookListSerializer(serializers.ModelSerializer):
    cover_spread = SpreadFlatSerializer(many=False, read_only=True)
    cover_page = PageFlatSerializer(many=False, read_only=True)
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
            "pp_author",
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
            "cover_page",
            "starred",
            "ignored",
            "is_eebo_book",
            "prefix",
            "repository",
            "pp_printer",
            "colloq_printer",
            "pp_notes",
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
            "sequence",
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

    class Meta:
        model = models.Page
        fields = [
            "url",
            "id",
            "label",
            "created_by_run",
            "book",
            "side",
            "sequence",
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
            "sequence",
            "side",
            "x",
            "y",
            "w",
            "h",
            "rot1",
            "rot2",
            "tif",
        ]


class SpreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "label", "book", "sequence", "image"]


class SpreadDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False)

    class Meta:
        model = models.Spread
        fields = ["url", "id", "label", "book", "sequence", "image"]


class SpreadCreateSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.Spread
        fields = ["url", "id", "book", "sequence", "image"]


class BookAllRunsSerializer(serializers.Serializer):
    pages = PageRunSerializer(many=True)
    lines = LineRunSerializer(many=True)
    characters = CharacterRunSerializer(many=True)


class BookDetailSerializer(serializers.ModelSerializer):
    spreads = SpreadListSerializer(many=True)
    cover_spread = SpreadListSerializer(many=False)
    cover_page = PageListSerializer(many=False)
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
            "pp_author",
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
            "cover_page",
            "starred",
            "ignored",
            "is_eebo_book",
            "prefix",
            "repository",
            "pp_printer",
            "colloq_printer",
            "pp_notes",
        ]


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
            "page",
            "line",
            "sequence",
            "x_min",
            "x_max",
            "y_min",
            "y_max",
            "character_class",
            "class_probability",
            "human_character_class",
            "damage_score",
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
            "y_min",
            "y_max",
            "character_class",
            "class_probability",
            "human_character_class",
            "damage_score",
            "exposure",
            "offset",
            "absolute_coords",
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
            "y_min",
            "y_max",
            "character_class",
            "class_probability",
            "damage_score",
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


class CharacterMatchSerializer(serializers.ModelSerializer):
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=models.CharacterClass.objects.all()
    )

    class Meta:
        model = models.Character
        fields = [
            "id",
            "label",
            "character_class",
            "image",
        ]


class ExistingCharacterMatchSerializer(serializers.Serializer):
    query = serializers.PrimaryKeyRelatedField(
        queryset=models.Character.objects.all(), many=False
    )
    matches = serializers.ListField(
        child=serializers.UUIDField()
    )

    class Meta:
        model = models.CharacterMatch
        fields = [
            "query_id",
            "matches",
        ]
