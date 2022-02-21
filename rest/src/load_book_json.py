"""
Script to load JSON-formatted outputs from Ocular into the P&P REST API.
"""

import requests
from retrying import retry
import json
import logging
from glob import glob
import optparse
import re

AUTH_TOKEN = open("/pylon5/hm4s82p/shared/api/api_token.txt", "r").read().strip()
AUTH_HEADER = {"Authorization": f"Token {AUTH_TOKEN}"}
PP_URL = "https://printprobdb.bridges.psc.edu/api"
CERT_PATH = "/pylon5/hm4s82p/shared/api/incommonrsaserverca-bundle.crt"


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
            f"{PP_URL}/character_classes/",
            params={"limit": 500},
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        if cc_res.status_code == 200:
            for cc in cc_res.json()["results"]:
                self.data[cc["classname"]] = cc["classname"]
            logging.info(self.data)
        else:
            raise Exception(cc_res.content)

    def get_or_create(self, ocular_code):
        if ocular_code == "":
            ocular_code = "space"
        elif ocular_code == ".":
            ocular_code = "period"
        elif ocular_code == ";":
            ocular_code = "semicolon"
        elif ocular_code == "/":
            ocular_code = "slash"
        elif ocular_code == "\\":
            ocular_code = "backslash"
        logging.info(ocular_code)
        try:
            return self.data[ocular_code]
        except:
            cc_res = requests.post(
                f"{PP_URL}/character_classes/",
                json={"classname": ocular_code, "label": ocular_code},
                headers=AUTH_HEADER,
                verify=CERT_PATH,
            )
            if cc_res.status_code == 201:
                self.data[ocular_code] = ocular_code
                return ocular_code
            else:
                raise Exception(cc_res.content)


class BookLoader:
    def __init__(self, book_id, json_directory):
        self.book_id = book_id
        self.json_directory = json_directory
        self.cc = CharacterClasses()
        self.cc.load_character_classes()

    def load_db(self):
        self.confirm_book()
        self.load_json()
        self.create_pages()
        self.create_lines()
        self.create_characters()

    def confirm_book(self):
        """
        Confirm that the book actually exists on Bridges
        """
        res = requests.get(
            f"{PP_URL}/books/{self.book_id}/", headers=AUTH_HEADER, verify=CERT_PATH
        )
        if res.status_code != 200:
            raise Exception(
                f"The book {book_id} is not yet registered in the database. Please confirm you have used the correct UUID."
            )

    def load_json(self):
        self.pages = json.load(open(f"{self.json_directory}/pages.json", "r"))["pages"]
        logging.info(f"{len(self.pages)} pages loaded")
        self.lines = json.load(open(f"{self.json_directory}/lines.json", "r"))["lines"]
        logging.info(f"{len(self.lines)} lines loaded")
        self.characters = json.load(open(f"{self.json_directory}/chars.json", "r"))[
            "chars"
        ]
        logging.info(f"{len(self.characters)} characters loaded")

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_delay=30000,
    )
    def make_post(self, url, json):
        res = requests.post(url, json=json, headers=AUTH_HEADER, verify=CERT_PATH)
        if res.status_code != 201:
            try:
                if "id" in res.json():
                    # IF there's a duplicated ID, that means it was already loaded. Keep going.
                    logging.warning(res.json())
                    return None
            except:
                logging.warning(f"Retrying {json}")
                raise Exception(f"Couldn't be created: {res.content}")
        return res

    def create_pages(self):
        page_run_response = requests.post(
            f"{PP_URL}/runs/pages/",
            json={"book": self.book_id},
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        if page_run_response.status_code != 201:
            raise Exception(
                f"Page run couldn't be created: {page_run_response.content}"
            )
        page_run_id = page_run_response.json()["id"]
        for p in self.pages:
            page_response = requests.post(
                f"{PP_URL}/pages/",
                json={
                    "id": p["id"],
                    "created_by_run": page_run_id,
                    "sequence": p["sequence"],
                    "side": "s",
                    "tif": p["filename"].replace("/pylon5/hm4s82p/shared", ""),
                },
                headers=AUTH_HEADER,
                verify=CERT_PATH,
            )
            if page_response.status_code != 201:
                raise Exception(f"Page couldn't be created: {page_response.content}")
            page_response_id = page_response.json()["id"]
            if page_response_id != p["id"]:
                raise Exception(
                    f"Page id submitted as {p['id']} but {page_response_id} returned instead"
                )
            logging.info(f"Page {p['sequence']} loaded as {p['id']}")

    def create_lines(self):
        line_run_response = requests.post(
            f"{PP_URL}/runs/lines/",
            json={
                "book": self.book_id,
            },
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        if line_run_response.status_code != 201:
            raise Exception(f"Couldn't create line run: {line_run_response.content}")
        self.line_run_id = line_run_response.json()["id"]

        for line in self.lines:
            line_response = requests.post(
                f"{PP_URL}/lines/",
                json={
                    "id": line["id"],
                    "created_by_run": self.line_run_id,
                    "page": line["page_id"],
                    "sequence": line["sequence"],
                    "y_min": line["y_start"],
                    "y_max": line["y_end"],
                },
                headers=AUTH_HEADER,
                verify=CERT_PATH,
            )
            if line_response.status_code != 201:
                raise Exception(line.content)
            line_response_id = line_response.json()["id"]
            if line_response_id != line["id"]:
                raise Exception(
                    f"Line id submitted as {line['id']} but {line_response_id} returned instead"
                )
            logging.info(f"Line {line['id']} created")

    def create_characters(self):
        character_run_response = requests.post(
            f"{PP_URL}/runs/characters/",
            json={
                "book": self.book_id,
            },
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        if character_run_response.status_code != 201:
            raise Exception(
                f"Couldn't create line run: {character_run_response.content}"
            )
        self.character_run_id = character_run_response.json()["id"]

        for char in self.characters:
            char_type = self.cc.get_or_create(char["character_class"])
            char_response = self.make_post(
                url=f"{PP_URL}/characters/",
                json={
                    "id": char["id"],
                    "created_by_run": self.character_run_id,
                    "line": char["line_id"],
                    "sequence": char["sequence"],
                    "offset": char["offset"],
                    "exposure": char["exposure"],
                    "class_probability": char["logprob"],
                    "character_class": char_type,
                    "x_max": char["x_end"],
                    "x_min": char["x_start"],
                    "y_max": char["y_end"],
                    "y_min": char["y_start"],
                },
            )
            # if char_response.status_code != 201:
            #     raise Exception(char_response.content)
            # char_response_id = char_response.json()["id"]
            # if char_response_id != char["id"]:
            #     raise Exception(
            #         f"Character id submitted as {char['id']} but {char_response_id} returned instead"
            #     )
            logging.info(f"Character {char['id']} loaded")


def main():

    logging.basicConfig(level=logging.INFO)

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
        "-j",
        "--json",
        dest="json",
        help="Absolute directory path (starting with /pylon5) where the Ocular JSON output is stored.",
    )

    (opt, sources) = p.parse_args()

    logging.info(f"Using {CERT_PATH} for SSL verification")

    pp_loader = BookLoader(
        book_id=opt.book_id,
        json_directory=opt.json,
    )
    pp_loader.load_db()


if __name__ == "__main__":
    main()
