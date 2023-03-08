import logging

from .. import models


def save_matched_characters_in_db(book, matched_chars):
    for matched_char in matched_chars:
        if matched_char is not None and matched_char['query'] is not None:
            try:
                query = models.Character.objects.get(id=matched_char['query'])
                existing = models.CharacterMatch.objects.filter(book=book, query=query).first()
                if existing is None:
                    if matched_char['matches'] is None or len(matched_char['matches']) == 0:  # nothing to save
                        continue
                    logging.info("Saving new match")
                    models.CharacterMatch.objects.create(book=book, query=query, matches=matched_char['matches'])
                else:
                    logging.info({"Existing:": existing})
                    if matched_char['matches'] is None or len(matched_char['matches']) == 0:
                        logging.info("Deleting existing match")
                        existing.delete()
                    else:
                        logging.info("Updating existing match")
                        existing.matches = matched_char['matches']
                        existing.save()
            except Exception as err:
                raise err
