from django.db import models
from collections import namedtuple
import uuid


class Run(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_started = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(
        blank=True,
        null=False,
        default="",
        max_length=5000,
        help_text="Free-text notes describing the nature of this run",
    )

    class Meta:
        ordering = ["date_started"]

    def __str__(self):
        return f"{self.pk}-{self.date_started}"

    @staticmethod
    def most_recent_run():
        return Run.objects.order_by("-date_started").first()

    def pages_created(self):
        return Page.objects.filter(created_by_run=self).all()

    def lines_created(self):
        return Line.objects.filter(created_by_run=self).all()

    def characters_created(self):
        return Character.objects.filter(created_by_run=self).all()


class Attempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by_run = models.ForeignKey(
        Run,
        on_delete=models.CASCADE,
        help_text="Which pipeline run created this object instance",
    )

    class Meta:
        abstract = True


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_entered = models.DateTimeField(
        auto_now=True, help_text="Date this classification was made"
    )

    class Meta:
        abstract = True
        ordering = ["date_entered"]


class BadCapture(Task):
    image = models.OneToOneField(
        "Image",
        related_name="good_capture",
        on_delete=models.CASCADE,
        help_text="The image being classified as a poor segmentation",
    )


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(
        blank=True,
        null=False,
        max_length=500,
        help_text="Standard identifier using the printer/id/location schema, without any filetype name",
    )
    web_file = models.OneToOneField(
        "ImageFile",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={"filetype": "jpg"},
        help_text="direct pointer to the path of the JPG version of this image, if it exists",
    )

    def __str__(self):
        return id

    def web_url(self):
        if self.web_file is not None:
            return f"/img/{self.web_file.filepath}"
        else:
            return None

    def bad_capture(self):
        return BadCapture.objects.filter(image=self).exists()


class ImageFile(models.Model):
    TYPES = (("png", "png"), ("jpg", "jpeg"), ("tif", "tiff"), ("pdf", "pdf"))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="files",
        help_text="The image of which this file is one type",
    )
    filetype = models.CharField(
        max_length=3, choices=TYPES, help_text="File encoding (e.g. png, jpg, tif...)"
    )
    date_uploaded = models.DateTimeField(
        auto_now_add=True, help_text="Date this file was added to the server"
    )
    filepath = models.CharField(
        max_length=2000,
        help_text="relative file path to root directory containing all images",
        unique=True,
    )

    class Meta:
        unique_together = (("parent_image", "filetype"),)
        ordering = ["image", "date_uploaded"]

    def __str__(self):
        return str(self.id)


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
    pdf = models.ForeignKey(
        ImageFile,
        blank=True,
        null=True,
        limit_choices_to={"filetype": "pdf"},
        related_name="book_depicted",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["estc"]

    def __str__(self):
        return self.title

    def ordered_pages_run(self, run):
        """
        Get all pages for this book based on a given run
        """
        return models.Page.objects.filter(spread__book=self, created_by_run=run)

    def ordered_pages(self):
        """
        Get all pages for this book based on the most recent run in the database
        """
        return ordered_pages_run(self, Run.most_recent_run())

    def cover_page(self):
        return self.pages.first()

    def n_spreads(self):
        return self.spreads.count()

    def n_pages(self):
        return ordered_pages.count()


class ProposedBookLineHeight(Attempt):
    """
    Book line heights are proposed per-run
    """

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="proposed_line_heights"
    )
    line_height = models.PositiveIntegerField(
        help_text="Proposed line height for a book"
    )

    class Meta:
        unique_together = (("book", "created_by_run"),)


class Spread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="spreads")
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Sequence of this page in a given book"
    )
    images = models.ManyToManyField(Image, blank=True, related_name="depicted_spreads")

    class Meta:
        unique_together = (("book", "sequence"),)

    def __str__(self):
        return f"{self.book.title} s. {self.sequence}"


class Page(Attempt):
    """
    The definition of a page may change between runs in this model, since it depends on splitting spreads, therefore it is a subclass of an Attempt.
    """

    SPREAD_SIDE = (("l", "left"), ("r", "right"))
    spread = models.ForeignKey(Spread, on_delete=models.CASCADE, related_name="pages")
    side = models.CharField(
        max_length=1,
        choices=SPREAD_SIDE,
        help_text="Side of the spread this has been segmented to",
    )
    images = models.ManyToManyField(Image, blank=True, related_name="depicted_pages")
    x_min = models.PositiveIntegerField(
        help_text="Starting x-axis location of the page on the original spread image"
    )
    x_max = models.PositiveIntegerField(
        help_text="Ending x-axis location of the page on the original spread image"
    )

    class Meta:
        unique_together = (("created_by_run", "spread", "side"),)
        ordering = ["created_by_run", "spread", "side"]

    def __str__(self):
        return f"{self.spread.book.title} p. {self.spread.sequence}{self.side}"

    def n_lines(self):
        return self.lines.count()

    def pref_image(self):
        return self.images.first()

    def book_title(self):
        return self.book.title


class Line(Attempt):
    """
    The definition of a line may change between runs in this model, since it depends on splitting page spreads, therefore it is a subclass of an Attempt.
    """

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="lines")
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Order on page, from top to bottom"
    )
    images = models.ManyToManyField(Image, blank=True)
    y_min = models.PositiveIntegerField(
        help_text="Y-axis index for the start of this line on the Page image"
    )
    y_max = models.PositiveIntegerField(
        help_text="Y-axis index for the end of this line on the Page image"
    )

    class Meta:
        unique_together = (("created_by_run", "page", "sequence"),)
        ordering = ["created_by_run", "page", "sequence"]

    def __str__(self):
        return f"{self.page} l. {self.sequence}"

    def n_chars(self):
        return self.characters.count()

    def n_images(self):
        return self.images.count()

    def pref_image(self):
        return self.images.first()

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


class Character(Attempt):
    """
    The definition of a character may change between runs in this model, since it depends on line segmentation, therefore it is a subclass of an Attempt.
    """

    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name="characters")
    images = models.ManyToManyField(Image, related_name="characters", blank=True)
    sequence = models.PositiveIntegerField(
        db_index=True, help_text="Sequence of characters on the line"
    )
    x_min = models.PositiveIntegerField(
        help_text="X-axis index for the start of this character on the line image"
    )
    x_max = models.PositiveIntegerField(
        help_text="X-axis index for the end of this character on the line image"
    )

    class Meta:
        unique_together = (("created_by_run", "line", "sequence"),)
        ordering = ["created_by_run", "line", "sequence"]

    def __str__(self):
        return f"{self.line} c. {self.sequence}"

    def pref_image(self):
        return self.images.first()

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


class CharacterClass(models.Model):
    classname = models.CharField(
        primary_key=True,
        max_length=50,
        editable=False,
        help_text="A human-readable, unique class identifier",
    )

    def __str__(self):
        return self.classname


class ClassAssignment(Attempt):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="class_assignments"
    )
    character_class = models.ForeignKey(
        CharacterClass, on_delete=models.CASCADE, related_name="class_assignments"
    )
    log_probability = models.FloatField()

    class Meta:
        unique_together = ("created_by_run", "character", "character_class")
        ordering = ["created_by_run__date_started", "character", "-log_probability"]

    def _str__(self):
        return f"run {created_by_run}: chr {character} - {character_class} {log_probability}"
