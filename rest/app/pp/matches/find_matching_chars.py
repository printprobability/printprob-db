import json
import re
from glob import glob
import os
from django.db.models import Q
import logging
import subprocess
from .. import serializers, models
from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile

JSON_OUTPUT_DIR = '/ocean/projects/hum160002p/shared/ocr_results/json_output'


def _get_immediate_subdirectories(a_dir, starting_with=None):
    all_match_directories = os.listdir(a_dir)
    return [name for name in all_match_directories
            if os.path.isdir(os.path.join(a_dir, name)) and (starting_with is None or name.startswith(starting_with))]


def _find_character_for_path(path):
    # Incoming path is of the format -
    # .../rroberts_R6026_uscu_2_kingsloo1699-0042_page1rline13_char23_G_uc_aligned.tif
    split_path = path.split('/')
    final_part = split_path[len(split_path) - 1]
    char_path = final_part.split('_aligned', 1)[0]
    split_parts = final_part.split('-', 1)
    grep_part = final_part.split('_aligned')[0]
    book_string = split_parts[0] + '_color'
    json_output_folder = os.path.join(JSON_OUTPUT_DIR, book_string)
    json_file = f"{json_output_folder}/chars.json"
    grep_command = f"grep -A1 {grep_part} {json_file} | grep -v {grep_part}"
    try:
        proc = subprocess.Popen(grep_command, stdout=subprocess.PIPE, stderr=None, shell=True)
        matched_id_line, err = proc.communicate()
        if matched_id_line is not None and matched_id_line != '':
            character_id = (str(matched_id_line).split(':'))[1].split(',')[0].replace('"', '').strip()
            return {'name': char_path, 'id': character_id}
    except Exception as err:
        logging.error({"Error finding character: ", path})
        logging.error(err)
        return {'name': char_path, 'id': None}


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


def _serialize_char(request, character):
    obj = None
    try:
        obj = models.Character.objects.get(id=character['id'])
    except models.Character.DoesNotExist as err:
        logging.error({"Error in finding matched character ": character['id']})
        logging.error(err)
    if obj is None:
        return {'name': character['name'], 'obj': None}
    serializer = serializers.CharacterMatchSerializer(obj, context={'request': request})
    return {'name': character['name'], 'obj': json.loads(json.dumps(serializer.data))}


def get_matched_characters(request, csv_file, limit, offset):
    result = []
    limit_count = 0
    idx = 0
    serialized_result = []
    with open(csv_file, 'r') as csvfile:
        for line in csvfile:
            # continue till offset
            if idx < offset:
                idx += 1
                continue
            row = line.split(',')
            if len(row) == 21:
                last_char_index = 11
                last_distance_index = 21
            if len(row) == 41:
                last_char_index = 21
                last_distance_index = 41
            matched_image_characters = [_find_character_for_path(image)
                                        for image in row[0:last_char_index]]
            distances = row[last_char_index:last_distance_index]
            if matched_image_characters[0] is not None:
                limit_count += 1
                result.append({})
                result[limit_count-1]['target'] = matched_image_characters[0]
                result[limit_count-1]['matches'] = matched_image_characters[1:last_char_index]
                result[limit_count-1]['distances'] = distances
                # have we got all the rows we wanted ?
                if limit_count == limit:
                    break
            idx += 1
        for idx, res in enumerate(result):
            res['target'] = _serialize_char(request, res['target'])
            if res['target'] is None:
                continue
            res['matches'] = [_serialize_char(request, match) for match in res['matches']]
            serialized_result.append({})
            serialized_result[idx] = res
    return serialized_result
