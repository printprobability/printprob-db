import os
import requests
import re
from glob import glob
from random import random, randrange
from uuid import uuid4, UUID
from hashlib import md5

# Enter the database hostname and authorization token
b = os.environ["TEST_HOST"]
ht = {"Authorization": f"Token {os.environ['TEST_TOKEN']}"}

books = glob("/Volumes/data_mdlincoln/pp/chars/*")
print(books)


def cleanpath(s):
    """
    Make the absolute paths from my local storage into relative paths
    """
    return re.sub("^.+/chars/", "/chars/", s)


# post character classes
char_classes = []
for book in books:
    allchars = glob(f"{book}/**/*.tif", recursive=True)
    for char in allchars:
        char_class = re.search(r"([A-Z]_[a-z]{2})\.tif", char).groups()[0]
        char_classes.append(char_class)

for cc in set(char_classes):
    # Make sure that the character class has been registered in the database. Right now this just takes a string as a primary key, and doesn't use the UUID pattern that we need for classes where there are going to be thousands or millions of instances
    requests.post(f"{b}character_classes/", data={"classname": cc}, headers=ht).json()

for book in books:

    book_eebo = book.split("/")[3].split("_")[1]

    book_id = requests.get(f"{b}books/", params={"eebo": book_eebo}, headers=ht).json()[
        "results"
    ][0]["id"]

    char_run = requests.post(
        f"{b}runs/characters/",
        data={
            "params": str(uuid4()),
            "script_path": str(uuid4()),
            "script_md5": uuid4(),
            "book": book_id,
        },
        headers=ht,
    ).json()["id"]

    # Get all the character images from a given book
    allchars = glob(f"{book}/**/*.tif", recursive=True)
    for char in allchars:
        print(char)
        # Get the sequence of the spread in that book
        spread_seq = int(re.search(r"-(\d{3})_", char).groups()[0])

        # Get the side of the page in that spread
        page_no = re.search(r"page(\d)", char).groups()[0]
        if page_no == "1":
            page_side = "l"
        else:
            page_side = "r"

        # Get the sequence of the line in that page
        line_seq = int(re.search(r"line(\d+)_", char).groups()[0])

        # Get the sequence of the character in that line
        char_seq = int(re.search(r"_char(\d+)_", char).groups()[0])

        # Finally, collect the character class
        char_class = re.search(r"([A-Z]_[a-z]{2})\.tif", char).groups()[0]

        # We need to get the UUID of the line that we're conencting this
        # character to. We do this by calling GET on the lines/ endpoint, and
        # using URL query parameters to pass the book id, spread sequence, page
        # side, and line sequence. With those 4 parameters we should get a
        # single unique line entry (N.B. this actually also needs a unique RUN
        # id parameter once we're working with multiple runs...). This will
        # send a GET request formatted like http://printprobdb.library.cmu.edu/lines/?book=99860883&spread_sequence=2&page_side=l&sequence=1&created_by_run=
        line_id = requests.get(
            f"{b}lines/",
            params={
                "book_id": book_id,
                "spread_sequence": spread_seq,
                "page_side": page_side,
                "sequence": line_seq,
            },
            headers=ht,
        ).json()["results"][0]["id"]

        charpath = cleanpath(char)

        # For some reason I was occasionally getting errors that some of the filepaths I was putting in had already been registered in the database, thus causing the endpoint to throw a unique constraint error. If this happens, we just GET the image UUID, passing in the filepath as a URL query parameter
        try:
            char_image = requests.post(
                f"{b}images/",
                data={
                    "tif": charpath,
                    "jpg": re.sub("tif", "jpg", charpath),
                    "jpg_md5": md5(open(char, "rb").read()).hexdigest(),
                    "tif_md5": md5(open(char, "rb").read()).hexdigest(),
                },
                headers=ht,
            ).json()["id"]
        except:
            char_image = requests.get(
                f"{b}images/", params={"filepath": charpath}, headers=ht
            ).json()["results"][0]["id"]

        # Finally, create the character in the database, passing in the run UUID, line UUID that we retrieved, the image UUID, the character class name, and its sequence on the line
        char_id = requests.post(
            f"{b}characters/",
            data={
                "created_by_run": char_run,
                "line": line_id,
                "sequence": char_seq,
                "character_class": char_class,
                "class_probability": random(),
                "x_min": randrange(0, 500),
                "x_max": randrange(0, 500),
                "image": char_image,
            },
            headers=ht,
        )
        print(char_id.json()["id"])
