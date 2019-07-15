from django.core import management
from django.core.management.base import BaseCommand
from django.db.models import Q
from pp import models


class Command(BaseCommand):
    help = "Wipe all images not referenced by a Page, Line, Character, etc."

    def handle(self, *args, **options):
        models.Image.objects.exclude(depicts_spread__isnull=False).exclude(
            depicts_page__isnull=False
        ).exclude(depicts_line__isnull=False).exclude(
            depicts_character__isnull=False
        ).delete()
