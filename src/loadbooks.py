import os
import requests
import re
from glob import glob
from uuid import UUID

b = os.environ['TEST_HOST']
ht = {"Authorization": f"Token {os.environ['TEST_TOKEN']}"}

books = glob("/Volumes/data_mdlincoln/pp/books/*")
print(books)

# Start a run
run_id = requests.post(f"{b}runs/", data={"notes": "trial run"}, headers=ht).json()[
    "pk"
]
print(run_id)

def cleanpath(s):
    return re.sub("^.+/pp/", "/", s)

for book in books:
    bnames = book.split("/")[-1].split("_")
    print(bnames)
    r = requests.post(
        f"{b}books/",
        data={
            "estc": int(bnames[1]),
            "vid": int(bnames[2]),
            "publisher": bnames[0],
            "title": bnames[4],
        },
        headers=ht,
    ).json()
    print(r)
    spread_pix = [f for f in glob(f"{book}/*.tif") if re.search("\d{3}\.tif", f)]
    for s in spread_pix:
        snames = s.split("/")[-1].split("_")[-1].split("-")[-1].split(".")[0]
        print(snames)
        # create new images/image_files
        spath = cleanpath(s)
        image_id = requests.post(
            f"{b}images/quick_create/",
            data={"tiff": spath, "jpeg": re.sub("tif", "jpeg", spath)},
            headers=ht,
        ).json()["pk"]
        print(image_id)
        spread_id = requests.post(
            f"{b}spreads/",
            data={"book": int(bnames[1]), "sequence": int(snames), "primary_image": image_id},
            headers=ht,
        ).json()["pk"]
        print(spread_id)

        pagepics = [
            p for p in glob(f"{book}/*.tif") if re.search(f"{snames}_page\d\.tif", p)
        ]
        if len(pagepics) < 2:
            continue
        lpath = cleanpath(pagepics[0])
        left_page_pic = requests.post(
            f"{b}images/quick_create/",
            data={"tiff": lpath, "jpeg": re.sub("tif", "jpeg", lpath)},
            headers=ht,
        ).json()["pk"]
        left_page_id = requests.post(
            f"{b}pages/",
            data={
                "spread": spread_id,
                "side": "l",
                "created_by_run": run_id,
                "x_min": 0,
                "x_max": 0,
                "primary_image": left_page_pic,
            },
            headers=ht,
        ).json()["pk"]
        rpath = cleanpath(pagepics[1])
        right_page_pic = requests.post(
            f"{b}images/quick_create/",
            data={"tiff": rpath, "jpeg": re.sub("tif", "jpeg", rpath)},
            headers=ht,
        ).json()["pk"]
        right_page_id = requests.post(
            f"{b}pages/",
            data={
                "spread": spread_id,
                "side": "r",
                "created_by_run": run_id,
                "x_min": 0,
                "x_max": 0,
                "primary_image": right_page_pic,
            },
            headers=ht,
        ).json()["pk"]
        left_lines = [
            p
            for p in glob(f"{book}/*.tif")
            if re.search(f"{snames}_page1r_line\d+.tif", p)
        ]
        for l in left_lines:
            print(l)
            l_image_id = requests.post(
                f"{b}images/quick_create/",
                data={"tiff": cleanpath(l), "jpeg": re.sub("tif", "jpeg", cleanpath(l))},
                headers=ht,
            ).json()["pk"]
            lseq = int(re.search(r"(\d+)\.tif", l).groups()[0])
            line_id = requests.post(
                f"{b}lines/",
                data={
                    "created_by_run": run_id,
                    "page": left_page_id,
                    "sequence": lseq,
                    "y_min": 0,
                    "y_max": 0,
                    "primary_image": l_image_id,
                },
                headers=ht,
            ).json()["pk"]
        right_lines = [
            p
            for p in glob(f"{book}/*.tif")
            if re.search(f"{snames}_page2r_line\d+.tif", p)
        ]
        for l in right_lines:
            print(l)
            l_image_id = requests.post(
                f"{b}images/quick_create/",
                data={"tiff": cleanpath(l), "jpeg": re.sub("tif", "jpeg", cleanpath(l))},
                headers=ht,
            ).json()["pk"]
            lseq = int(re.search(r"(\d+)\.tif", l).groups()[0])
            line_id = requests.post(
                f"{b}lines/",
                data={
                    "created_by_run": run_id,
                    "page": right_page_id,
                    "sequence": lseq,
                    "y_min": 0,
                    "y_max": 0,
                    "primary_image": l_image_id,
                },
                headers=ht,
            ).json()["pk"]
