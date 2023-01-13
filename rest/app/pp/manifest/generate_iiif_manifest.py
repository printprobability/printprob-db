import os.path
from datetime import date

import logging
from iiif_prezi.factory import ManifestFactory

from django.conf import settings


def generate_iiif_manifest(book, pages, images_path, images_dir_path):
    logging.info({"Generating manifest for images path : ", images_path})
    factory = ManifestFactory()
    factory.set_base_prezi_uri(settings.IMAGE_BASEURL+images_path)
    factory.set_base_image_uri(settings.IMAGE_BASEURL+images_path)
    factory.set_base_image_dir(images_dir_path)

    manifest = factory.manifest(label=f'Manifest for book - {book.id}')
    manifest.set_metadata({"Date":  date.today()})
    manifest.viewingDirection = "left-to-right"
    seq = manifest.sequence(ident="normal", label="Normal Order")
    for page in pages:
        page_number = page.sequence
        cvs = seq.canvas(ident="page-%s" % page_number, label="Page %s" % page_number)
        cvs.set_image_annotation(page.tif.split('/')[-1], iiif=False)
    logging.info("Finished generating manifest")
    return manifest.toFile(compact=False)
