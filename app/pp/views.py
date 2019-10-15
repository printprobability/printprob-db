import zipfile
import os
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.conf import settings
from django.utils.text import slugify
from rest_framework import (
    viewsets,
    views,
    generics,
    status,
    mixins,
    pagination,
    parsers,
    exceptions,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count, F, Q, Exists, OuterRef
from django.contrib.auth.models import User
from rest_framework import permissions
from django_filters import rest_framework as filters
from . import models, serializers
from base64 import b64encode


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
    images = filters.BooleanFilter(
        method="has_images",
        label="Has images?",
        help_text="Has been processed on Bridges?",
    )
    year_early = filters.DateFilter(method="after_early", label="Started after date")
    year_late = filters.DateFilter(method="before_late", label="Finished before date")
    order = filters.OrderingFilter(
        fields=(
            ("pq_title", "Title"),
            ("pq_author", "Author"),
            ("date_early", "Published after"),
        )
    )

    def has_images(self, queryset, name, value):
        page_run = models.PageRun.objects.filter(book=OuterRef("pk"))
        line_run = models.LineRun.objects.filter(book=OuterRef("pk"))
        character_run = models.CharacterRun.objects.filter(book=OuterRef("pk"))

        if value:
            return (
                queryset.annotate(
                    has_pages=Exists(page_run),
                    has_lines=Exists(line_run),
                    has_characters=Exists(character_run),
                )
                .filter(Q(has_pages=True) | Q(has_lines=True) | Q(has_characters=True))
                .all()
            )
        return queryset

    def after_early(self, queryset, name, value):
        return queryset.filter(date_early__gte=value)

    def before_late(self, queryset, name, value):
        return queryset.filter(date_late__lte=value)


class BookViewSet(CRUDViewSet):
    """
    list: Lists all books.
    """

    queryset = (
        models.Book.objects.annotate(n_spreads=Count("spreads"))
        .prefetch_related(
            "spreads",
            "pageruns",
            "pageruns__pages",
            "lineruns",
            "linegroupruns__linegroups",
            "characterruns",
        )
        .all()
    )
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BookDetailSerializer
        elif self.action == "list":
            return serializers.BookListSerializer
        return serializers.BookCreateSerializer


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
    queryset = models.PageRun.objects.prefetch_related("pages").all()
    filterset_class = RunFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageRunDetailSerializer
        elif self.action == "list":
            return serializers.PageRunListSerializer
        return serializers.PageRunCreateSerializer


class LineRunViewSet(CRUDViewSet):
    queryset = models.LineRun.objects.all()
    filterset_class = RunFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineRunDetailSerializer
        elif self.action == "list":
            return serializers.LineRunListSerializer
        return serializers.LineRunCreateSerializer


class LineGroupRunViewSet(CRUDViewSet):
    queryset = models.LineGroupRun.objects.all()
    filterset_class = RunFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineGroupRunDetailSerializer
        elif self.action == "list":
            return serializers.LineGroupRunListSerializer
        return serializers.LineGroupRunCreateSerializer


class CharacterRunViewSet(CRUDViewSet):
    queryset = models.CharacterRun.objects.all()
    filterset_class = RunFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterRunDetailSerializer
        elif self.action == "list":
            return serializers.CharacterRunListSerializer
        return serializers.CharacterRunCreateSerializer


class ImageViewSet(CRUDViewSet):
    """
    retrieve:
    Returns an image descripton with lists of all file formats available for that image.

    list:
    Returns a list of images, with references to thier file versions and a URL for the preferred web version of the image.

    create:
    Create a new image record by specifying both the jpg and tif paths.
    """

    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer


class PageFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        help_text="Book ID for this page",
        field_name="spread__book",
        widget=forms.TextInput,
    )
    spread_sequence = filters.NumberFilter(
        field_name="spread__sequence",
        help_text="The spread sequence integer this page belongs to",
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
        "spread__book__lineruns", "created_by_run"
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
        field_name="page__spread__book",
        label="Book ID",
        help_text="Lines belonging to this book",
        widget=forms.TextInput,
    )
    spread_sequence = filters.NumberFilter(
        field_name="page__spread__sequence",
        label="Spread sequence",
        help_text="Lines belonging to a spread with this sequence index",
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


class LineGroupFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        field_name="spread__book",
        label="Book ID",
        widget=forms.TextInput,
    )
    spread_sequence = filters.NumberFilter(
        field_name="spread__sequence", help_text="Spread sequence number in the book"
    )
    spread_id = filters.ModelChoiceFilter(
        queryset=models.Spread.objects.all(),
        field_name="spread",
        label="Spread ID",
        widget=forms.TextInput,
    )
    page = (
        filters.ModelChoiceFilter(
            queryset=models.Page.objects.all(),
            field_name="pages__pk",
            label="Page ID",
            widget=forms.TextInput,
        ),
    )
    created_by_run = filters.ModelChoiceFilter(
        queryset=models.LineGroupRun.objects.all(),
        label="Line Group Run ID",
        widget=forms.TextInput,
    )


