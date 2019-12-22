import requests
import shutil
import json
from time import sleep
import re
from os import path, makedirs
import sys
import optparse


class Manifest:
    def __init__(self, url, dest_dir):
        self.url = url
        self.data = requests.get(url).json()
        self.images = []
        self.get_image_info()
        self.bl_id = self.url.split("/")[7]
        self.dir = f"{dest_dir}/{self.bl_id}"
        if not path.isdir(self.dir):
            makedirs(self.dir)

    def get_image_info(self):
        for index, img in enumerate(self.data["sequences"][0]["canvases"]):
            iobj = Image(
                data=img["images"][0]["resource"]["service"], seq=index, parent=self
            )
            self.images.append(iobj)

    def pull_images(self):
        for img in self.images:
            if img.is_downloaded:
                continue
            else:
                # be polite and sleep
                sleep(0.3)
                img.download_image()


class Image:
    def __init__(self, data, seq, parent):
        self.data = data
        self.seq = seq
        self.parent = parent

    @property
    def img_id(self):
        return self.data["@id"]

    @property
    def url(self):
        return f"{self.img_id}/full/full/0/default.jpg"

    @property
    def dl_filename(self):
        return f"{self.parent.dir}/{self.seq}.jpg"

    def download_image(self):
        print(f"Downloading {self.url}")
        # NOTE the stream=True parameter below
        with requests.get(self.url, stream=True) as r:
            with open(self.dl_filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        return self.dl_filename

    @property
    def is_downloaded(self):
        return path.exists(self.dl_filename)


def main():
    if sys.version_info < (3, 0):
        sys.exit("This program requires python version 3.0 or later")

    # Options and arguments
    p = optparse.OptionParser(
        description="IIIF Image API Level-0 static file generator",
        usage="usage: %prog [options] file (-h for help)",
    )

    p.add_option(
        "--destination",
        "-d",
        default=".",
        action="store",
        help="Destination directory for tiles",
    )

    (opt, sources) = p.parse_args()

    man = Manifest(url=sources[0], dest_dir=opt.destination)
    man.pull_images()


if __name__ == "__main__":
    main()
