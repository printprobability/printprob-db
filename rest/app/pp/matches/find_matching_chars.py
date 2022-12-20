import json
import re
from glob import glob
import os
import csv
from django.db.models import Q
import logging
import subprocess
from .. import serializers, models
from rest_framework.renderers import JSONRenderer
from subprocess import check_call, STDOUT
from tempfile import NamedTemporaryFile

TOP_K_CSV_SUFFIX = '*_topk.csv'
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
        with NamedTemporaryFile() as f:
            check_call(["/bin/sh", "-c", grep_command], stdout=f, stderr=STDOUT)
            f.seek(0)
            matched_id_line = f.read()
            if matched_id_line is not None:
                character_id = (str(matched_id_line).split(':'))[1].split(',')[0].replace('"', '').strip()
                logging.info({"Found character": character_id})
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


def get_matched_characters(request, character_class_dir):
    topk_csv_files = list(glob(os.path.join(character_class_dir, TOP_K_CSV_SUFFIX)))
    logging.info(topk_csv_files)
    result = []
    if len(topk_csv_files) > 0:
        topk_csv_file = topk_csv_files[0]
        with open(topk_csv_file, newline='') as csvfile:
            topk_reader = csv.reader(csvfile, delimiter=',')
            for idx, row in enumerate(topk_reader):
                logging.info(f"Fetching characters for row number: {idx+1}")
                matched_image_characters = [_find_character_for_path(image)
                                            for image in row[0:10]]
                result.append({})
                result[idx]['target'] = matched_image_characters[0]
                result[idx]['matches'] = matched_image_characters[1:10]
        for res in result:
            res['target'] = models.Character.objects.get(id=res['target'])
            res['matches'] = [models.Character.objects.get(id=match) for match in res['matches']]
    serializer = serializers.CharacterMatchSerializer(result, context={'request': request})
    return JSONRenderer().render(serializer.data)
