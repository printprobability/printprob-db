import tarfile
from tempfile import TemporaryDirectory
from uuid import UUID
import logging

import requests
from django import forms
from django.conf import settings
from django.db import transaction, DatabaseError
from django.db.models import F, Q, Exists, OuterRef, Prefetch
from django.db.models.query import EmptyQuerySet
from django.http import FileResponse
from django.utils.text import slugify
from django_filters import rest_framework as filters
from drf_tweaks.pagination import NoCountsLimitOffsetPagination
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers
from .management.commands.bulk_update import BookLoader as BookUpdater
from .management.commands.bulk_load import BookLoader as BookCreator


class GetSerializerClassMixin(object):
    def get_queryset(self):
        try:
            return self.queryset_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class CRUDViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["get"])
    def count(self, request):
        ocount = (
            self.filterset_class(
                self.request.GET,
                # Get the baseline model without pre-joining anything
                queryset=self.get_queryset().model.objects.all(),
            )
                .qs.values("pk")
                .count()
        )
        return Response({"count": ocount})


class BookFilter(filters.FilterSet):
    eebo = filters.NumberFilter(help_text="Numeric EEBO ID")
    vid = filters.NumberFilter(help_text="Numeric VID")
    tcp = filters.CharFilter(help_text="TCP")
    estc = filters.CharFilter(help_text="ESTC")
    pq_title = filters.CharFilter(
        help_text="books with titles containing this string (case insensitive)",
        lookup_expr="icontains",
    )
    pq_publisher = filters.CharFilter(
        help_text="books with publisher labels containing this string (case insensitive)",
        lookup_expr="icontains",
    )
    pq_author = filters.CharFilter(
        help_text="books with authors containing this string (case insensitive)",
        lookup_expr="icontains",
    )
    pp_publisher = filters.CharFilter(
        help_text="books assinged to this printer by P&P team", lookup_expr="icontains"
    )
    colloq_printer = filters.CharFilter(lookup_expr="icontains")
    pp_printer = filters.CharFilter(lookup_expr="icontains")
    repository = filters.CharFilter(lookup_expr="icontains")
    pp_author = filters.CharFilter(
        help_text="books assinged to this author by P&P team", lookup_expr="icontains"
    )
    repository = filters.CharFilter(
        help_text="Repository holding this copy of the book", lookup_expr="icontains"
    )
    characters = filters.BooleanFilter(
        method="has_characters",
        label="Has characters?",
        help_text="Has had Character extractions processed",
    )
    pq_year_verbatim = filters.CharFilter(
        help_text="Search verbatim date strings from EEBO", lookup_expr="icontains"
    )
    pq_year_early = filters.RangeFilter(label="PQ start year")
    pq_year_late = filters.RangeFilter(label="PQ end year")
    tx_year_early = filters.RangeFilter(label="TX start year")
    tx_year_late = filters.RangeFilter(label="TX end year")
    year_early = filters.RangeFilter(label="PP start date")
    year_late = filters.RangeFilter(label="PP end date")
    starred = filters.BooleanFilter(label="Has star?")
    ignored = filters.BooleanFilter(label="Ignored?")
    is_eebo_book = filters.BooleanFilter(
        label="Record from EEBO database?",
        help_text="Book loaded from original EEBO data dump",
    )
    printer_like = filters.CharFilter(
        method='match_printer_name',
        label="Substring match on printer name",
        help_text="Substring match on printer name against either pp_printer or colloq_printer fields"
    )
    has_grouping = filters.BooleanFilter(
        label="Has characters in a group?", method="has_any_grouping"
    )

    def has_any_grouping(self, queryset, name, value):
        if value:
            groupings = models.CharacterGrouping.objects.filter(
                characters__created_by_run__book=OuterRef("pk")
            )
            return (
                queryset.annotate(has_groupings=Exists(groupings))
                    .filter(has_groupings=True)
                    .all()
            )
        return queryset

    def has_images(self, queryset, name, value):
        spreads = models.Spread.objects.filter(book=OuterRef("pk"), tif__isnull=False)
        pages = models.Page.objects.filter(
            created_by_run__book=OuterRef("pk"), tif__isnull=False
        )
        lines = models.Line.objects.filter(created_by_run__book=OuterRef("pk"))
        characters = models.Character.objects.filter(
            created_by_run__book=OuterRef("pk")
        )

        if value:
            return (
                queryset.annotate(
                    has_pages=Exists(pages),
                    has_lines=Exists(lines),
                    has_characters=Exists(characters),
                )
                    .filter(Q(has_pages=True) | Q(has_lines=True) | Q(has_characters=value))
                    .all()
            )
        return queryset

    def has_characters(self, queryset, name, value):
        characters = models.Character.objects.filter(
            created_by_run__book=OuterRef("pk")
        )

        if value:
            return queryset.filter(Exists(characters)).distinct()
        else:
            return queryset.filter(~Exists(characters)).distinct()

    def after_early(self, queryset, name, value):
        return queryset.filter(date_early__gte=value)

    def before_late(self, queryset, name, value):
        return queryset.filter(date_late__lte=value)

    def match_printer_name(self, queryset, name, value):

        # No query result if incoming value is an empty string
        # We do not want to return everything
        if not value.strip():
            return EmptyQuerySet()

        # Match rows where we have either the pp_printer value or the colloq_printer value as non-empty
        qs_filter = (
                (Q(pp_printer__exact='', _negated=True) | Q(colloq_printer__exact='', _negated=True)) &
                (Q(pp_printer__icontains=value) | Q(colloq_printer__icontains=value))
        )
        return queryset.filter(qs_filter)


