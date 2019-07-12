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
    files__filepath = filters.CharFilter()
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

    @action(detail=False, methods=["post"])
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


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Book.objects.annotate(n_pages=Count("spreads__pages")).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BookDetailSerializer
        return serializers.BookListSerializer


class SpreadViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Spread.objects.all()
    serializer_class = serializers.SpreadSeralizer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("book", "sequence")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.SpreadDetailSerializer
        elif self.action == "list":
            return serializers.SpreadListSerializer
        return serializers.SpreadSeralizer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Page.objects.annotate(n_lines=Count("lines")).all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("spread__book", "spread", "side", "created_by_run")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageDetailSerializer
        elif self.action == "list":
            return serializers.PageListSerializer
        return serializers.PageSerializer


class LineViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Line.objects.annotate(
        n_chars=Count("characters"), n_images=Count("images")
    ).all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "page__spread__book",
        "page__spread__sequence",
        "page__side",
        "sequence",
        "created_by_run",
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineDetailSerializer
        elif self.action == "list":
            return serializers.LineListSerializer
        return serializers.LineSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Character.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "line__page__spread__book",
        "line",
        "sequence",
        "created_by_run",
        "character_class",
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterDetailSerializer
        return serializers.CharacterListSerializer


class BadCaptureViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.BadCapture.objects.all()
    serializer_class = serializers.BadCaptureSeralizer
    lookup_field = "image"


class CharacterClassViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.CharacterClass.objects.all()
    serializer_class = serializers.CharacterClassSerializer

