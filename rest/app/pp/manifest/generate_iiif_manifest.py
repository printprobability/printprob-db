import os.path
from datetime import date
import ssl

import logging
from iiif_prezi.factory import ManifestFactory

from django.conf import settings


def generate_iiif_manifest(book, pages, images_path, images_dir_path):
    logging.info({"Generating manifest for images path : ", images_path})
    factory = ManifestFactory()
    factory.set_iiif_image_info(2.0, 2) # Version, ComplianceLevel
    factory.set_base_prezi_uri(settings.IMAGE_BASEURL+images_path)
    factory.set_base_image_uri(settings.IMAGE_BASEURL+images_path)
    factory.set_base_image_dir(images_dir_path)

    manifest = factory.manifest(label=f'Manifest for book - {book.id}')
    manifest.set_metadata({"Date":  str(date.today())})
    manifest.viewingDirection = "left-to-right"
    manifest.viewingHint = "paged"
    manifest.description = "manifest"
    seq = manifest.sequence(ident="normal", label="Normal Order")
    ctx = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    for i, page in enumerate(pages):
        cvs = seq.canvas(ident="page-%s" % i, label="Page %s" % i)
        cvs.set_image_annotation(page.tif.split('/')[-1], iiif=True)
    logging.info("Finished generating manifest")
    ssl._create_default_https_context = ctx
    return manifest.toString(compact=False)
