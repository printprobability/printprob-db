import csv
from bl_dl import Manifest

with open("bl_pre1700_images.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row.keys())
        manifest_url = row["IIIF manifest (1)"]
        man1 = Manifest(url=manifest_url, dest_dir="britishlibrary")
        man1.pull_images()
