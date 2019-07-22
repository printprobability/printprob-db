import os
import requests
import re
from glob import glob
from random import randrange

# Enter the database hostname and authorization token
b = os.environ["TEST_HOST"]
ht = {"Authorization": f"Token {os.environ['TEST_TOKEN']}"}

books = glob("/Volumes/data_mdlincoln/pp/books/*")
print(books)

# Start a Run. This POST request will return a UUID that will need to be added when creating new Page, Line, and Character entries in the database
run_id = requests.post(f"{b}runs/", data={"notes": "trial run"}, headers=ht).json()[
    "pk"
]
print(run_id)


def cleanpath(s):
    """
    Make the absolute paths from my local storage into relative paths
    """
    return re.sub("^.+/pp/", "/", s)


for book in books:
    # Segment the book metadata
    bnames = book.split("/")[-1].split("_")
    print(bnames)
    # Create a new book in the database.
    r = requests.post(
        f"{b}books/",
        data={
            "eebo": int(bnames[1]),
            "vid": int(bnames[2]),
            "publisher": bnames[0],
            "title": bnames[4],
        },
        headers=ht,
    ).json()
    print(r)
    # Collect all the spread TIF files from that book's folder
    spread_pix = [f for f in glob(f"{book}/*.tif") if re.search("\d{3}\.tif", f)]
    for s in spread_pix:
        # Segment the spread metadata
        snames = s.split("/")[-1].split("_")[-1].split("-")[-1].split(".")[0]
        print(snames)
        spath = cleanpath(s)

        # From the tiff and jpeg filepaths, create a new Image in the database.
        # The JSON returned from this POST action will contain the UUID of the
        # newly-created image
        image_id = requests.post(
            f"{b}images/",
            data={"tif": spath, "jpg": re.sub("tif", "jpeg", spath)},
            headers=ht,
        ).json()["pk"]
        print(image_id)

        # Create a new Spread in the database, registering which book it comes
        # from, its sequence in the book, and passing the UUID of the image
        # representing it.
        spread_id = requests.post(
            f"{b}spreads/",
            data={
                "book": int(bnames[1]),
                "sequence": int(snames),
                "primary_image": image_id,
            },
            headers=ht,
        ).json()["pk"]
        print(spread_id)

        # For each spread, find the two Page images
        pagepics = [
            p for p in glob(f"{book}/*.tif") if re.search(f"{snames}_page\d\.tif", p)
        ]

        # Since this is just a proof-of-concept, I skipped any possible sets of
        # pages where there may have been more matches than we were set up for
        # right now
        if len(pagepics) < 2:
            continue

        # Get the path of the left page and first save its image paths
        lpath = cleanpath(pagepics[0])
        left_page_pic = requests.post(
            f"{b}images/",
            data={"tif": lpath, "jpg": re.sub("tif", "jpeg", lpath)},
            headers=ht,
        ).json()["pk"]
        # ...and then save the page itself into the db, connected to the spread UUID, the run UUID, and the image UUID
        left_page_id = requests.post(
            f"{b}pages/",
            data={
                "spread": spread_id,
                "side": "l", # Side must be "l" or "r"
                "created_by_run": run_id,
                "x_min": randrange(0, 500),
                "x_max": randrange(0, 500),
                "primary_image": left_page_pic,
            },
            headers=ht,
        ).json()["pk"]

        # Get the path of the right page and first save its image paths
        rpath = cleanpath(pagepics[1])
        right_page_pic = requests.post(
            f"{b}images/",
            data={"tif": rpath, "jpg": re.sub("tif", "jpeg", rpath)},
            headers=ht,
        ).json()["pk"]
        # ...and then create its entry
        right_page_id = requests.post(
            f"{b}pages/",
            data={
                "spread": spread_id,
                "side": "r",
                "created_by_run": run_id,
                "x_min": randrange(0, 500),
                "x_max": randrange(0, 500),
                "primary_image": right_page_pic,
            },
            headers=ht,
        ).json()["pk"]

        # Now iterate through the lines on the left page
        left_lines = [
            p
            for p in glob(f"{book}/*.tif")
            if re.search(f"{snames}_page1r_line\d+.tif", p)
        ]
        for l in left_lines:
            print(l)
            # Create an image for the line first, getting its UUID
            l_image_id = requests.post(
                f"{b}images/",
                data={"tif": cleanpath(l), "jpg": re.sub("tif", "jpeg", cleanpath(l))},
                headers=ht,
            ).json()["pk"]
            lseq = int(re.search(r"(\d+)\.tif", l).groups()[0])

            # and then save the line to the database
            line_id = requests.post(
                f"{b}lines/",
                data={
                    "created_by_run": run_id,
                    "page": left_page_id,
                    "sequence": lseq,
                    "y_min": randrange(0, 500),
                    "y_max": randrange(0, 500),
                    "primary_image": l_image_id,
                },
                headers=ht,
            ).json()["pk"]

        # Now get the lines on the right page, create their images, and save them
        right_lines = [
            p
            for p in glob(f"{book}/*.tif")
            if re.search(f"{snames}_page2r_line\d+.tif", p)
        ]
        for l in right_lines:
            print(l)
            l_image_id = requests.post(
                f"{b}images/",
                data={"tif": cleanpath(l), "jpg": re.sub("tif", "jpeg", cleanpath(l))},
                headers=ht,
            ).json()["pk"]
            lseq = int(re.search(r"(\d+)\.tif", l).groups()[0])
            line_id = requests.post(
                f"{b}lines/",
                data={
                    "created_by_run": run_id,
                    "page": right_page_id,
                    "sequence": lseq,
                    "y_min": randrange(0, 500),
                    "y_max": randrange(0, 500),
                    "primary_image": l_image_id,
                },
                headers=ht,
            ).json()["pk"]
