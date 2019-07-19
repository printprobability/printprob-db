from django.urls import path, include
from django.views.generic import TemplateView
import django.contrib.auth.views as auth_views
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view

from . import views

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet)
router.register(r"spreads", views.SpreadViewSet)
router.register(r"pages", views.PageViewSet)
router.register(r"lines", views.LineViewSet)
router.register(r"line_groups", views.LineGroupViewSet)
router.register(r"characters", views.CharacterViewSet)
router.register(r"images", views.ImageViewSet)
router.register(r"runs/pages", views.PageRunViewSet)
router.register(r"runs/lines", views.LineRunViewSet)
router.register(r"runs/line_groups", views.LineGroupRunViewSet)
router.register(r"runs/characters", views.CharacterRunViewSet)
router.register(r"character_classes", views.CharacterClassViewset)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "schema",
        get_schema_view(
            title="Print & Probability",
            description="API for Print & Probability data processing pipeline.",
        ),
        name="openapi-schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
]
