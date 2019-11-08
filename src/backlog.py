import requests
from glob import glob
import re
import os
import hashlib

ROOT = "/Users/mlincoln/Development/printprobability/pp-images/"


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
        self.page_run = PageRun(self)
        self.spreads = []
        self.pages = []

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
    def page_log(self):
        return self.page_directory + "pagelog.txt"

    @property
    def line_directory(self):
        return f"{self.book_directory}lines/"

    @property
    def char_dimensions_dir(self):
        return f"{ROOT}srijhwan/broken_type_new/output_{self.bookstring}/"

    @property
    def char_images_dir(self):
        return f"{ROOT}srijhwan/broken_type_new/char_images3/{self.bookstring}/"

    def gen_spreads(self):
        spread_files = [
            self.page_directory + f
            for f in os.listdir(self.page_directory)
            if re.search(r".+\d{3}\.tif", f)
        ]
        self.spreads = [Spread(book=self, filepath=f) for f in spread_files]

    def gen_pages(self):
        page_log = open(self.page_log, "r").read().split("\n")
        all_pages = []
        for pl in page_log:
            if pl == "":
                continue
            log_items = pl.split(",")
            print(log_items)
            page_image_path = self.page_directory + log_items[1].replace("./", "")
            print(f"Page image path: {page_image_path}")
            spread_index = int(re.match(r"^.+-(\d{3})_", page_image_path).groups()[0])
            print(self.spreads[spread_index - 1])
            all_pages.append(
                Page(
                    pagerun=self.page_run,
                    spread=self.spreads[spread_index - 1],
                    filepath=page_image_path,
                    x=float(log_items[2]),
                    y=float(log_items[3]),
                    w=float(log_items[4]),
                    h=float(log_items[5]),
                    rot1=float(log_items[6]),
                    rot2=float(log_items[6]),
                )
            )
        return all_pages


class Image:
    def __init__(self, endpoint, filepath):
        self.endpoint = endpoint
        self.filepath = filepath
        print(f"Image: {self.filepath}")
        res = requests.post(
            self.endpoint.endpoint + "images/",
            data={"tif": self.relative_filepath, "tif_md5": self.md5},
            headers=self.endpoint.auth_header,
        )
        try:
            self.id = res.json()["id"]
        except:
            print(self.relative_filepath)
            raise Exception(res.text)

    @property
    def md5(self):
        return hashlib.md5(open(self.filepath, "rb").read()).hexdigest()

    @property
    def relative_filepath(self):
        return "/" + self.filepath.replace(ROOT, "")


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


class PageRun:
    def __init__(self, book):
        self.book = book
        self.id = requests.post(
            self.book.endpoint.endpoint + "runs/pages/",
            data={"book": book.id},
            headers=self.book.endpoint.auth_header,
        ).json()["id"]
        print(f"Page run {self.id} created")


class Page:
    def __init__(self, pagerun, spread, filepath, x, y, w, h, rot1, rot2):
        self.endpoint = spread.book.endpoint
        self.pagerun = pagerun
        self.spread = spread
        self.filepath = filepath
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rot1 = rot1
        self.rot2 = rot2
        self.image = Image(endpoint=self.endpoint, filepath=self.filepath)
        res = requests.post(
            self.endpoint.endpoint + "pages/",
            data={
                "created_by_run": self.pagerun.id,
                "spread": self.spread.id,
                "side": self.side,
                "x": self.x,
                "y": self.y,
                "w": self.w,
                "h": self.h,
                "rot1": self.rot1,
                "rot2": self.rot2,
                "image": self.image.id,
            },
            headers=self.endpoint.auth_header,
        )
        try:
            self.id = res.json()["id"]
        except:
            print(res.text)
            raise Exception

    @property
    def side(self):
        try:
            side_string = re.match(r".+page(\d)", self.filepath).groups()[0]
            if side_string == "1":
                return "l"
            else:
                return "r"
        except:
            return None


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
print(anon1.gen_spreads())
print(anon1.gen_pages())
