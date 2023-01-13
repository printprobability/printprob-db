from .. import models
import logging


def save_matched_characters_in_db(book, matched_chars):
    for matched_char in matched_chars:
        if matched_char is not None and matched_char['query'] is not None:
            try:
                query = models.Character.objects.get(id=matched_char['query'])
                existing = models.CharacterMatch.objects.filter(book=book, query=query).first()
                if existing is None:
                    if matched_char['match'] is None: # nothing to save
                        continue
                    logging.info("Saving new match")
                    match = models.Character.objects.get(id=matched_char['match'])
                    models.CharacterMatch.objects.create(book=book, query=query, match=match)
                else:
                    logging.info({"Existing:": existing})
                    if matched_char['match'] is None:
                        logging.info("Deleting existing match")
                        existing.delete()
                    else:
                        match = models.Character.objects.get(id=matched_char['match'])
                        logging.info("Updating existing match")
                        existing.match = match
                        existing.save()
            except Exception as err:
                raise err