class LineGroupViewSet(CRUDViewSet):
    queryset = models.LineGroup.objects.all()
    filterset_class = LineGroupFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineGroupDetailSerializer
        elif self.action == "list":
            return serializers.LineGroupListSerializer
        return serializers.LineGroupCreateSerializer


class CharacterFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        field_name="line__page__spread__book",
        label="Book ID",
        widget=forms.TextInput,
    )
    spread_sequence = filters.NumberFilter(
        field_name="line__page__spread__sequence", label="Spread sequence"
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
    order = filters.OrderingFilter(fields=(("class_probability", "class_probability"),))

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


class characterPagination(pagination.CursorPagination):
    ordering = "-class_probability"


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = (
        models.Character.objects.select_related(
            "line",
            "line__page",
            "line__page__spread",
            "line__page__spread__book",
            "character_class",
            "human_character_class",
        )
        .defer("data")
        .all()
    )
    filterset_class = CharacterFilter
    pagination_class = characterPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterDetailSerializer
        elif self.action == "list":
            return serializers.CharacterListSerializer
        return serializers.CharacterCreateSerializer

    @action(detail=True, methods=["get"])
    def file(self, request, pk=None):
        obj = self.get_object()
        response = HttpResponse(bytes(obj.data), content_type="image/png")
        response["Content-Transfer-Encoding"] = "base64"
        response["Content-Disposition"] = f"filename={obj.id}.tiff"
        return response

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


class CharacterGroupingViewSet(CRUDViewSet):
    queryset = models.CharacterGrouping.objects.select_related(
        "created_by"
    ).prefetch_related("characters", "characters__image")
    filterset_class = CharacterGroupingFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterGroupingDetailSerializer
        elif self.action == "list":
            return serializers.CharacterGroupingListSerializer
        return serializers.CharacterGroupingCreateSerializer

    @action(detail=True, methods=["patch"])
    def add_characters(self, request, pk=None):
        obj = self.get_object()
        serializer = serializers.CharacterGroupingCharacterListSerializer(
            data=request.data
        )
        if serializer.is_valid():
            for char in serializer.data["characters"]:
                obj.characters.add(char)
            return Response({"status": "characters added"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
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

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        response = HttpResponse(content_type="application/zip")
        obj = self.get_object()

        zip_file_name = f"character_group-{slugify(obj.label)}-{obj.id}.zip"

        if obj.characters.count() < 1:
            return Response(
                [{"error": "This character group has no characters to download"}],
                status=status.HTTP_400_BAD_REQUEST,
            )
        filenames = obj.characters.all().values_list("image__jpg", flat=True)

        zip_file = zipfile.ZipFile(response, "w")
        for filename in filenames:
            fdir, fname = os.path.split(filename)
            zip_file.write(f"{settings.REAL_IMAGE_BASEDIR}/{filename}", fname)
        zip_file.close()
        response["Content-Disposition"] = f"attachment; filename={zip_file_name}"

        return response
