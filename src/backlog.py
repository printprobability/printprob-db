import requests
from glob import glob
import re
import os
import hashlib

ROOT = "/Users/mlincoln/Desktop/anon/"


class Endpoint:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token
        res = requests.get(endpoint + "books/", headers=self.auth_header)
        if res.status_code != 200:
            raise Exception("Endpoint/token not allowed")
        else:
            print(f"Authorized at {self.endpoint}")

    @property
    def auth_header(self):
        return {"Authorization": f"Token {self.token}"}


class Book:
    def __init__(self, endpoint, bookstring):
        self.bookstring = bookstring
        self.endpoint = endpoint
        self.id = requests.get(
            self.endpoint.endpoint + "books/",
            params={"eebo": self.eebo},
            headers=self.endpoint.auth_header,
        ).json()["results"][0]["id"]

    @property
    def eebo(self):
        return int(re.match("^[A-Za-z]+_(\d+)_", self.bookstring).groups()[0])

    @property
    def book_directory(self):
        return f"{ROOT}mpwillia/line_extractions/complete/{self.bookstring}/"

    @property
    def book_pdf(self):
        return glob(self.book_directory, "*.pdf")[0]

    @property
    def page_directory(self):
        return f"{self.book_directory}pages/"

    @property
    def line_directory(self):
        return f"{self.book_directory}lines/"

    @property
    def char_dimensions_dir(self):
        return f"{ROOT}srijhwan/broken_type_new/output_{self.bookstring}/"

    @property
    def char_images_dir(self):
        return f"{ROOT}srijhwan/broken_type_new/char_images3/{self.bookstring}/"

    @property
    def spreads(self):
        spread_files = [
            self.page_directory + f
            for f in os.listdir(self.page_directory)
            if re.search(r".+\d{3}\.tif", f)
        ]
        return [Spread(book=self, filepath=f) for f in spread_files]


class Image:
    def __init__(self, endpoint, filepath):
        self.endpoint = endpoint
        self.filepath = filepath
        self.id = requests.post(
            self.endpoint.endpoint + "images/",
            data={"tif": self.filepath, "tif_md5": self.md5},
            headers=self.endpoint.auth_header,
        ).json()["id"]

    @property
    def md5(self):
        return hashlib.md5(open(self.filepath, "rb").read()).hexdigest()


class Spread:
    def __init__(self, book, filepath):
        self.book = book
        self.filepath = filepath
        self.image = Image(endpoint=self.book.endpoint, filepath=self.filepath)
        print(f"Image {self.image.id} created")
        self.id = requests.post(
            self.book.endpoint.endpoint + "spreads/",
            data={"book": book.id, "sequence": self.sequence, "image": self.image.id},
            headers=self.book.endpoint.auth_header,
        ).json()["id"]
        print(f"Spread {self.id} created")

    @property
    def sequence(self):
        return int(re.match(r".+-(\d{3})\.tif", self.filepath).groups()[0])


class Val:
    def __init__(self, valtext):
        self.value = valtext.split("\t")[1]


class Char:
    def __init__(self, chartext):
        raw_text = chartext.split("\n")
        self.chartype = Val(raw_text[0]).value
        self.log_prob = float(Val(raw_text[1]).value)
        self.exposure = int(Val(raw_text[2]).value)
        self.offset = int(Val(raw_text[3]).value)
        self.begin = int(Val(raw_text[4]).value)
        self.end = int(Val(raw_text[5]).value)
        self.line = int(Val(raw_text[6]).value)


class Line:
    def __init__(self, fp):
        self.filepath = fp
        linetext = open(fp, "r").read()
        self.chars = [Char(lt) for lt in linetext.split("\n\n") if len(lt) > 0]

    @property
    def eebo(self):
        try:
            return int(re.match(r".+_(\d{8})_", self.filepath).groups()[0])
        except:
            return None

    @property
    def spread_sequence(self):
        try:
            return int(re.match(r".+-(\d{3})_page", self.filepath).groups()[0])
        except:
            return None

    @property
    def page_side(self):
        try:
            side_string = re.match(r".+page(..)", self.filepath).groups()[0]
            if side_string == "1r":
                return "l"
            else:
                return "r"
        except:
            return None

    @property
    def line_sequence(self):
        return self.chars[0].line


local_db = Endpoint(
    endpoint="http://localhost/api/", token="373f5a24e62a8327971cce64dc5458dbfcfbd1d9"
)
anon1 = Book(
    endpoint=local_db, bookstring="anon_9053941_42343_65height_treatiseofexecution"
)
print(anon1.spreads)
