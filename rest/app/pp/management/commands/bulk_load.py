from pp import models
from django.core.management.base import BaseCommand
import json
import logging
from uuid import UUID
from django.db import transaction
import concurrent.futures

from pp.util import ArrayDivideUtil

TIF_ROOT = "/ocean/projects/hum160002p/shared"


class Command(BaseCommand):
    help = "Load segmented book components from a directory path"

    def add_arguments(self, parser):
        parser.add_argument(
            "-b",
            "--book_id",
            dest="book_id",
            help="UUID of the book from printprobability.bridges.psc.edu",
        )
        parser.add_argument(
            "-j",
            "--json",
            dest="json",
            help="Absolute directory path (starting with /pylon5) where the Ocular JSON output is stored.",
        )

    def handle(self, *args, **options):
        book_id = options["book_id"]
        directory = options["json"]

        bl = BookLoader(book_id=book_id, json_directory=directory)
        bl.load_db()


class CharacterClasses:
    """
    Utility to create a hashmap of Ocular character codes to database IDs, so that we don't need to check every single time
    """

    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

    data = {}

    def load_character_classes(self):
        """
        Create a dict of all currently-loaded character classes
        """
        for cc in models.CharacterClass.objects.all():
            self.data[cc.classname] = cc.classname

    def get_or_create(self, ocular_code):
        if ocular_code == "":
            ocular_code = "space"
        elif ocular_code == ".":
            ocular_code = "period"
        elif ocular_code == ";":
            ocular_code = "semicolon"
        elif ocular_code == "/":
            ocular_code = "slash"
        elif ocular_code == "\\":
            ocular_code = "backslash"
        try:
            return self.data[ocular_code]
        except:
            models.CharacterClass.objects.create(
                classname=ocular_code, label=ocular_code
            )
            # update the existing dict
            self.data[ocular_code] = ocular_code


class BookLoader:
    def __init__(self, book_id, json_directory):
        self.book_id = book_id
        self.json_directory = json_directory
        self.cc = CharacterClasses()
        self.cc.load_character_classes()

    @transaction.atomic
    def load_db(self):
        self.confirm_book()
        self.load_json()
        self.create_pages()
        self.create_lines()
        self.create_characters()

    def confirm_book(self):
        """
        Confirm that the book actually exists on Bridges
        """
        if not models.Book.objects.filter(id=self.book_id).exists():
            raise Exception(
                f"The book {self.book_id} is not yet registered in the database. Please confirm you have used the correct UUID."
            )
        self.book = models.Book.objects.get(id=self.book_id)

    def load_json(self):
        self.pages = json.load(open(f"{self.json_directory}/pages.json", "r"))["pages"]
        # Add a "side" to every page
        for page in self.pages:
            page["side"] = "s"
        logging.info(f"{len(self.pages)} pages loaded")
        self.lines = json.load(open(f"{self.json_directory}/lines.json", "r"))["lines"]
        logging.info(f"{len(self.lines)} lines loaded")
        self.characters = json.load(open(f"{self.json_directory}/chars.json", "r"))[
            "chars"
        ]
        # Normalize characters
        for character in self.characters:
            character["character_class"] = self.cc.get_or_create(
                character["character_class"]
            )
        logging.info(f"{len(self.characters)} characters loaded")

    @staticmethod
    def create_pages_for_book(pages_json, book, tif_root):
        # Create page run
        page_run = models.PageRun.objects.create(book=book)
        # Create list of page objects
        page_list = [
            models.Page(
                id=page["id"],
                created_by_run=page_run,
                sequence=page["sequence"],
                side=page["side"],
                tif=page["filename"].replace(tif_root, ""),
            )
            for page in pages_json
        ]
        # Bulk save to DB
        models.Page.objects.bulk_create(
            page_list, batch_size=500, ignore_conflicts=True
        )
        return page_list

    @staticmethod
    def create_lines_for_book(lines_json, book):
        # Create line run
        line_run = models.LineRun.objects.create(book=book)
        page_objects = models.Page.objects.in_bulk(
            list({line["page_id"] for line in lines_json}), field_name="id"
        )
        # Create list of line objects
        line_list = [
            models.Line(
                id=line["id"],
                created_by_run=line_run,
                page=page_objects[UUID(line["page_id"])],
                sequence=line["sequence"],
                y_min=line["y_start"],
                y_max=line["y_end"],
            )
            for line in lines_json
        ]
        # Bulk save to DB
        models.Line.objects.bulk_create(
            line_list, batch_size=500, ignore_conflicts=True
        )
        return line_list

    @staticmethod
    def create_characters_for_book(characters_json, book):
        # Create character run
        character_run = models.CharacterRun.objects.create(book=book)
        # Collect line objects
        line_objects = models.Line.objects.in_bulk(
            list({character["line_id"] for character in characters_json}),
            field_name="id",
        )
        # Collect character class objects
        character_class_objects = models.CharacterClass.objects.in_bulk(
            models.CharacterClass.objects.all().values_list("classname", flat=True),
            field_name="classname",
        )
        # Create list of character objects
        character_list = []
        for i, character in enumerate(characters_json):
            # skip characters that have no `character_class`
            if not character["character_class"]:
                continue
            try:
                cmodel = models.Character(
                    id=character["id"],
                    created_by_run=character_run,
                    line=line_objects[UUID(character["line_id"])],
                    sequence=character["sequence"],
                    y_min=character["y_start"],
                    y_max=character["y_end"],
                    x_min=character["x_start"],
                    x_max=character["x_end"],
                    offset=character["offset"],
                    exposure=character["exposure"],
                    class_probability=character["logprob"],
                    damage_score=character.get("damage_score", None),
                    character_class=character_class_objects[
                        character["character_class"]
                    ],
                )
                character_list.append(cmodel)
            except:
                logging.error(f"Failing char object at index {i}: {character}")
                raise
        worker_size = 20
        chunks = ArrayDivideUtil.divide_into_chunks(character_list, int(round(len(character_list) / worker_size)))
        logging.info({"Total number of characters to be added": len(character_list)})
        logging.info({"Number of chunks for characters": len(chunks)})
        with concurrent.futures.ThreadPoolExecutor(max_workers=worker_size) as executor:
            logging.info("Bulk creating characters using a threadpool executor")

            def db_bulk_create(characters):
                logging.info("Saving characters to the database")
                # Bulk save to DB
                return models.Character.objects.bulk_create(characters, batch_size=500, ignore_conflicts=True)

            result_futures = list(map(lambda characters: executor.submit(db_bulk_create, characters), chunks))
            for future in concurrent.futures.as_completed(result_futures):
                try:
                    logging.info({"Characters chunk created", len(future.result())})
                except Exception as e:
                    logging.error(f'Error in creating character - {str(e)}')
        return character_list

    @transaction.atomic
    def create_pages(self):
        page_list = BookLoader.create_pages_for_book(self.pages, self.book, TIF_ROOT)
        logging.info({"pages created": len(page_list)})

    @transaction.atomic
    def create_lines(self):
        line_list = BookLoader.create_lines_for_book(self.lines, self.book)
        logging.info({"lines created": len(line_list)})

    @transaction.atomic
    def create_characters(self):
        character_list = BookLoader.create_characters_for_book(self.characters, self.book)
        logging.info({"characters created": len(character_list)})
