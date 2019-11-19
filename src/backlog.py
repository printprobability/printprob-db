import requests
from glob import glob
import re
import os
import hashlib
from base64 import b64encode
from logging import warning
import optparse
from tqdm import tqdm

CHARTYPE_DICT = {
    "!": "exclamation",
    " ": "space",
    ",": "comma",
    ".": "period",
    "-": "hyphen",
    ":": "colon",
    ";": "semicolon",
    "?": "question",
    "'": "apostrophe",
    '"': "doublequote",
    "(": "openparentheses",
    ")": "closeparentheses",
    "[": "openbracket",
    "]": "closebracket",
    "*": "asterisk",
    "/": "forwardslash",
    "#": "pound",
    "^": "caret",
    "+": "plus",
    "=": "equals",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "ſ": "long_s",
    "a": "a_lc",
    "b": "b_lc",
    "c": "c_lc",
    "d": "d_lc",
    "e": "e_lc",
    "f": "f_lc",
    "g": "g_lc",
    "h": "h_lc",
    "i": "i_lc",
    "j": "j_lc",
    "k": "k_lc",
    "l": "l_lc",
    "m": "m_lc",
    "n": "n_lc",
    "o": "o_lc",
    "p": "p_lc",
    "q": "q_lc",
    "r": "r_lc",
    "s": "s_lc",
    "t": "t_lc",
    "u": "u_lc",
    "v": "v_lc",
    "w": "w_lc",
    "x": "x_lc",
    "y": "y_lc",
    "z": "z_lc",
    "A": "A_uc",
    "B": "B_uc",
    "C": "C_uc",
    "D": "D_uc",
    "E": "E_uc",
    "F": "F_uc",
    "G": "G_uc",
    "H": "H_uc",
    "I": "I_uc",
    "J": "J_uc",
    "K": "K_uc",
    "L": "L_uc",
    "M": "M_uc",
    "N": "N_uc",
    "O": "O_uc",
    "P": "P_uc",
    "Q": "Q_uc",
    "R": "R_uc",
    "S": "S_uc",
    "T": "T_uc",
    "U": "U_uc",
    "V": "V_uc",
    "W": "W_uc",
    "X": "X_uc",
    "Y": "Y_uc",
    "Z": "Z_uc",
}


class Endpoint:
    def __init__(self, endpoint, token, root):
        self.endpoint = endpoint
        self.token = token
        self.root = root
        res = requests.get(endpoint + "books/", headers=self.auth_header)
        if res.status_code != 200:
            raise Exception("Endpoint/token not allowed")
        else:
            print(f"Authorized at {self.endpoint}")
        self.load_chartypes()

    def load_chartypes(self):
        for s, sid in CHARTYPE_DICT.items():
            try:
                requests.post(
                    self.endpoint + "character_classes/",
                    data={"classname": sid},
                    headers=self.auth_header,
                )
            except:
                continue

    @property
    def auth_header(self):
        return {"Authorization": f"Token {self.token}"}


