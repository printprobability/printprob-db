from django.urls import path, include
import django.contrib.auth.views as auth_views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter()
router.register(r"runs", views.RunViewSet)
router.register(r"books", views.BookViewSet)
router.register(r"spreads", views.SpreadViewSet)
router.register(r"pages", views.PageViewSet)
router.register(r"lines", views.LineViewSet)
router.register(r"characters", views.CharacterViewSet)
router.register(r"images", views.ImageViewSet)
router.register(r"files", views.ImageFileViewSet)
router.register(r"character_classes", views.CharacterClassViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="P & P Pipeline API")),
]