class BookViewSet(CRUDViewSet, GetSerializerClassMixin):
    """
    list: Lists all books.
    """

    detail_queryset = models.Book.objects.prefetch_related("spreads").all()

    list_queryset = models.Book.objects.prefetch_related(
        Prefetch("spreads", queryset=models.Spread.objects.filter(sequence=1))
    ).all()

    queryset = detail_queryset
    serializer_action_classes = {"list": list_queryset, "detail": detail_queryset}
    filterset_class = BookFilter
    ordering_fields = ["pq_title", "pq_author", "pq_publisher", "date_early"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BookDetailSerializer
        return serializers.BookListSerializer

    @action(detail=True, methods=["delete"])
    def reset(self, request, pk=None):
        obj = self.get_object()
        res = obj.spreads.all().delete()
        return Response(res)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def bulk_pages(self, request, pk=None):
        book = self.get_object()
        # try:
        pages_json = request.data["pages"]
        tif_root = request.data["tif_root"]
        page_list = BookCreator.create_pages_for_book(pages_json, book, tif_root)
        return Response(
            {"pages created": len(page_list)}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def bulk_lines(self, request, pk=None):
        book = self.get_object()
        # try:
        lines_json = request.data["lines"]
        line_list = BookCreator.create_lines_for_book(lines_json, book)
        return Response(
            {"lines created": len(line_list)}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def bulk_characters(self, request, pk=None):
        # try:
        characters_json = request.data["characters"]
        character_run_id = request.data["character_run_id"]
        if character_run_id is None:
            logging.info("Character run id is missing")
        if characters_json is None:
            logging.info("Characters list is missing")
        if character_run_id is None or characters_json is None:
            return Response({"error": "missing character run or characters"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Get character run
        character_run = models.CharacterRun.objects.get(id=character_run_id)
        if character_run is None:
            logging.info({"Missing character run": character_run_id})
            return Response({"error": f"missing character run for id: {character_run_id}"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            character_list = BookCreator.create_characters_for_book(characters_json, character_run)
            return Response({"characters created": len(character_list)}, status=status.HTTP_201_CREATED)
        except DatabaseError:
            logging.error("No characters created, error creating character run")
            return Response({"error": "There was an error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def bulk_pages_update(self, request, pk=None):
        # try:
        pages_json = request.data["pages"]
        tif_root = request.data["tif_root"]
        page_list = BookUpdater.update_pages_for_book(pages_json, tif_root)
        return Response(
            {"pages updated": len(page_list)}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def bulk_lines_update(self, request, pk=None):
        # try:
        lines_json = request.data["lines"]
        line_list = BookUpdater.update_lines_for_book(lines_json)
        return Response(
            {"lines updated": len(line_list)}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def bulk_characters_update(self, request, pk=None):
        # try:
        characters_json = request.data["characters"]
        if characters_json is None:
            return Response({"error": "missing character run or characters"}, status=status.HTTP_400_BAD_REQUEST)
        # Get character run
        first_character = models.Character.objects.get(id=characters_json[0]['id'])
        character_run_id = first_character.created_by_run.pk
        character_run = models.CharacterRun.objects.get(id=character_run_id)
        if character_run is None:
            return Response({"error": f"missing character run for id: {character_run_id}"},
                            status=status.HTTP_400_BAD_REQUEST)
        logging.info({"Updating character run": character_run_id})
        try:
            characters_count = BookUpdater.update_characters_for_book(characters_json, character_run)
            return Response(
                {"characters updated": characters_count}, status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response({"Error updating characters: ", str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpreadFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        help_text="Spreads from this book ID",
        widget=forms.TextInput,
    )
    sequence = filters.NumberFilter(help_text="Spread sequence index")


class SpreadViewSet(CRUDViewSet):
    """
    list: Spreads belong to a single `Book` instance, and are indexed by sequence in that book.
    """

    queryset = models.Spread.objects.prefetch_related(
        "book", "book__pageruns__pages"
    ).all()
    filterset_class = SpreadFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.SpreadDetailSerializer
        elif self.action == "list":
            return serializers.SpreadListSerializer
        return serializers.SpreadCreateSeralizer


# Run Views ----


class RunFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        help_text="Run associated with this book",
        widget=forms.TextInput,
    )


class PageRunViewSet(CRUDViewSet):
    queryset = models.PageRun.objects.all()
    filterset_class = RunFilter
    serializer_class = serializers.PageRunSerializer


class LineRunViewSet(CRUDViewSet):
    queryset = models.LineRun.objects.all()
    filterset_class = RunFilter
    serializer_class = serializers.LineRunSerializer


class CharacterRunViewSet(CRUDViewSet):
    queryset = models.CharacterRun.objects.all()
    filterset_class = RunFilter
    serializer_class = serializers.CharacterRunSerializer


class PageFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        help_text="Book ID for this page",
        field_name="created_by_run__book",
        widget=forms.TextInput,
    )
    sequence = filters.NumberFilter(
        field_name="sequence", help_text="The sequence of this page in the book"
    )
    side = filters.ChoiceFilter(
        choices=models.Page.SPREAD_SIDE, help_text="Which side of the page"
    )
    created_by_run = filters.ModelChoiceFilter(
        queryset=models.PageRun.objects.all(),
        help_text="The run ID that created this Page",
        widget=forms.TextInput,
    )


class PageViewSet(CRUDViewSet):
    """
    list: Pages belong to a single `Spread` instance, and are either marked as on the left (`l`) or right (`r`) side. Because the exact split of pages may differ run to run, they are also tied to a `Run` ID.
    """

    queryset = models.Page.objects.prefetch_related(
        "created_by_run__book__lineruns", "created_by_run"
    ).all()
    filterset_class = PageFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageDetailSerializer
        elif self.action == "list":
            return serializers.PageListSerializer
        return serializers.PageCreateSerializer


class LineFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        field_name="page__created_by_run__book",
        label="Book ID",
        help_text="Lines belonging to this book",
        widget=forms.TextInput,
    )
    page_sequence = filters.NumberFilter(
        field_name="page__sequence",
        label="Sequence",
        help_text="Lines belonging to a page with this sequence index",
    )
    page_side = filters.ChoiceFilter(
        choices=models.Page.SPREAD_SIDE,
        field_name="page__side",
        help_text="Lines belonging to a page on this side of a spread",
    )
    sequence = filters.NumberFilter(help_text="Order on page, from top to bottom")
    created_by_run = filters.ModelChoiceFilter(
        queryset=models.LineRun.objects.all(),
        help_text="Which pipeline run created these lines",
        widget=forms.TextInput,
    )


class LineViewSet(CRUDViewSet):
    queryset = models.Line.objects.all()
    filterset_class = LineFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineDetailSerializer
        elif self.action == "list":
            return serializers.LineListSerializer
        return serializers.LineCreateSerializer


class CharacterFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        field_name="created_by_run__book",
        label="Book ID",
        widget=forms.TextInput,
    )
    page_sequence = filters.NumberFilter(
        field_name="line__page__sequence", label="Page sequence"
    )
    page_sequence_gte = filters.NumberFilter(
        field_name="line__page__sequence",
        label="Page sequence (greater than or equal)",
        lookup_expr="gte",
    )
    page_sequence_lte = filters.NumberFilter(
        field_name="line__page__sequence",
        label="Page sequence (less than or equal)",
        lookup_expr="lte",
    )
    page_side = filters.ChoiceFilter(
        choices=models.Page.SPREAD_SIDE, field_name="line__page__side"
    )
    line_sequence = filters.NumberFilter(
        field_name="line__sequence", label="Line sequence"
    )
    sequence = filters.NumberFilter()
    created_by_run = filters.ModelChoiceFilter(
        queryset=models.CharacterRun.objects.all(), widget=forms.TextInput
    )
    character_class = filters.ModelChoiceFilter(
        queryset=models.CharacterClass.objects.all(), widget=forms.TextInput
    )
    human_character_class = filters.ModelChoiceFilter(
        queryset=models.CharacterClass.objects.all(), widget=forms.TextInput
    )
    damage_score_gte = filters.NumberFilter(
        field_name="damage_score",
        label="Damage score (greater than or equal)",
        lookup_expr="gte",
    )
    agreement = filters.ChoiceFilter(
        choices=(
            ("all", "all"),
            ("unknown", "unknown"),
            ("agreement", "agreement"),
            ("disagreement", "disagreement"),
        ),
        method="class_agreement",
        label="Machine/human class agreement",
    )
    has_grouping = filters.BooleanFilter(
        method="in_any_grouping", label="In at least one grouping?"
    )

    def class_agreement(self, queryset, name, value):
        if value == "unknown":
            return queryset.filter(human_character_class__isnull=True)
        elif value == "agreement":
            return queryset.filter(character_class__exact=F("human_character_class"))
        elif value == "disagreement":
            return queryset.exclude(character_class=F("human_character_class")).exclude(
                human_character_class__isnull=True
            )
        else:
            return queryset

    def in_any_grouping(self, queryset, name, value):
        if value:
            groupings = models.CharacterGrouping.objects.filter(
                characters=OuterRef("pk")
            )
            return (
                queryset.annotate(has_groupings=Exists(groupings))
                    .filter(has_groupings=True)
                    .all()
            )
        else:
            return queryset


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = (
        models.Character.objects.select_related(
            "line",
            "line__page",
            "created_by_run__book",
            "character_class",
            "human_character_class",
        )
            .annotate(
            lineseq=F("line__sequence"),
            pageseq=F("line__page__sequence"),
            bookseq=F("created_by_run__book__id"),
        )
            .all()
    )
    ordering_fields = [
        "class_probability",
        "bookseq",
        "pageseq",
        "lineseq",
        "sequence",
        "damage_score",
    ]
    filterset_class = CharacterFilter
    pagination_class = NoCountsLimitOffsetPagination

    def get_queryset(self):
        if self.action == "create":
            return models.Character.objects.all()
        else:
            return self.queryset.order_by('id')

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterDetailSerializer
        elif self.action == "list":
            return serializers.CharacterListSerializer
        return serializers.CharacterCreateSerializer

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def annotate(self, request):
        serializer = serializers.CharacterAnnotateSerializer(data=request.data)
        if serializer.is_valid():
            target_characters = [
                char.id for char in serializer.validated_data["characters"]
            ]

            models.Character.objects.filter(id__in=target_characters).update(
                human_character_class=serializer.validated_data["human_character_class"]
            )
            return Response({"status": f"{len(target_characters)} updated"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterClassFilter(filters.FilterSet):
    character_class = filters.CharFilter(
        help_text="Partial text match for character class label",
        lookup_expr="icontains",
    )


class CharacterClassViewset(CRUDViewSet):
    queryset = models.CharacterClass.objects.all()
    serializer_class = serializers.CharacterClassSerializer
    filterset_class = CharacterClassFilter


class CharacterGroupingFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name="created_by__username")
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        # field_name="characters__created_by_run__book",
        method="characters_from_book",
        label="Book ID",
        widget=forms.TextInput,
    )

    def characters_from_book(self, queryset, name, value):
        if value:
            characters = models.Character.objects.filter(
                created_by_run__book=value, charactergroupings=OuterRef("pk")
            )
            return (
                queryset.annotate(chars_from_book=Exists(characters))
                    .filter(chars_from_book=True)
                    .all()
            )
        return queryset


class CharacterGroupingViewSet(CRUDViewSet, GetSerializerClassMixin):
    detail_queryset = (
        models.CharacterGrouping.objects.select_related("created_by")
            .prefetch_related("characters__line__page")
            .all()
    )
    list_queryset = models.CharacterGrouping.objects.select_related("created_by").all()
    queryset = detail_queryset

    serializer_action_classes = {"list": list_queryset, "detail": detail_queryset}
    filterset_class = CharacterGroupingFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterGroupingDetailSerializer
        elif self.action == "list":
            return serializers.CharacterGroupingListSerializer
        return serializers.CharacterGroupingCreateSerializer

    @action(detail=True, methods=["patch"])
    @transaction.atomic
    def add_characters(self, request, pk=None):
        obj = self.get_object()
        serializer = serializers.CharacterGroupingCharacterListSerializer(
            data=request.data
        )
        if serializer.is_valid():
            for char in serializer.data["characters"]:
                logging.info({"adding character": char})
                obj.characters.add(char)
            return Response({"status": "characters added"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    @transaction.atomic
    def delete_characters(self, request, pk=None):
        obj = self.get_object()
        serializer = serializers.CharacterGroupingCharacterListSerializer(
            data=request.data
        )
        if serializer.is_valid():
            for char in serializer.data["characters"]:
                obj.characters.remove(char)
            return Response({"status": "characters removed"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    @transaction.atomic
    def move_characters(self, request, pk=None):
        target_group_id = request.GET['target_group']
        if target_group_id is None:
            return Response("Missing target character group id", status=status.HTTP_400_BAD_REQUEST)
        target_group = models.CharacterGrouping.objects.get(id=target_group_id)
        if target_group is None:
            return Response(f"Target character group not found for id: {target_group_id}",
                            status=status.HTTP_400_BAD_REQUEST)
        current_character_group = self.get_object()
        serializer = serializers.CharacterGroupingCharacterListSerializer(
            data=request.data
        )
        if serializer.is_valid():
            for char in serializer.data["characters"]:
                current_character_group.characters.remove(char)
                target_group.characters.add(char)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "characters moved"})

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        obj = self.get_object()

        zip_file_name = f"character_group-{slugify(obj.label)}-{obj.id}.tar.gz"

        if obj.characters.count() < 1:
            return Response(
                [{"error": "This character group has no characters to download"}],
                status=status.HTTP_400_BAD_REQUEST,
            )

        image_objects = (
            models.Character.objects.filter(charactergroupings=obj)
                .select_related("line__page")
                .all()
        )

        with TemporaryDirectory(dir=settings.DOWNLOAD_SCRATCH_DIR) as scratch_dir:
            zip_file = tarfile.open(f"{scratch_dir}/cg.tar.gz", "w:gz")
            for img in image_objects:
                filename = f"{img.label}.tif"
                # Make requests out to the iiif endpoint and send back the files
                # TODO stream the zip response as we request images, rather than waiting for all the images to be done first.
                direct_url = img.full_tif
                download_destination = f"{scratch_dir}/{filename}"
                tif_response = requests.get(direct_url, verify=settings.CA_CERT_ROUTE)
                open(download_destination, "wb").write(tif_response.content)
                zip_file.add(download_destination, arcname=filename)
            zip_file.close()
            response = FileResponse(
                open(zip_file.name, "rb"), content_type="application/gzip"
            )
            response["Content-Disposition"] = f"attachment; filename={zip_file_name}"
            return response