class Book:
    def __init__(self, endpoint, bookstring):
        self.bookstring = bookstring
        self.endpoint = endpoint
        res = requests.get(
            self.endpoint.endpoint + "books/",
            params={"vid": self.vid},
            headers=self.endpoint.auth_header,
        )
        try:
            self.id = res.json()["results"][0]["id"]
        except:
            raise Exception(
                f"No book with VID {self.vid} found. Full error: {res.text}"
            )
        self.spreads = []
        self.page_run = PageRun(self)
        self.pages = []
        self.line_run = LineRun(self)
        self.lines = []
        self.character_run = CharacterRun(self)
        self.characters = []
        self.gen_spreads()
        self.gen_pages()
        self.gen_lines()

    def validate_data(self):
        # Line results must exist

        # Character results must exist

    @property
    def vid(self):
        return int(re.match("^[A-Za-z]+_\d+_(\d+)_", self.bookstring).groups()[0])

    @property
    def book_directory(self):
        return (
            f"{self.endpoint.root}mpwillia/line_extractions/complete/{self.bookstring}/"
        )

    @property
    def spread_directory(self):
        return f"{self.book_directory}book/"

    @property
    def book_pdf(self):
        return glob(self.book_directory + "*.pdf")[0]

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
    def extractions_dir(self):
        return f"{self.endpoint.root}srijhwan/broken_type_new/output_{self.bookstring}/extractions/"

    @property
    def char_images_dir(self):
        return f"{self.endpoint.root}srijhwan/broken_type_new/char_images3/{self.bookstring}/"

    def gen_spreads(self):
        spread_files = [
            self.page_directory + f
            for f in os.listdir(self.page_directory)
            if re.search(r".+\d{3}\.tif", f)
        ]
        self.spreads = [Spread(book=self, filepath=f) for f in spread_files]

    def gen_pages(self):
        page_log = open(self.page_log, "r").read().split("\n")
        for pl in page_log:
            if pl == "":
                continue
            log_items = pl.split(",")
            # print(log_items)
            page_image_path = self.page_directory + log_items[1].replace(
                "./", ""
            ).replace(".tif", "r.tif")
            # print(f"Page image path: {page_image_path}")
            spread_index = int(re.match(r"^.+-(\d{3})_", page_image_path).groups()[0])
            try:
                spread = [s for s in self.spreads if s.sequence == spread_index][0]
            except:
                raise Exception(f"Spread {spread_index} not found.")
            # print(self.spreads[spread_index - 1])
            self.pages.append(
                Page(
                    pagerun=self.page_run,
                    spread=spread,
                    filepath=page_image_path,
                    x=float(log_items[2]),
                    y=float(log_items[3]),
                    w=float(log_items[4]),
                    h=float(log_items[5]),
                    rot1=float(log_items[6]),
                    rot2=float(log_items[6]),
                )
            )

    def gen_lines(self):
        line_stats = glob(self.line_directory + "*.tif.csv")
        for l in tqdm(line_stats, desc="Loading pages"):
            l_text = open(l, "r").read()
            if re.match(r".+page(\d)r", l).groups()[0] == "1":
                page_side = "l"
            else:
                page_side = "r"
            spread_sequence = int(re.match(r".+-(\d{3})_page", l).groups()[0])
            for r in tqdm(l_text.split("\n"), desc="Lines", leave=False):
                if r == "":
                    continue
                l_row = r.split(",")

                matches = [
                    p
                    for p in self.pages
                    if p.side == page_side and p.spread.sequence == spread_sequence
                ]
                if len(matches) == 1:
                    page = matches[0]
                else:
                    raise Exception(
                        f"{self.extraction_filepath} should exist but doesn't"
                    )
                new_line = Line(
                    line_run=self.line_run,
                    page=page,
                    character_run=self.character_run,
                    y1=l_row[0],
                    y2=l_row[1],
                    extraction_filepath=self.extractions_dir
                    + l_row[2]
                    .replace("./", "")
                    .replace("_line", ".png_line")
                    .replace("tif", "txt"),
                )


class Image:
    def __init__(self, endpoint, filepath):
        self.endpoint = endpoint
        self.filepath = filepath
        # print(self.relative_filepath)
        res = requests.post(
            self.endpoint.endpoint + "images/",
            data={"tif": self.relative_filepath, "tif_md5": self.md5},
            headers=self.endpoint.auth_header,
        )
        try:
            self.id = res.json()["id"]
        except:
            warning(self.relative_filepath)
            raise Exception(res.text)

    @property
    def md5(self):
        return hashlib.md5(open(self.filepath, "rb").read()).hexdigest()

    @property
    def relative_filepath(self):
        return "/" + self.filepath.replace(self.endpoint.root, "")


class Spread:
    def __init__(self, book, filepath):
        self.book = book
        self.filepath = filepath
        # print(self.filepath)
        self.image = Image(endpoint=self.book.endpoint, filepath=self.filepath)
        # print(f"Image {self.image.id} created")
        res = requests.post(
            self.book.endpoint.endpoint + "spreads/",
            data={"book": book.id, "sequence": self.sequence, "image": self.image.id},
            headers=self.book.endpoint.auth_header,
        )
        try:
            self.id = res.json()["id"]
        except:
            raise Exception(res.text)
        # print(f"Spread {self.id} created")

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
        # print(f"Page run {self.id} created")


class LineRun:
    def __init__(self, book):
        self.book = book
        self.id = requests.post(
            self.book.endpoint.endpoint + "runs/lines/",
            data={"book": book.id},
            headers=self.book.endpoint.auth_header,
        ).json()["id"]
        # print(f"Line run {self.id} created")


class CharacterRun:
    def __init__(self, book):
        self.book = book
        self.id = requests.post(
            self.book.endpoint.endpoint + "runs/characters/",
            data={"book": book.id},
            headers=self.book.endpoint.auth_header,
        ).json()["id"]
        # print(f"Character run {self.id} created")


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
            warning(res.text)
            raise Exception

    @property
    def side(self):
        try:
            side_string = self.side_number
            if side_string == "1":
                return "l"
            else:
                return "r"
        except:
            return None

    @property
    def side_number(self):
        return re.match(r".+page(\d)", self.filepath).groups()[0]


