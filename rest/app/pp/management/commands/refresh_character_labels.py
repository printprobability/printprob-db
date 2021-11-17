from django.core.management.base import BaseCommand
from django.db.models import CharField, OuterRef, Subquery, ExpressionWrapper, F, Value as V
from django.db.models.functions import Concat
from pp import models

class Command(BaseCommand):
    help = "Refresh all materialized labels for Characters."

    def add_arguments(self, parser):
        parser.add_argument("--cached", action="store_true", help="Only refresh objects with no labels")

    def handle(self, *args, **options):

        use_cache = options["cached"]

        if (use_cache):
            qs = models.Character.objects.filter(label="")
        else:
            qs = models.Character.objects.all()

        book_label = models.Book.objects.filter(characterruns__characters=OuterRef("id")).annotate(tlabel = F("label")).values("tlabel")

        page_label = models.Page.objects.filter(lines__characters=OuterRef("id")).annotate(tlabel = ExpressionWrapper(Concat(V(" p. "), "sequence", V("-"), "side"), output_field=CharField())).values("tlabel")

        line_label = models.Line.objects.filter(characters=OuterRef("id")).annotate(tlabel = ExpressionWrapper(Concat(V(" l. "), "sequence"), output_field=CharField())).values("tlabel")

        update_result = qs.update(
          label = Concat("character_class_id", V(" - "), Subquery(book_label), Subquery(page_label), Subquery(line_label), V(" c. "), "sequence")
        )

        print(update_result)
