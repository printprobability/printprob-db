import csv
import os

books_with_vid = []
ocr_results_without_vid = []

# Get ocr_results filenames

ocr_results = [
    d.name.replace("_color", "")
    for d in list(os.scandir("/pylon5/hm4s82p/shared/ocr_results/json_output"))
]

# Load CSV

with open("pp_master.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for rec in reader:
        matchname = rec["conc"] + "_color"
        if rec["conc"] in ocr_results:
            try:
                books_with_vid.append({"vid": int(rec["VID"]), "json_name": matchname})
            except:
                ocr_results_without_vid.append({"json_name": matchname})


with open("books_with_vid.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, ["VID", "json_name"])
    writer.writeheader()
    writer.writerows(books_with_vid)

with open("ocr_results_without_vid.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, ["json_name"])
    writer.writeheader()
    writer.writerows(ocr_results_without_vid)
