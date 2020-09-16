from django.db import models
from django.contrib.auth.models import User
from collections import namedtuple
import uuid
from datetime import date
from django.conf import settings
import math


class uuidModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=200, default="", editable=False, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.label = self.labeller()
        super(uuidModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.label


class Run(uuidModel):
    # Use string interpolation of the child class field
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name="%(class)ss"
    )
    date_started = models.DateTimeField(auto_now_add=True)
    script_version = models.CharField(max_length=200, default="", blank=True)

    class Meta:
        abstract = True
        ordering = ["-date_started"]

    def labeller(self):
        return f"{str(self.id)} - {self.date_started}"


class PageRun(Run):
    def component_count(self):
        return self.pages.count()


class LineRun(Run):
    def component_count(self):
        return self.lines.count()


class CharacterRun(Run):
    def component_count(self):
        return self.characters.count()


class Book(uuidModel):
    # Fields that should not be editable when is_eebo_book==TRUE
    EEBO_ONLY = [
        "eebo",
        "vid",
        "tcp",
        "estc",
        "zipfile",
        "zip_path",
        "pq_title",
        "pq_url",
        "pq_author",
        "pq_year_verbatim",
        "pq_year_early",
        "pq_year_late",
        "tx_year_early",
        "tx_year_late",
    ]

    eebo = models.PositiveIntegerField(
        db_index=True, null=True, help_text="EEBO ID number"
    )
    vid = models.PositiveIntegerField(
        db_index=True, null=True, help_text="Proquest ID number"
    )
    tcp = models.CharField(db_index=True, blank=True, help_text="TCP ID", max_length=50)
    estc = models.CharField(
        db_index=True,
        blank=True,
        help_text="English Short Title Catalogue Number",
        max_length=50,
    )
    pq_title = models.CharField(
        max_length=2000, db_index=True, help_text="Title (as cataloged by EEBO)"
    )
    pq_publisher = models.CharField(
        blank=True,
        max_length=2000,
        help_text="Publisher (as cataloged by EEBO)",
        editable=False,
    )
    pq_author = models.CharField(
        blank=True,
        max_length=2000,
        help_text="Author (as cataloged by EEBO)",
        editable=False,
    )
    pq_year_verbatim = models.CharField(
        max_length=2000,
        blank=True,
        help_text="Date string from EEBO, may contain non-numeric values",
        editable=False,
    )
    pq_year_early = models.PositiveIntegerField(
        db_index=True, null=True, help_text="Proquest early year", editable=False
    )
    pq_year_late = models.PositiveIntegerField(
        db_index=True, null=True, help_text="Proquest late year", editable=False
    )
    tx_year_early = models.PositiveIntegerField(
        db_index=True, null=True, help_text="Texas A&M early year", editable=False
    )
    tx_year_late = models.PositiveIntegerField(
        db_index=True, null=True, help_text="Texas A&M late year", editable=False
    )
    pq_url = models.URLField(
        max_length=1000, blank=True, help_text="ProQuest URL", editable=False
    )
    pp_publisher = models.CharField(
        blank=True, max_length=2000, help_text="Publisher as asserted by P&P team"
    )
    pdf = models.CharField(
        blank=True,
        max_length=1500,
        help_text="relative file path to root directory containing pdfs",
    )
    date_early = models.DateField(
        default=date(year=1550, month=1, day=1), db_index=True
    )
    date_late = models.DateField(
        default=date(year=1800, month=12, day=12), db_index=True
    )
    zipfile = models.CharField(max_length=1000, blank=True, null=False)
    starred = models.BooleanField(default=False, db_index=True)
    ignored = models.BooleanField(default=False, db_index=True)
    is_eebo_book = models.BooleanField(default=False, db_index=True)
    prefix = models.CharField(max_length=200, blank=True, null=True, unique=True)
    n_spreads = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["pq_title"]

    def labeller(self):
        return f"({self.vid}) {self.pq_title[:30]}..."

    def all_runs(self):
        return {
            "pages": self.pageruns.all(),
            "lines": self.lineruns.all(),
            "characters": self.characterruns.all(),
        }

    def most_recent_runs(self):
        return {
            "page": self.pageruns.first(),
            "line": self.lineruns.first(),
            "character": self.characterruns.first(),
        }

    def most_recent_pages(self):
        """
        Get all pages for this book based on the most recent run in the database
        """
        return self.pageruns.first().pages.all()

    def cover_spread(self):
        return self.spreads.first()

    @property
    def zip_path(self):
        return f"{self.zipfile}/{self.vid}/*.tif"


