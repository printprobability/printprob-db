from django.shortcuts import render
from rest_framework import viewsets, views, generics, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework import permissions
from django_filters import rest_framework as filters
from . import models, serializers


class CRUDViewSet(viewsets.ModelViewSet):
    http_method_names = [u"get", u"post", u"delete", u"head", u"options", u"trace"]


class BookFilter(filters.FilterSet):
    eebo = filters.NumberFilter(help_text="Numeric EEBO ID")
    vid = filters.NumberFilter(help_text="Numeric VID")
    title = filters.CharFilter(
        help_text="books with titles containing this string (case insensitive)",
        lookup_expr="icontains",
    )
    publisher = filters.CharFilter(
        help_text="books with publisher labels containing this string (case insensitive)",
        lookup_expr="icontains",
    )
    pdf = filters.CharFilter(help_text="book with this PDF filepath")


class BookViewSet(CRUDViewSet):
    """
    list: Lists all books. Along with [`CharacterClass`](#character-class-create), `Book` instances use a human-readable ID (here, the EEBO id) rather than a UUID.
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
        queryset=models.Book.objects.all(), help_text="Spreads from this book ID"
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
        queryset=models.Book.objects.all(), help_text="Run associated with this book"
    )


class PageRunViewSet(CRUDViewSet):
    queryset = models.PageRun.objects.all()
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


class ImageFilter(filters.FilterSet):
    filepath = filters.CharFilter(
        field_name="files__filepath",
        distinct=True,
        help_text="Retrive the image pointer that references this file",
    )
    depicted_spreads = filters.ModelChoiceFilter(
        queryset=models.Spread.objects.all(),
        help_text="Retrieve image that depicts this spread id",
    )
    depicted_pages = filters.ModelChoiceFilter(
        queryset=models.Page.objects.all(),
        help_text="Retrive the image that depicts this page id",
    )
    depicted_lines = filters.ModelChoiceFilter(
        queryset=models.Line.objects.all(),
        help_text="Retrive the image that depicts this line id",
    )
    depicted_characters = filters.ModelChoiceFilter(
        queryset=models.Character.objects.all(),
        help_text="Retrieve the image that depicts this character id",
    )


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
    filterset_class = ImageFilter


class PageFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(),
        help_text="Book ID for this page",
        field_name="spread__book",
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
        queryset=models.Book.objects.all(), field_name="spread__book", label="Book ID"
    )
    spread_sequence = filters.NumberFilter(
        field_name="spread__sequence", help_text="Spread sequence number in the book"
    )
    spread_id = filters.ModelChoiceFilter(
        queryset=models.Spread.objects.all(), field_name="spread", label="Spread ID"
    )
    page = (
        filters.ModelChoiceFilter(
            queryset=models.Page.objects.all(), field_name="pages__pk", label="Page ID"
        ),
    )
    created_by_run = filters.ModelChoiceFilter(
        queryset=models.LineGroupRun.objects.all(), label="Line Group Run ID"
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
        queryset=models.CharacterRun.objects.all()
    )
    character_class = filters.ModelChoiceFilter(
        queryset=models.CharacterClass.objects.all()
    )


class CharacterViewSet(CRUDViewSet):
    queryset = models.Character.objects.select_related("image").all()
    filterset_class = CharacterFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterDetailSerializer
        elif self.action == "list":
            return serializers.CharacterListSerializer
        return serializers.CharacterCreateSerializer


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


class CharacterGroupingViewSet(viewsets.ModelViewSet):
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
