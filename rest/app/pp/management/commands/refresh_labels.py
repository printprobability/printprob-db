from django.core import management
from django.core.management.base import BaseCommand
from pp import models
from tqdm import tqdm


class Command(BaseCommand):
    help = "Refresh all materialized labels for a Page, Line, Character, etc."

    def add_arguments(self, parser):
        parser.add_argument("--cached", action="store_true", help="Only refresh objects with no labels")

    def handle(self, *args, **options):
        labelled_models = [
            models.Book,
            models.PageRun,
            models.LineRun,
            models.CharacterRun,
            models.Spread,
            models.Page,
            models.Line,
            models.Character,
        ]

        use_cache = options["cached"]

        for m in labelled_models:
            print(m)
            if (use_cache):
                qs = m.objects.filter(label="")
            else:
                qs = m.objects.all()
            for i in tqdm(qs, total=qs.count()):
                i.save()