class Task(uuidModel):
    date_entered = models.DateTimeField(
        auto_now=True, help_text="Date this classification was made"
    )

    class Meta:
        abstract = True
        ordering = ["date_entered"]

    def labeller(self):
        return f"{date_entered}"

        return self.id


class ImagedModel(uuidModel):
    tif = models.CharField(
        max_length=2000,
        help_text="relative file path to root directory containing all images",
        blank=True,
    )

    @property
    def iiif_base(self):
        return f"{settings.IMAGE_BASEURL}{self.tif}"

    @property
    def web_url(self):
        return f"{self.iiif_base}/full/full/0/default.jpg"

    @property
    def thumbnail(self):
        return f"{self.iiif_base}/full/500,/0/default.jpg"

    @property
    def full_tif(self):
        return f"{self.iiif_base}/full/full/0/default.tif"

    @property
    def image(self):
        return {
            "tif": self.tif,
            "iiif_base": self.iiif_base,
            "web_url": self.web_url,
            "thumbnail": self.thumbnail,
            "full_tif": self.full_tif,
        }

    class Meta:
        abstract = True


class CroppedModel(uuidModel):
    @property
    def region_string(self):
        ac = self.absolute_coords
        return f"{ac['x']},{ac['y']},{ac['w']},{ac['h']}"

    @property
    def buffer(self):
        ac = self.absolute_coords
        buffer = 50
        return f"{self.root_object.iiif_base}/{max(ac['x'] - buffer, 0)},{max(ac['y'] - buffer, 0)},{ac['w'] + (2 * buffer)},{ac['h'] + (2 * buffer)}/150,/0/default.jpg"

    @property
    def web_url(self):
        return f"{self.root_object.iiif_base}/{self.region_string}/full/0/default.jpg"

    @property
    def full_tif(self):
        return f"{self.root_object.iiif_base}/{self.region_string}/full/0/default.tif"

    @property
    def thumbnail(self):
        return f"{self.root_object.iiif_base}/{self.region_string}/500,/0/default.jpg"

    @property
    def image(self):
        return {
            "web_url": self.web_url,
            "thumbnail": self.thumbnail,
            "buffer": self.buffer,
        }

    class Meta:
        abstract = True


class Spread(ImagedModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="spreads",
        help_text="Book to which this spread belongs",
    )
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Sequence of this page in a given book"
    )

    class Meta:
        unique_together = (("book", "sequence"),)
        ordering = ("book", "sequence")

    def labeller(self):
        return f"{self.book} spread {self.sequence}"

    def most_recent_pages(self):
        return self.book.pageruns.first().pages.filter(spread=self)

    def save(self, *args, **kwargs):
        """
        Update book spread count on save
        """
        response = super().save(*args, **kwargs)
        self.book.n_spreads = self.book.spreads.count()
        self.book.save()
        return response


class Page(ImagedModel):
    """
    The definition of a page may change between runs in this model, since it depends on splitting spreads, therefore it is a subclass of an Attempt.
    """

    SPREAD_SIDE = (("s", "single"), ("l", "left"), ("r", "right"))
    sequence = models.PositiveIntegerField(default=0)
    side = models.CharField(
        max_length=1,
        choices=SPREAD_SIDE,
        help_text="Side of the spread this has been segmented to",
    )
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    w = models.FloatField(null=True)
    h = models.FloatField(null=True)
    rot1 = models.FloatField(null=True)
    rot2 = models.FloatField(null=True)
    created_by_run = models.ForeignKey(
        PageRun,
        on_delete=models.CASCADE,
        help_text="Which pipeline run created this object instance",
        related_name="pages",
    )

    class Meta:
        unique_together = (("created_by_run", "sequence"),)
        ordering = ["created_by_run", "sequence"]

    def labeller(self):
        return f"{self.created_by_run.book} p. {self.sequence}-{self.side}"

    def n_lines(self):
        return self.lines.count()

    def most_recent_lines(self):
        return self.created_by_run.book.lineruns.first().lines.filter(page=self)

    def book(self):
        return self.created_by_run.book


