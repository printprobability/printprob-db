from django.core import management
from django.core.management.base import BaseCommand
from django.db.models import Q
from pp import models


class Command(BaseCommand):
    help = "Wipe all images not referenced by a Page, Line, Character, etc."

    def handle(self, *args, **options):
        models.Image.objects.exclude(spreads__isnull=False).exclude(
            pages__isnull=False
        ).exclude(lines__isnull=False).exclude(characters__isnull=False).delete()
