from django.urls import path, include
import django.contrib.auth.views as auth_views
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
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


schema_view = get_schema_view(
    openapi.Info(
        title="P&P API",
        default_version="v1",
        description="Test description",
        contact=openapi.Contact(email="mlincoln@andrew.cmu.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
