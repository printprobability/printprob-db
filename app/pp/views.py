from django.shortcuts import render
from rest_framework import viewsets, views, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from rest_framework import permissions

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


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

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

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.SpreadSeralizer
        return serializers.ReadSpreadSeralizer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Page.objects.annotate(n_lines=Count("lines")).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageDetailSerializer
        return serializers.PageListSerializer


class LineViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Line.objects.annotate(
        n_chars=Count("characters"), n_images=Count("images")
    ).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineDetailSerializer
        return serializers.LineListSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Character.objects.all()

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


class ClassAssignmentViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.ClassAssignment.objects.all()
    serializer_class = serializers.ClassAssignmentSerializer
