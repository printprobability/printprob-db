import os
import requests
import re
from glob import glob
from uuid import UUID

b = os.environ["TEST_HOST"]
ht = {"Authorization": f"Token {os.environ['TEST_TOKEN']}"}

books = glob("/Volumes/data_mdlincoln/pp/chars/*")
print(books)

# Get last run
run_id = requests.get(f"{b}runs/", headers=ht).json()["results"][0]["pk"]
print(run_id)

for book in books:
    book_id = book.split("/")[5].split("_")[1]
    allchars = glob(f"{book}/**/*.tif", recursive=True)
    for char in allchars:
        book_id = int(re.search(r"_(\d{8})_", char).groups()[0])
        spread_seq = int(re.search(r"-(\d{3})_", char).groups()[0])
        page_no = re.search(r"page(\d)", char).groups()[0]
        if page_no == "1":
            page_side = "l"
        else:
            page_side = "r"
        line_seq = int(re.search(r"line(\d+)_", char).groups()[0])
        char_seq = int(re.search(r"_char(\d+)_", char).groups()[0])
        char_class = re.search(r"([A-Z]_[a-z]{2})\.tif", char).groups()[0]

        line_id = requests.get(
            f"{b}lines/",
            params={
                "book_id": book_id,
                "spread_sequence": spread_seq,
                "page_side": page_side,
                "sequence": line_seq,
            },
            headers=ht,
        ).json()["results"][0]["pk"]

        try:
            char_image = requests.post(
                f"{b}images/quick_create/",
                data={"tiff": char, "jpeg": re.sub("tif", "jpeg", char)},
                headers=ht,
            ).json()["pk"]
        except:
            char_image = requests.get(
                f"{b}images/", params={"filepath": char}, headers=ht
            ).json()["results"][0]["pk"]

        requests.post(
            f"{b}character_classes/", data={"classname": char_class}, headers=ht
        ).json()

        char_id = requests.post(
            f"{b}characters/",
            data={
                "created_by_run": run_id,
                "line": line_id,
                "sequence": char_seq,
                "character_class": char_class,
                "class_probability": 0.74,
                "x_min": 0,
                "x_max": 100,
                "primary_image": char_image,
            },
            headers=ht,
        )
        print(char_id.json())
