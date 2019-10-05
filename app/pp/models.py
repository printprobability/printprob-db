from django.db import models
from django.contrib.auth.models import User
from collections import namedtuple
import uuid
from datetime import date
from django.conf import settings


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
    script_path = models.CharField(
        max_length=2000, help_text="Filepath of the script governing this run"
    )
    script_md5 = models.UUIDField(help_text="md5 hash of the script (as hex digest)")
    date_started = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-date_started"]

    def labeller(self):
        return f"{str(self.id)} - {self.date_started}"


class PageRun(Run):
    params = models.CharField(max_length=1000)


class LineRun(Run):
    params = models.CharField(max_length=1000)


class LineGroupRun(Run):
    params = models.CharField(max_length=1000)


class CharacterRun(Run):
    params = models.CharField(max_length=1000)


class Book(uuidModel):
    eebo = models.PositiveIntegerField(
        db_index=True, null=True, help_text="EEBO ID number", editable=False
    )
    vid = models.PositiveIntegerField(
        db_index=True, null=True, help_text="Proquest ID number", editable=False
    )
    pq_title = models.CharField(
        max_length=2000,
        db_index=True,
        help_text="Title (as cataloged by EEBO)",
        editable=False,
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
    pq_url = models.URLField(
        max_length=1000, blank=True, help_text="ProQuest URL", editable=False
    )
    publisher = models.CharField(
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

    class Meta:
        ordering = ["pq_title"]

    def labeller(self):
        return f"({self.vid}) {self.pq_title[:30]}..."

    def all_runs(self):
        return {
            "pages": self.pageruns.all(),
            "lines": self.lineruns.all(),
            "linegroups": self.linegroupruns.all(),
            "characters": self.characterruns.all(),
        }

    def most_recent_runs(self):
        return {
            "page": self.pageruns.first(),
            "line": self.lineruns.first(),
            "linegroup": self.linegroupruns.first(),
            "character": self.characterruns.first(),
        }

    def most_recent_pages(self):
        """
        Get all pages for this book based on the most recent run in the database
        """
        return self.pageruns.first().pages.all()

    def cover_spread(self):
        return self.spreads.first()

    def cover_page(self):
        return self.most_recent_pages().first()

    def n_spreads(self):
        return self.spreads.count()

    def n_pages(self):
        return ordered_pages.count()


class Task(uuidModel):
    date_entered = models.DateTimeField(
        auto_now=True, help_text="Date this classification was made"
    )

    class Meta:
        abstract = True
        ordering = ["date_entered"]

    def labeller(self):
        return f"{date_entered}"


class Image(uuidModel):
    jpg = models.CharField(
        max_length=2000,
        help_text="relative file path to root directory containing all images",
        unique=True,
    )
    tif = models.CharField(
        max_length=2000,
        help_text="relative file path to root directory containing all images",
        unique=True,
    )
    jpg_md5 = models.UUIDField(help_text="md5 hash of the jpg file (as hex digest)")
    tif_md5 = models.UUIDField(help_text="md5 hash of the tif file (as hex digest)")

    def labeller(self):
        return self.jpg

    def web_url(self):
        return f"{settings.IMAGE_BASEURL}{self.jpg}"


class ImagedModel(uuidModel):

    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="%(class)ss"
    )

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


class Page(ImagedModel):
    """
    The definition of a page may change between runs in this model, since it depends on splitting spreads, therefore it is a subclass of an Attempt.
    """

    SPREAD_SIDE = (("s", "single"), ("l", "left"), ("r", "right"))
    spread = models.ForeignKey(
        Spread,
        on_delete=models.CASCADE,
        related_name="pages",
        help_text="Spread ID this page belongs to",
    )
    side = models.CharField(
        max_length=1,
        choices=SPREAD_SIDE,
        help_text="Side of the spread this has been segmented to",
    )
    x_min = models.PositiveIntegerField(
        help_text="Starting x-axis location of the page on the original spread image"
    )
    x_max = models.PositiveIntegerField(
        help_text="Ending x-axis location of the page on the original spread image"
    )
    created_by_run = models.ForeignKey(
        PageRun,
        on_delete=models.CASCADE,
        help_text="Which pipeline run created this object instance",
        related_name="pages",
    )

    class Meta:
        unique_together = (("created_by_run", "spread", "side"),)
        ordering = ["created_by_run", "spread", "side"]

    def labeller(self):
        return f"{self.spread.book} p. {self.spread.sequence}-{self.side}"

    def n_lines(self):
        return self.lines.count()

    def most_recent_lines(self):
        return self.spread.book.lineruns.first().lines.filter(page=self)

    def spread_sequence(self):
        return self.spread.sequence

    def book(self):
        return self.spread.book


class Line(ImagedModel):
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
        return self.page.spread.book.characterruns.first().characters.filter(line=self)

    def most_recent_linegroups(self):
        return LineGroup.objects.filter(
            lines=self, created_by_run=self.page.spread.book.linegroupruns.first()
        ).distinct()

    def line_height(self):
        return self.y_max - self.y_min

    def page_side(self):
        return self.page.side


class LineGroup(uuidModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="linegroups")
    lines = models.ManyToManyField(Line, related_name="linegroups")
    created_by_run = models.ForeignKey(
        LineGroupRun, on_delete=models.CASCADE, related_name="linegroups"
    )

    def labeller(self):
        return f"{self.page} grouping"


class CharacterClass(models.Model):
    classname = models.CharField(
        primary_key=True,
        max_length=50,
        help_text="A human-readable, unique class identifier",
    )

    class Meta:
        ordering = ["classname"]

    def __str__(self):
        return self.classname

    def label(self):
        return str(self)


class Character(ImagedModel):
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
    class_probability = models.FloatField()
    created_by_run = models.ForeignKey(
        CharacterRun,
        on_delete=models.CASCADE,
        help_text="Which pipeline run created this object instance",
        related_name="characters",
    )

    class Meta:
        unique_together = (("created_by_run", "line", "sequence"),)
        ordering = ["created_by_run", "line", "sequence"]

    def labeller(self):
        return f"{self.line} c. {self.sequence}"

    def book(self):
        return self.line.page.spread.book

    def spread(self):
        return self.line.page.spread

    def page(self):
        return self.line.page

    def absolute_coords(self):
        bbox = {}
        xmin = self.line.page.x_min + self.x_min
        xmax = self.line.page.x_min + self.x_max
        ymin = self.line.y_min
        ymax = self.line.y_max
        return [
            {"x": xmin, "y": ymin},
            {"x": xmax, "y": ymin},
            {"x": xmax, "y": ymax},
            {"x": xmin, "y": ymax},
        ]


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