class Val:
    def __init__(self, valtext):
        self.value = valtext.split("\t")[1]


class Line:
    def __init__(self, page, line_run, character_run, y1, y2, extraction_filepath):
        self.line_run = line_run
        self.endpoint = self.line_run.book.endpoint
        self.extraction_filepath = extraction_filepath
        # print(self.extraction_filepath)
        self.y1 = y1
        self.y2 = y2
        self.page = page
        res = requests.post(
            self.endpoint.endpoint + "lines/",
            data={
                "created_by_run": self.line_run.id,
                "page": self.page.id,
                "sequence": self.sequence,
                "y_min": self.y1,
                "y_max": self.y2,
            },
            headers=self.endpoint.auth_header,
        )
        try:
            self.id = res.json()["id"]
        except:
            raise Exception(res.text)
        # print(f"Line {self.id} created")
        try:
            linepath = open(self.extraction_filepath, "r").read()
        except:
            warning(f"{self.extraction_filepath} doesn't exist. Skipping line)
        # print(self.extraction_filepath)
        # print(char_image_paths)
        # print(linepath)
        self.characters = []
        for i, lt in enumerate(linepath.split("\n\n")):
            if len(lt) > 0:
                self.characters.append(
                    Character(
                        character_run=character_run, line=self, chartext=lt, sequence=i
                    )
                )

    @property
    def spread_sequence(self):
        return

    @property
    def page_side(self):
        if re.match(r".+page(\d)r", self.extraction_filepath).groups()[0] == "1":
            page_side = "l"
        else:
            page_side = "r"
        return page_side

    @property
    def sequence(self):
        return int(
            re.match(r".+line(\d{1,2})\.txt", self.extraction_filepath).groups()[0]
        )


class Character:
    def __init__(self, character_run, line, chartext, sequence):
        self.line = line
        self.character_run = character_run
        self.endpoint = self.character_run.book.endpoint
        self.sequence = sequence
        self.chartext = chartext
        # print(self.image_filepath)
        # print(self.chartext)
        raw_text = self.chartext.split("\n")
        self.chartype = Val(raw_text[0]).value
        self.log_prob = float(Val(raw_text[1]).value)
        self.exposure = int(Val(raw_text[2]).value)
        self.offset = int(Val(raw_text[3]).value)
        self.begin = int(Val(raw_text[4]).value)
        self.end = int(Val(raw_text[5]).value)
        try:
            payload = {
                "created_by_run": self.character_run.id,
                "line": self.line.id,
                "sequence": self.sequence,
                "x_min": self.begin,
                "x_max": self.end,
                "offset": self.offset,
                "exposure": self.exposure,
                "character_class": CHARTYPE_DICT[self.chartype],
                "class_probability": self.log_prob,
            }
        except:
            return None
        res = requests.post(
            self.endpoint.endpoint + "characters/",
            data=payload,
            headers=self.endpoint.auth_header,
        )
        try:
            self.id = res.json()["id"]
        except:
            print(f"{payload} was rejected")
            raise Exception(res.text)

    @property
    def image_filepath(self):
        try:
            matches = [
                cp
                for cp in self.char_image_paths
                if re.search(r".+char" + str(self.sequence) + r"_", cp) is not None
            ]
            if len(matches) > 1:
                warning(f"Too many matches in: {matches}")
                raise Exception
            else:
                return matches[0]
        except:
            warning(
                f"Missing character image at: Spread {self.line.spread_sequence}, Page side {self.line.page_side}, Line no {self.line.sequence}, Char no {self.sequence}, Char type {self.chartype}"
            )
            raise Exception


def main():
    # Options and arguments
    p = optparse.OptionParser(
        description="Load book images into database",
        usage="usage: %prog [options] bookstring (-h for help)",
    )

    p.add_option("--endpoint", "-e", default=None, action="store", help="API Endpoint")

    p.add_option("--token", "-t", default=None, action="store", help="API token")

    p.add_option(
        "--root",
        "-r",
        default=None,
        action="store",
        help="Root directory of Ocular input/output files (e.g. Bridges workgroup directory)",
    )

    (opt, sources) = p.parse_args()

    local_db = Endpoint(endpoint=opt.endpoint, token=opt.token, root=opt.root)

    res = Book(endpoint=local_db, bookstring=sources[0])


if __name__ == "__main__":
    main()
