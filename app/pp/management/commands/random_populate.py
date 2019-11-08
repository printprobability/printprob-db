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
    help = "Fill database with random images"

    def add_arguments(self, parser):
        parser.add_argument("n_books", nargs="+", type=int)

    def handle(self, *args, **options):

        n_books = options["n_books"][0]

        ff = Faker()

        print("Generating books")
        for i in tqdm(range(1, n_books + 1)):
            book = models.Book.objects.create(
                eebo=random.randrange(500000),
                vid=random.randrange(500000),
                pq_title=ff.sentence(
                    nb_words=30, variable_nb_words=True, ext_word_list=None
                ),
                pq_author=ff.sentence(
                    nb_words=10, variable_nb_words=True, ext_word_list=None
                ),
                pq_publisher=ff.sentence(
                    nb_words=15, variable_nb_words=True, ext_word_list=None
                ),
                pq_url=ff.file_path(depth=3, extension="pdf"),
                date_early=ff.date(pattern="%Y-%m-%d", end_datetime=None),
                date_late=ff.date(pattern="%Y-%m-%d", end_datetime=None),
            )

        def quickimage():
            return models.Image.objects.create(
                tif=ff.file_path(depth=3, extension="tif"), tif_md5=uuid4()
            )

        books = models.Book.objects.all()

        print("Generating spreads")
        for book in tqdm(books):
            for i in range(0, 3):
                models.Spread.objects.create(book=book, sequence=i, image=quickimage())

        print("Generating pages")
        for book in tqdm(books):
            page_run = models.PageRun.objects.create(book=book)
            for spread in book.spreads.all():
                for s in ["l", "r"]:
                    models.Page.objects.create(
                        spread=spread,
                        created_by_run=page_run,
                        side=s,
                        image=quickimage(),
                        x=random.randrange(0, 500),
                        y=random.randrange(0, 500),
                        w=random.randrange(0, 500),
                        h=random.randrange(0, 500),
                        rot1=random.randrange(0, 500),
                        rot2=random.randrange(0, 500),
                    )

        print("Generating lines")

        def gen_lines(book):
            line_run = models.LineRun.objects.create(book=book)
            for page in tqdm(
                models.Page.objects.filter(spread__book=book).all(), leave=False
            ):
                for i in range(0, 3):
                    models.Line.objects.create(
                        page=page,
                        created_by_run=line_run,
                        image=quickimage(),
                        sequence=i,
                        y_min=random.randrange(0, 500),
                        y_max=random.randrange(0, 500),
                    )

        def gen_all_lines(books):
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = list(tqdm(pool.map(gen_lines, books), total=books.count()))
            return results

        gen_all_lines(books)

        print("Generating linegroups")

        def gen_linegroups(book):
            linegroup_run = models.LineGroupRun.objects.create(book=book)
            for page in tqdm(
                models.Page.objects.filter(spread__book=book).all(), leave=False
            ):
                for i in range(0, 1):
                    lg = models.LineGroup.objects.create(
                        page=page, created_by_run=linegroup_run
                    )
                    for line in models.Line.objects.filter(page=page).order_by("?")[:1]:
                        lg.lines.add(line)

        def gen_all_linegroups(books):
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = list(
                    tqdm(pool.map(gen_linegroups, books), total=books.count())
                )
            return results

        gen_all_linegroups(books)

        all_letters = list(string.ascii_letters)

        for cc in all_letters:
            models.CharacterClass.objects.get_or_create(classname=cc)

        all_classes = list(models.CharacterClass.objects.all())

        print("Generating characters")

        def gen_chars(book):
            character_run = models.CharacterRun.objects.create(book=book)
            book_lines = models.Line.objects.filter(page__spread__book=book).all()

            for line in tqdm(book_lines, leave=False):
                for i in range(0, 3):
                    randclass = all_classes[random.randrange(0, 52)]
                    models.Character.objects.create(
                        line=line,
                        created_by_run=character_run,
                        data=os.urandom(1024),
                        sequence=i,
                        x_min=random.randrange(0, 500),
                        x_max=random.randrange(0, 500),
                        character_class=randclass,
                        class_probability=random.random(),
                    )

        def gen_all_chars(books):
            with ThreadPoolExecutor(max_workers=4) as pool:
                tqdm(pool.map(gen_chars, books), total=books.count())

        gen_all_chars(books)

