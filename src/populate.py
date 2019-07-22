from pp import models
from uuid import uuid4
from faker import Faker
import random

ff = Faker()
models.Book.objects.all().delete()
models.Image.objects.all().delete()


b1 = models.Book.objects.create(
    eebo=1234,
    vid=231,
    title=ff.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
    pdf=ff.file_path(depth=3, extension="pdf"),
)
b2 = models.Book.objects.create(
    eebo=5678,
    vid=987,
    title=ff.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
    pdf=ff.file_path(depth=3, extension="pdf"),
)
books = [b1, b2]


def quickimage():
    return models.Image.objects.create(
        jpg=ff.file_path(depth=3, extension="jpg"),
        tif=ff.file_path(depth=3, extension="tif"),
        jpg_md5=uuid4(),
        tif_md5=uuid4(),
    )


for book in books:
    for i in range(0, 2):
        models.Spread.objects.create(book=book, sequence=i, image=quickimage())

for book in books:
    page_run = models.PageRun.objects.create(
        book=book,
        params=ff.license_plate(),
        script_path=ff.file_path(depth=3, extension="py"),
        script_md5=uuid4(),
    )
    for spread in book.spreads.all():
        for s in ["l", "r"]:
            models.Page.objects.create(
                spread=spread,
                created_by_run=page_run,
                side=s,
                image=quickimage(),
                x_min=random.randrange(0, 500),
                x_max=random.randrange(0, 500),
            )

for book in books:
    line_run = models.LineRun.objects.create(
        book=book,
        params=ff.license_plate(),
        script_path=ff.file_path(depth=3, extension="py"),
        script_md5=uuid4(),
    )
    for page in models.Page.objects.filter(spread__book=book).all():
        for i in range(0, 3):
            models.Line.objects.create(
                page=page,
                created_by_run=line_run,
                image=quickimage(),
                sequence=i,
                y_min=random.randrange(0, 500),
                y_max=random.randrange(0, 500),
            )

for book in books:
    linegroup_run = models.LineGroupRun.objects.create(
        book=book,
        params=ff.license_plate(),
        script_path=ff.file_path(depth=3, extension="py"),
        script_md5=uuid4(),
    )
    for page in models.Page.objects.filter(spread__book=book).all():
        for i in range(0, 2):
            lg = models.LineGroup.objects.create(
                page=page, created_by_run=linegroup_run
            )
            for line in models.Line.objects.filter(page=page).order_by("?")[:1]:
                lg.lines.add(line)

for cc in ["a", "b", "c"]:
    models.CharacterClass.objects.get_or_create(classname=cc)

for book in books:
    character_run = models.CharacterRun.objects.create(
        book=book,
        params=ff.license_plate(),
        script_path=ff.file_path(depth=3, extension="py"),
        script_md5=uuid4(),
    )
    for line in models.Line.objects.filter(page__spread__book=book).all():
        for i in range(0, 2):
            randclass = models.CharacterClass.objects.order_by("?")[0]
            models.Character.objects.create(
                line=line,
                created_by_run=character_run,
                image=quickimage(),
                sequence=i,
                x_min=random.randrange(0, 500),
                x_max=random.randrange(0, 500),
                character_class=randclass,
                class_probability=random.random(),
            )

book = books[0]
new_character_run = models.CharacterRun.objects.create(
    book=book,
    params=ff.license_plate(),
    script_path=ff.file_path(depth=3, extension="py"),
    script_md5=uuid4(),
)
for line in models.Line.objects.filter(page__spread__book=book).all():
    for i in range(0, 2):
        randclass = models.CharacterClass.objects.order_by("?")[0]
        models.Character.objects.create(
            line=line,
            created_by_run=character_run,
            image=quickimage(),
            sequence=i,
            x_min=random.randrange(0, 500),
            x_max=random.randrange(0, 500),
            character_class=randclass,
            class_probability=random.random(),
        )
