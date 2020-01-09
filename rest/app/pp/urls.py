from django.urls import path, include
from django.views.generic import TemplateView
import django.contrib.auth.views as auth_views
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet)
router.register(r"spreads", views.SpreadViewSet)
router.register(r"pages", views.PageViewSet)
router.register(r"lines", views.LineViewSet)
router.register(r"linegroups", views.LineGroupViewSet)
router.register(r"characters", views.CharacterViewSet)
router.register(r"runs/pages", views.PageRunViewSet)
router.register(r"runs/lines", views.LineRunViewSet)
router.register(r"runs/linegroups", views.LineGroupRunViewSet)
router.register(r"runs/characters", views.CharacterRunViewSet)
router.register(r"character_classes", views.CharacterClassViewset)
router.register(r"character_groupings", views.CharacterGroupingViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Print & Probability",
        default_version="v1",
        description="API for Print & Probability data processing pipeline.",
        contact=openapi.Contact(email="mlincoln@andrew.cmu.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("user/", views.UserView.as_view(), name="user-profile"),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
