import os.path
from datetime import date
import ssl

import logging
from iiif_prezi.factory import ManifestFactory

from django.conf import settings

from rest.app.pp.views import BASE_PATH


def _fix_originals_path(input_path):
    to_replace = 'lines_color'
    if 'pages_color' in input_path:
        to_replace = 'pages_color'
    originals_path = input_path.replace(to_replace, 'originals_precrop')
    if not os.path.exists(originals_path):
        originals_path = input_path.replace(to_replace, 'originals')
        if not os.path.exists(originals_path):
            return None
    return originals_path


def generate_iiif_manifest(book, pages, images_dir_path):
    page_images = False
    if 'pages_color' in images_dir_path:
        page_images = True
    images_dir_path = _fix_originals_path(images_dir_path)
    images_path = images_dir_path.split(BASE_PATH)[1]
    if images_path is None or images_dir_path is None:
        logging.error({ "Image path not found": images_dir_path})
        return None

    logging.info({"Generating manifest for images path : ", images_path})
    logging.info({"Setting directory on disk for images : ", images_dir_path})
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
        original_image = page.tif.split('/')[-1]
        if not page_images:
            original_image = original_image.split('_page')[0]+'.tif'
        cvs.set_image_annotation(original_image, iiif=True)
    logging.info("Finished generating manifest")
    ssl._create_default_https_context = ctx
    return manifest.toString(compact=False)
