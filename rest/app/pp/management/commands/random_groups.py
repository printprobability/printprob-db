from pp import models
from uuid import uuid4
from faker import Faker
import random
import string
from tqdm import tqdm
from django.core import management
from django.core.management.base import BaseCommand
from concurrent.futures import ThreadPoolExecutor
import os


class Command(BaseCommand):
    help = "Create a lot of new character curation groups"

    def handle(self, *args, **options):

        n_groups = 250

        ff = Faker()

        for i in tqdm(range(1, n_groups + 1)):
            group = models.CharacterGrouping.objects.create(
                label=ff.sentence(
                    nb_words=5, variable_nb_words=True, ext_word_list=None
                ),
                notes=ff.sentence(
                    nb_words=150, variable_nb_words=True, ext_word_list=None
                ),
                created_by=models.User.objects.first(),
            )
            adding_chars = models.Character.objects.order_by("?")[0:30]
            group.characters.set(adding_chars)
            group.save()
