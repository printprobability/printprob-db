import os.path
from datetime import date

import logging
from iiif_prezi.factory import ManifestFactory

from django.conf import settings


def generate_iiif_manifest(book, pages, book_path):
    logging.info({"Generating manifest for book path : ", book_path})
    factory = ManifestFactory()
    factory.set_iiif_image_info(2.0, 2) # Version, ComplianceLevel
    factory.set_base_image_uri(settings.IMAGE_BASEURL)
    factory.set_base_prezi_uri(settings.IMAGE_BASEURL)
    image_dir = os.path.join(book_path, 'originals')
    logging.info({"Setting book images directory as : ", image_dir})
    factory.set_base_image_dir(image_dir)

    manifest = factory.manifest(label=f'Manifest for book - {book.id}')
    manifest.set_metadata({"Date":  date.today()})
    manifest.viewingDirection = "left-to-right"
    seq = manifest.sequence(ident="normal", label="Normal Order")
    for page in pages:
        page_number = page.sequence
        cvs = seq.canvas(ident="page-%s" % page_number, label="Page %s" % page_number)
        cvs.set_image_annotation(page.tif.split('/')[-1])
    logging.info("Finished generating manifest")
    return manifest.toFile(compact=False)
