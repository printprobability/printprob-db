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
            return character_id
    except:
        logging.error({"Error finding character: ", path})
        return None


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


def _serialize_char(request, obj):
    if obj is None:
        return {}
    serializer = serializers.CharacterMatchSerializer(obj, context={'request': request})
    return json.loads(json.dumps(serializer.data))


def get_matched_characters(request, csv_file, limit, offset):
    result = []
    limit_count = 0
    idx = 0
    with open(csv_file, 'r') as csvfile:
        for line in csvfile:
            # continue till offset
            if idx < offset:
                idx += 1
                continue
            row = line.split(',')
            matched_image_characters = [_find_character_for_path(image)
                                        for image in row[0:11]]
            if matched_image_characters[0] is not None:
                limit_count += 1
                result.append({})
                result[idx]['target'] = matched_image_characters[0]
                result[idx]['matches'] = matched_image_characters[1:11]
                # have we got all the rows we wanted ?
                if limit_count == limit:
                    break
            idx += 1
        for res in result:
            try:
                res['target'] = _serialize_char(request, models.Character.objects.get(id=res['target']))
                res['matches'] = [_serialize_char(request, models.Character.objects.get(id=match))
                                  for match in res['matches']]
                logging.info({"Done matching: ": res})
            except models.Character.DoesNotExist as err:
                logging.error({"Error in finding matched characters on row: ": idx})
                logging.error(err)

    return result
