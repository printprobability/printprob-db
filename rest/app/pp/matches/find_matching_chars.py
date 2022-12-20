import json
from glob import glob
import os
import csv
from django.db.models import Q
import logging
from .. import serializers, models
from rest_framework.renderers import JSONRenderer

TOP_K_CSV_SUFFIX = '*_topk.csv'
JSON_OUTPUT_DIR = '/ocean/projects/hum160002p/shared/ocr_results/json_output'


def _get_immediate_subdirectories(a_dir, starting_with=None):
    all_match_directories = os.listdir(a_dir)
    return [name for name in all_match_directories
            if os.path.isdir(os.path.join(a_dir, name)) and (starting_with is None or name.startswith(starting_with))]


def _find_character_for_path(request, path, characters):
    # Incoming path is of the format -
    # .../rroberts_R6026_uscu_2_kingsloo1699-0042_page1rline13_char23_G_uc_aligned.tif
    split_path = path.split('/')
    final_part = split_path[len(split_path)-1]
    grep_part = final_part.split('_aligned')[0]
    character = [char for char in characters if grep_part in str(char['filename'])]
    if character is None or len(character) == 0:
        return None
    if len(character) > 1:
        logging.error({"found multiple characters matching path": path})
        return None
    logging.info({"Found character": character[0]})
    return character[0]['id']


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
    characters = None
    if len(topk_csv_files) > 0:
        topk_csv_file = topk_csv_files[0]
        with open(topk_csv_file, newline='') as csvfile:
            topk_reader = csv.reader(csvfile, delimiter=',')
            for idx, row in enumerate(topk_reader):
                target_image = row[0]
                if characters is None:
                    split_path = target_image.split('/')
                    final_part = split_path[len(split_path)-1]
                    split_parts = final_part.split('-', 1)
                    book_string = split_parts[0]+'_color'
                    json_output_folder = os.path.join(JSON_OUTPUT_DIR, book_string)
                    characters = json.load(open(f"{json_output_folder}/chars.json", "r"))[
                        "chars"
                    ]
                    logging.info({"reading characters:": len(characters)})
                target_character = _find_character_for_path(request, target_image, characters)
                result.append({})
                if target_character is None:
                    continue
                matched_images = row[1:10]
                result[idx]['target'] = target_character
                matched_image_characters = [_find_character_for_path(request, image, characters)
                                            for image in matched_images]
                result[idx]['matches'] = matched_image_characters
        for res in result:
            res['target'] = models.Character.objects.get(id=res['target'])
            for idx, match in enumerate(res['matches']):
                res['target']['matches'][idx] = models.Character.objects.get(id=res['target']['matches'][idx])
    serializer = serializers.CharacterMatchSerializer(result, context={'request': request})
    return JSONRenderer().render(serializer.data)
