"""
Script to load JSON-formatted outputs from Ocular into the P&P REST API.
"""

import requests
import json
import logging
from glob import glob
import optparse
import re

AUTH_TOKEN = open("/pylon5/hm4s82p/shared/api/api_token.txt", "r").read()
AUTH_HEADER = {"Authorization": f"Token {AUTH_TOKEN}"}
PP_URL = "https://printprobdb.library.cmu.edu/api"


class CharacterClasses:
    """
    Utility to create a hashmap of Ocular character codes to database IDs, so that we don't need to check every single time
    """

    data = {}

    def load_character_classes(self):
        """
        Create a dict of all currently-loaded character classes
        """
        cc_res = requests.get(
            f"{PP_URL}/character_classes/", params={"limit": 500}, headers=AUTH_HEADER
        )
        if cc_res.status_code == 200:
            for cc in cc_res.content.results:
                self.data[cc["ocular_code"]]: cc["id"]
        else:
            raise Exception(cc_res.content)

    def get_or_create(self, ocular_code):
        try:
            return self.data[ocular_code]
        except:
            cc_res = requests.post(
                f"{PP_URL}/character_classes/",
                json={"id": ocular_code, "ocular_code": ocular_code},
                headers=AUTH_HEADER,
            )
            if cc_res.status_code == 201:
                self.data[ocular_code] = ocular_code
                return ocular_code
            else:
                raise Exception(cc_res.content)


class BookLoader:
    def __init__(self, book_id, lines_directory):
        self.book_id = book_id
        self.lines_directory = lines_directory
        self.cc = CharacterClasses()
        self.cc.load_character_classes()

    def load_db(self):
        self.confirm_book()
        self.load_lines_json()
        self.create_pages()
        self.create_lines()

    def confirm_book(self):
        """
        Confirm that the book actually exists on Bridges
        """
        res = requests.get(f"{PP_URL}/books/{self.book_id}/", headers=AUTH_HEADER)
        if res.status_code != 200:
            raise Exception(
                f"The book {book_id} is not yet registered in the database. Please confirm you have used the correct UUID."
            )

    def load_lines_json(self):
        self.linefiles = glob(f"{lines_directory}/*.json")
        if len(linefiles) <= 0:
            raise Exception("No json files found in the given directory")
        self.lines = []
        for linefile in self.linefiles:
            line_obj = json.load(open(linefile, "rb"))
            line_obj["page_num"] = int(re.search(r"\d{4}", linefile).group(0))
            self.lines.append(line_obj)
        n_lines = len(self.lines)
        logging.info(f"{len(self.lines)} line files loaded")

    def create_pages(self):
        # Create a list of unique pages represented across all the loaded JSON files
        duplicated_pages = [
            {"page_num": l["page_num"], "page_filename": l["page_filename"]}
            for l in self.lines
        ]
        self.pages = list({v["page_filename"]: v for v in duplicated_pages}.values())
        page_run_response = requests.post(
            f"{PP_URL}/runs/pages/",
            json={
                "book": self.book_id,
                "date_started": self.page_data["run"]["datetime_started"],
            },
            headers=AUTH_HEADER,
        )
        if page_run_respone.status_code != 200:
            raise Exception(f"Page run couldn't be created: {page_run_respone.content}")
        page_run_id = page_run_response.json()["id"]
        for p in self.pages:
            page_response = requests.post(
                f"{PP_URL}/pages/",
                json={
                    "created_by_run": page_run_id,
                    "sequence": p["page_num"],
                    "tif": p["page_filename"],
                },
                headers=AUTH_HEADER,
            )
            if page_response.status_code != 201:
                raise Exception(f"Page couldn't be created: {page_run_respone.content}")
            p["id"]: page_response.json()["id"]
            logging.info(f"Page {p['page_num']} loaded as {p['id']}")

    def create_lines(self):
        line_run_response = requests.post(
            f"{PP_URL}/run/lines/",
            json={
                "book": self.book_id,
                "date_started": self.line_data["run"]["datetime_started"],
            },
            headers=AUTH_HEADER,
        )
        if line_run_response.status_code != 201:
            raise Exception(f"Couldn't create line run: {line_run.content}")
        self.line_run_id = line_run_response.json()["id"]

        character_run_response = requests.post(
            f"{PP_URL}/run/characters/",
            json={
                "book": self.book_id,
                "date_started": self.line_data["run"]["datetime_started"],
            },
            headers=AUTH_HEADER,
        )
        if character_run_response.status_code != 201:
            raise Exception(
                f"Couldn't create line run: {character_run_response.content}"
            )
        self.character_run_id = character_run_response.json()["id"]

        for line in self.lines:
            line_response = requests.post(
                f"{PP_URL}/lines/",
                json={
                    created_by_run: line_run_id,
                    "page": line["page_id"],
                    "sequence": line["sequence"],
                    "y_min": line["y_start"],
                    "y_max": line["y_end"],
                },
                headers=AUTH_HEADER,
            )
            if line_response.status_code != 201:
                raise Exception(line.content)
            line.id = line_response.json()["id"]
            logging.info(f"Line {line['id']} created")
            for char in line["characters"]:
                char_type = self.cc.get_or_create(char["character_class"])
                char_response = requests.post(
                    f"{PP_URL}/characters/",
                    json={
                        "created_by_run": self.line_run_id,
                        "line": line.id,
                        "sequence": char["sequence"],
                        "offset": char["offset"],
                        "class_probability": char["logprob"],
                        "character_class": char_type,
                        "x_max": char["x_end"],
                        "x_start": char["x_start"],
                    },
                )
                if character.status_code != 201:
                    raise Exception(character.content)
                logging.info(f"Character {char_response.json['id']} loaded")


def main():
    # Options and arguments
    p = optparse.OptionParser(
        description="Load a directory containing Ocular JSON outputs",
        usage="usage: %prog [options] (-h for help)",
    )
    p.add_option(
        "-b",
        "--book_id",
        dest="book_id",
        help="UUID of the book from printprobability.bridges.psc.edu",
    )
    p.add_option(
        "-l",
        "--lines",
        dest="lines",
        help="Absolute directory path (starting with /pylon5) of the file where the Ocular JSON output is stored for lines.",
    )

    (opt, sources) = p.parse_args()

    pp_loader = BookLoader(book_id=opt.book_id, lines_directory=opt.lines,)
    pp_loader.load_db()


if __name__ == "__main__":
    main()
