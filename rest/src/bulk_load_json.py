"""
Script to load JSON-formatted outputs from Ocular into the P&P REST API.
"""

import requests
import json
import logging
from glob import glob
import optparse
import re

AUTH_TOKEN = open("/pylon5/hm4s82p/shared/api/api_token.txt", "r").read().strip()
AUTH_HEADER = {"Authorization": f"Token {AUTH_TOKEN}"}
PP_URL = "http://localhost/api"
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
                logging.info(f"{ocular_code} created")
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
        # Add a "side" to every page
        for page in self.pages:
            page["side"] = "s"
        logging.info(f"{len(self.pages)} pages loaded")
        self.lines = json.load(open(f"{self.json_directory}/lines.json", "r"))["lines"]
        logging.info(f"{len(self.lines)} lines loaded")
        self.characters = json.load(open(f"{self.json_directory}/chars.json", "r"))[
            "chars"
        ]
        # Normalize characters
        for character in self.characters:
            character["character_class"] = self.cc.get_or_create(
                character["character_class"]
            )
        logging.info(f"{len(self.characters)} characters loaded")

    def create_pages(self):
        bulk_page_response = requests.post(
            f"{PP_URL}/books/{self.book_id}/bulk_pages/",
            json={"pages": self.pages, "tif_root": "/pylon5/hm4s82p/shared"},
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        logging.info(bulk_page_response.content)

    def create_lines(self):
        bulk_line_response = requests.post(
            f"{PP_URL}/books/{self.book_id}/bulk_lines/",
            json={"lines": self.lines},
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        logging.info(bulk_line_response.content)

    def create_characters(self):
        bulk_character_response = requests.post(
            f"{PP_URL}/books/{self.book_id}/bulk_characters/",
            json={"characters": self.characters},
            headers=AUTH_HEADER,
            verify=CERT_PATH,
        )
        logging.info(bulk_character_response.content)


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

    pp_loader = BookLoader(book_id=opt.book_id, json_directory=opt.json,)
    pp_loader.load_db()


if __name__ == "__main__":
    main()
