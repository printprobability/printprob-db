from .. import models


def save_matched_characters_in_db(book, matched_chars):
    for matched_char in matched_chars:
        if matched_char['query'] is not None and matched_char['match'] is not None:
            try:
                query = models.Character.objects.get(id=matched_char['query'])
                match = models.Character.objects.get(id=matched_char['match'])
                models.CharacterMatch.objects.create(book=book, query=query, match=match)
            except Exception as err:
                raise err
