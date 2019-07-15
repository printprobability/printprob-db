from django.shortcuts import render
from rest_framework import viewsets, views, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from rest_framework import permissions
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from . import models, serializers


class RunViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns the given pipeline start timestamp and notes, and id lists of all books, spreads, pages, lines, and characters processed under that run.

    list:
    Returns a list of pipline run IDs with start timestamps and notes.

    create:
    Create a new run with optional notes. A timestamp is automatically generated.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Run.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.RunDetailSerializer
        return serializers.RunListSerializer


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


class ImageViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns an image descripton with lists of all file formats available for that image.

    list:
    Returns a list of images, with references to thier file versions and a URL for the preferred web version of the image.

    create:
    Create a new image record by specifying both the jpg and tif paths.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter


class BookFilter(filters.FilterSet):
    vid = filters.NumberFilter(help_text="Numeric VID")
    title = filters.CharFilter(
        help_text="books with titles containing this string (case insensitive)",
        lookup_expr="icontains",
    )
    publisher = filters.CharFilter(
        help_text="books with publisher labels containing this string (case insensitive)",
        lookup_expr="icontains",
    )


class BookViewSet(viewsets.ModelViewSet):
    """
    list: Lists all books. Along with [`CharacterClass`](#character-class-create), `Book` instances use a human-readable ID (here, the ESTC id) rather than a UUID.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Book.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BookDetailSerializer
        return serializers.BookListSerializer


class SpreadFilter(filters.FilterSet):
    book = filters.ModelChoiceFilter(
        queryset=models.Book.objects.all(), help_text="Spreads from this book ID"
    )
    sequence = filters.NumberFilter(help_text="Spread sequence index")


class SpreadViewSet(viewsets.ModelViewSet):
    """
    list: Spreads belong to a single `Book` instance, and are indexed by sequence in that book.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Spread.objects.all()
    serializer_class = serializers.SpreadSeralizer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpreadFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.SpreadDetailSerializer
        elif self.action == "list":
            return serializers.SpreadListSerializer
        return serializers.SpreadSeralizer


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
        queryset=models.Run.objects.all(), help_text="The run ID that created this Page"
    )


class PageViewSet(viewsets.ModelViewSet):
    """
    list: Pages belong to a single `Spread` instance, and are either marked as on the left (`l`) or right (`r`) side. Because the exact split of pages may differ run to run, they are also tied to a `Run` ID.
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Page.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PageFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageDetailSerializer
        elif self.action == "list":
            return serializers.PageListSerializer
        return serializers.PageSerializer


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
        queryset=models.Run.objects.all(),
        help_text="Which pipeline run created these lines",
    )


class LineViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Line.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LineFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineDetailSerializer
        elif self.action == "list":
            return serializers.LineListSerializer
        return serializers.LineSerializer


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
    created_by_run = filters.ModelChoiceFilter(queryset=models.Run.objects.all())
    character_class = filters.ModelChoiceFilter(
        queryset=models.CharacterClass.objects.all()
    )


class CharacterViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Character.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CharacterFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterDetailSerializer
        return serializers.CharacterListSerializer


class CharacterClassViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.CharacterClass.objects.all()
    serializer_class = serializers.CharacterClassSerializer

