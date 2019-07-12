from django.shortcuts import render
from rest_framework import viewsets, views, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from rest_framework import permissions
from django_filters import rest_framework as filters
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
    filepath = filters.CharFilter(field_name="files__filepath", distinct=True)
    depicted_spreads = filters.ModelChoiceFilter(queryset=models.Spread.objects.all())
    depicted_pages = filters.ModelChoiceFilter(queryset=models.Page.objects.all())
    depicted_lines = filters.ModelChoiceFilter(queryset=models.Line.objects.all())
    depicted_characters = filters.ModelChoiceFilter(
        queryset=models.Character.objects.all()
    )


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.QuickImageSerializer,
    )
    @transaction.atomic
    def quick_create(self, request):
        """
        Supply a tif and jpeg filepath of the same image to quickly create Image and ImageFile instances.
        """
        quick_image = serializers.QuickImageSerializer(data=request.data)
        if quick_image.is_valid():
            # Create a new Image instance
            image = models.Image.objects.create(notes=quick_image.data["notes"])

            # Create ImageFile instances
            jpeg_file = models.ImageFile.objects.create(
                parent_image=image, filetype="jpg", filepath=quick_image.data["jpeg"]
            )
            tiff_file = models.ImageFile.objects.create(
                parent_image=image, filetype="tif", filepath=quick_image.data["tiff"]
            )

            # Hook the Image web_file image up
            image.web_file = jpeg_file
            image.save()

            # Return the serialized Image object
            serialized_image = serializers.ImageSerializer(image)
            return Response(serialized_image.data)
        else:
            # Otherwise return an error
            return Response(quick_image.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageFileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.ImageFile.objects.all()
    serializer_class = serializers.ImageFileSerializer


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


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Page.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("spread__book", "spread", "side", "created_by_run")

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
    )
    spread_sequence = filters.NumberFilter(
        field_name="page__spread__sequence", label="Spread sequence"
    )
    page_side = filters.ChoiceFilter(
        choices=models.Page.SPREAD_SIDE, field_name="page__side"
    )
    sequence = filters.NumberFilter()
    created_by_run = filters.ModelChoiceFilter(queryset=models.Run.objects.all())


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

