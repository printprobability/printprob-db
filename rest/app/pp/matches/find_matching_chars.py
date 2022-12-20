import json
import re
from glob import glob
import os
import csv
from django.db.models import Q
import logging
from .. import serializers, models
from rest_framework.renderers import JSONRenderer

TOP_K_CSV_SUFFIX = '*_topk.csv'


def _get_immediate_subdirectories(a_dir, starting_with=None):
    all_match_directories = os.listdir(a_dir)
    return [name for name in all_match_directories
            if os.path.isdir(os.path.join(a_dir, name)) and (starting_with is None or name.startswith(starting_with))]


def _find_character_for_path(path, json_file):
    # Incoming path is of the format -
    # .../rroberts_R6026_uscu_2_kingsloo1699-0042_page1rline13_char23_G_uc_aligned.tif
    split_path = path.split('/')
    final_part = split_path[len(split_path)-1]
    grep_part = final_part.split('_aligned')[0]
    for line in json_file:
        if re.search(grep_part, line):
            next_line = next(json_file)
            character_id = next_line.split('"')[3]
            logging.info({"Found character": character_id})
            return character_id


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


def get_matched_characters(request, character_class_dir, json_output_folder):
    topk_csv_files = list(glob(os.path.join(character_class_dir, TOP_K_CSV_SUFFIX)))
    logging.info(topk_csv_files)
    result = []
    if len(topk_csv_files) > 0:
        topk_csv_file = topk_csv_files[0]
        with open(f"{json_output_folder}/chars.json","r") as json_file:
            with open(topk_csv_file, newline='') as csvfile:
                topk_reader = csv.reader(csvfile, delimiter=',')
                for idx, row in enumerate(topk_reader):
                    target_image = row[0]
                    target_character = _find_character_for_path(target_image, json_file)
                    result.append({})
                    if target_character is None:
                        continue
                    matched_images = row[1:10]
                    result[idx]['target'] = target_character
                    matched_image_characters = [_find_character_for_path(image, json_file)
                                                for image in matched_images]
                    result[idx]['matches'] = matched_image_characters
        for res in result:
            res['target'] = models.Character.objects.get(id=res['target'])
            res['matches'] = [models.Character.objects.get(id=match) for match in res['matches']]
    serializer = serializers.CharacterMatchSerializer(result, context={'request': request})
    return JSONRenderer().render(serializer.data)