class Line(CroppedModel):
    """
    The definition of a line may change between runs in this model, since it depends on splitting page spreads, therefore it is a subclass of an Attempt.
    """

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="lines",
        help_text="Page ID of this line",
    )
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Order on page, from top to bottom"
    )
    y_min = models.PositiveIntegerField(
        help_text="Y-axis index for the start of this line on the Page image"
    )
    y_max = models.PositiveIntegerField(
        help_text="Y-axis index for the end of this line on the Page image"
    )
    created_by_run = models.ForeignKey(
        LineRun,
        on_delete=models.CASCADE,
        help_text="Which pipeline run created this object instance",
        related_name="lines",
    )

    class Meta:
        unique_together = (("created_by_run", "page", "sequence"),)
        ordering = ["created_by_run", "page", "sequence"]

    def labeller(self):
        return f"{self.page} l. {self.sequence}"

    def n_chars(self):
        return self.characters.count()

    def most_recent_characters(self):
        return self.page.created_by_run.book.characterruns.first().characters.filter(
            line=self
        )

    @property
    def root_object(self):
        return self.page

    @property
    def absolute_coords(self):
        x = 0
        y = self.y_min
        w = 9999
        h = self.height
        return {"x": x, "y": y, "w": w, "h": h}

    @property
    def height(self):
        return self.y_max - self.y_min

    def page_side(self):
        return self.page.side


class CharacterClass(models.Model):
    LOWERCASE = "cl"
    UPPERCASE = "cu"
    NUMBER = "nu"
    PUNCTUATION = "pu"
    CHARACTER_GROUPS = [
        (LOWERCASE, "Lowercase"),
        (UPPERCASE, "Uppercase"),
        (NUMBER, "Number"),
        (PUNCTUATION, "Punctuation"),
    ]

    classname = models.CharField(
        primary_key=True,
        max_length=50,
        help_text="A human-readable, unique class identifier",
    )
    group = models.CharField(
        max_length=2, choices=CHARACTER_GROUPS, default=LOWERCASE, db_index=True
    )

    class Meta:
        ordering = ["group", "classname"]

    def __str__(self):
        return self.classname

    def label(self):
        return str(self)


class Character(CroppedModel):
    """
    The definition of a character may change between runs in this model, since it depends on line segmentation, therefore it is a subclass of an Attempt.
    """

    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name="characters")
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Sequence of characters on the line"
    )
    x_min = models.PositiveIntegerField(
        help_text="X-axis index for the start of this character on the line image"
    )
    x_max = models.PositiveIntegerField(
        help_text="X-axis index for the end of this character on the line image"
    )
    character_class = models.ForeignKey(
        CharacterClass, on_delete=models.CASCADE, related_name="assigned_to"
    )
    human_character_class = models.ForeignKey(
        CharacterClass,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="human_assigned_to",
    )
    class_probability = models.FloatField(db_index=True)
    created_by_run = models.ForeignKey(
        CharacterRun,
        on_delete=models.CASCADE,
        help_text="Which pipeline run created this object instance",
        related_name="characters",
    )
    exposure = models.IntegerField(default=0)
    offset = models.IntegerField(default=0)

    class Meta:
        unique_together = (("created_by_run", "line", "sequence"),)
        ordering = ["created_by_run", "line", "sequence"]

    def labeller(self):
        return f"{self.line} c. {self.sequence}"

    def book(self):
        return self.line.page.created_by_run.book

    def page(self):
        return self.line.page

    @property
    def width(self):
        return self.x_max - self.x_min

    @property
    def absolute_coords(self):
        multiplier = self.line.height / 30
        x = math.floor(self.x_min * multiplier)
        y = max(math.floor(self.line.y_min - self.offset * multiplier), 0)
        w = math.floor(self.width * multiplier)
        h = self.line.height
        return {"x": x, "y": y, "w": w, "h": h}

    @property
    def root_object(self):
        return self.line.page


# User-based models
class UserBasedModel(uuidModel):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)ss"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["created_by", "-date_created"]


class CharacterGrouping(UserBasedModel):
    label = models.CharField(
        max_length=200,
        help_text="A descriptive label (will appear in menus etc)",
        unique=True,
    )
    notes = models.TextField(
        max_length=10000,
        blank=True,
        null=False,
        help_text="A description or notes about the grouping",
    )
    characters = models.ManyToManyField(
        Character, related_name="charactergroupings", blank=True
    )

    def labeller(self):
        return self.label
