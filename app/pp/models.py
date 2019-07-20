from django.db import models
from collections import namedtuple
import uuid


class uuidModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


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

    def __str__(self):
        return f"{str(self.id)}-{self.date_started}"


class PageRun(Run):
    params = models.CharField(max_length=1000)


class LineRun(Run):
    params = models.CharField(max_length=1000)


class LineGroupRun(Run):
    params = models.CharField(max_length=1000)


class CharacterRun(Run):
    params = models.CharField(max_length=1000)


class Book(models.Model):
    estc = models.PositiveIntegerField(primary_key=True, help_text="ESTC ID number")
    vid = models.PositiveIntegerField(unique=True, help_text="Alternate ID number")
    title = models.CharField(
        max_length=1000, db_index=True, help_text="Title (as cataloged by ESTC)"
    )
    publisher = models.CharField(
        blank=True,
        null=False,
        max_length=500,
        help_text="Publisher (as cataloged by ESTC)",
    )
    pdf = models.CharField(
        max_length=2000,
        help_text="relative file path to root directory containing pdfs",
        unique=True,
    )

    class Meta:
        ordering = ["estc"]

    def __str__(self):
        return f"{self.estc} - {self.title}"

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

    def __str__(self):
        return str(self.id)

    def web_url(self):
        return f"/img{self.jpg}"


class Spread(uuidModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="spreads",
        help_text="Book to which this spread belongs",
    )
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Sequence of this page in a given book"
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="depicts_spread",
        help_text="Image depicting this spread",
    )

    class Meta:
        unique_together = (("book", "sequence"),)

    def __str__(self):
        return f"{self.book.title} spread {self.sequence}"

    def pref_image_url(self):
        if self.image is not None:
            return self.image.web_url()
        else:
            return None

    def most_recent_pages(self):
        return self.book.pageruns.first().pages.filter(spread=self)


class Page(uuidModel):
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
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="depicts_page"
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

    def __str__(self):
        return f"{self.spread.book.title} p. {self.spread.sequence}-{self.side}"

    def n_lines(self):
        return self.lines.count()

    def pref_image_url(self):
        if self.image is not None:
            return self.image.web_url()
        else:
            return None

    def most_recent_lines(self):
        return self.spread.book.lineruns.first().lines.filter(page=self)

    def spread_sequence(self):
        return self.spread.sequence


class Line(uuidModel):
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
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="depicts_line"
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

    def __str__(self):
        return f"{self.page} l. {self.sequence}"

    def n_chars(self):
        return self.characters.count()

    def pref_image_url(self):
        if self.image is not None:
            return self.image.web_url()
        else:
            return None

    def most_recent_characters(self):
        return self.page.spread.book.characterruns.first().characters.filter(line=self)

    def most_recent_linegroups(self):
        return self.page.spread.book.linegroupruns.first().linegroups.filter(lines=self)

    def line_height(self):
        return self.y_max - self.y_min

    def absolute_coords(self):
        """
        Return a bounding box based on the pixels in the original page image
        """
        bbox = namedtuple("BoundingBox", "xmin xmax ymin ymax")
        xmin = self.page.x_min
        xmax = self.page.x_max
        ymin = self.y_min
        ymax = self.y_max
        return bbox(xmin, xmax, ymin, ymax)


class LineGroup(uuidModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="linegroups")
    lines = models.ManyToManyField(Line, related_name="linegroups")
    created_by_run = models.ForeignKey(
        LineGroupRun, on_delete=models.CASCADE, related_name="linegroups"
    )


class CharacterClass(models.Model):
    classname = models.CharField(
        primary_key=True,
        max_length=50,
        help_text="A human-readable, unique class identifier",
    )

    def __str__(self):
        return self.classname


class Character(uuidModel):
    """
    The definition of a character may change between runs in this model, since it depends on line segmentation, therefore it is a subclass of an Attempt.
    """

    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name="characters")
    image = models.ForeignKey(
        Image, related_name="depicts_character", on_delete=models.CASCADE
    )
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

    def __str__(self):
        return f"{self.line} c. {self.sequence} ({self.character_class} - {self.class_probability})"

    def pref_image_url(self):
        if self.image is not None:
            return self.image.web_url()
        else:
            return None

    def absolute_coords(self):
        """
        Return a bounding box based on the pixels in the original page image. This doesn't yet take rotation into account :( Might need to make that the responsibility of the app
        """
        bbox = namedtuple("BoundingBox", "xmin xmax ymin ymax")
        xmin = self.line.page.x_min + self.x_min
        xmax = self.line.page.x_min + self.x_max
        ymin = self.line.y_min
        ymax = self.line.y_max
        return bbox(xmin, xmax, ymin, ymax)

