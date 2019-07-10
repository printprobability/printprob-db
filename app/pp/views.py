from django.shortcuts import render
from rest_framework import viewsets, views, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import permissions

from . import models, serializers


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Book.objects.annotate(n_pages=Count("spreads__pages")).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BookDetailSerializer
        return serializers.BookListSerializer


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Page.objects.annotate(n_lines=Count("lines")).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PageDetailSerializer
        return serializers.PageListSerializer


class LineViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Line.objects.annotate(
        n_chars=Count("characters"), n_images=Count("images")
    ).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.LineDetailSerializer
        return serializers.LineListSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Character.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CharacterDetailSerializer
        return serializers.CharacterListSerializer


class BadCaptureViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.BadCapture.objects.all()
    serializer_class = serializers.BadCaptureSeralizer
    lookup_field = "image"
