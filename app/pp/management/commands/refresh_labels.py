from django.core import management
from django.core.management.base import BaseCommand
from pp import models
from tqdm import tqdm


class Command(BaseCommand):
    help = "Refresh all materialized labels for a Page, Line, Character, etc."

    def handle(self, *args, **options):
        labelled_models = [
            models.Image,
            models.Book,
            models.PageRun,
            models.LineRun,
            models.CharacterRun,
            models.Spread,
            models.Line,
            models.Page,
            models.Character,
        ]

        for m in labelled_models:
            print(m)
            for i in tqdm(m.objects.all()):
                i.save()
