import json
import logging
import os

from .. import serializers, models

JSON_OUTPUT_DIR = '/ocean/projects/hum160002p/shared/ocr_results/json_output'


def _get_immediate_subdirectories(a_dir, starting_with=None):
    all_match_directories = os.listdir(a_dir)
    absolute_path_directories = [os.path.join(a_dir, name) for name in all_match_directories]
    absolute_path_directories.sort(key=os.path.getmtime, reverse=True)
    result = []
    for f in absolute_path_directories:
        file_name = os.path.split(f)[1]
        if os.path.isdir(f) and (starting_with is None or file_name.startswith(starting_with)):
            result += [file_name]
    return result


def get_match_directories(matches_path):
    matches = []
    all_match_directories = _get_immediate_subdirectories(matches_path, "matching_output_")
    for idx, match_dir in enumerate(all_match_directories):
        matches.append({})
        matches[idx]['dir'] = match_dir
        character_classes = _get_immediate_subdirectories(os.path.join(matches_path, match_dir))
        if len(character_classes) == 0:
            continue
        matches[idx]['character_classes'] = character_classes
    return matches


def _serialize_char(request, character_id):
    obj = None
    try:
        obj = models.Character.objects.get(id=character_id)
    except models.Character.DoesNotExist as err:
        logging.error({"Error in finding matched character ": character_id})
        logging.error(err)
    if obj is None:
        return None
    serializer = serializers.CharacterMatchSerializer(obj, context={'request': request})
    return json.loads(json.dumps(serializer.data))


def get_matched_characters(request, csv_file, limit, offset):
    result = []
    limit_count = 0
    with open(csv_file, 'r') as csvfile:
        idx = 0
        for line in csvfile:
            # continue till offset
            if idx < offset:
                idx += 1
                continue
            row = line.split(',')
            # rows have [query_uuids] + topk_uuid + dists
            # e.g., for top 10:
            # 11 + 10 = 21 -> 11
            # for top 20:
            # 21 + 20 = 41 -> 21
            # for top 5:
            # 6 + 5 = 11 -> 5
            last_char_index = len(row) // 2 + 1
            last_distance_index = len(row)
            limit_count += 1
            result.append({})
            result[limit_count - 1]['target'] = _serialize_char(request, row[0])
            result[limit_count - 1]['matches'] = [_serialize_char(request, match) for match in row[1:last_char_index]]
            result[limit_count - 1]['distances'] = row[last_char_index:last_distance_index]
            # have we got all the rows we wanted ?
            if limit_count == limit:
                break
            idx += 1
    return result


def existing_matched_characters(book, queries):
    result = []
    for query in queries:
        existing = models.CharacterMatch.objects.filter(book=book, query=query).first()
        if existing is not None:
            result.append(existing)
    return result
