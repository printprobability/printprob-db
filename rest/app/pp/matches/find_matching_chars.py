from glob import glob
import os
import csv
from django.db.models import Q
import logging
from .. import serializers
from rest_framework.renderers import JSONRenderer

TOP_K_CSV_SUFFIX = '*_topk.csv'


def _get_immediate_subdirectories(a_dir, starting_with=None):
    all_match_directories = os.listdir(a_dir)
    return [name for name in all_match_directories
            if os.path.isdir(os.path.join(a_dir, name)) and (starting_with is None or name.startswith(starting_with))]


def _find_character_for_path(request, path, characters):
    # Incoming path is of the format -
    # .../rroberts_R6026_uscu_2_kingsloo1699-0042_page1rline13_char23_G_uc_aligned.tif
    split_path = path.split('/')
    final_part = split_path[len(split_path)-1]
    split_parts = final_part.split('-', 1)
    sequence_parts = split_parts[1].split('_')
    page_number = int(sequence_parts[0])
    line_number = int(sequence_parts[1].split('line')[1])
    character_number = int(sequence_parts[2].split('char')[1]) # get the character sequence number
    character_class = sequence_parts[3] + '_' + sequence_parts[4] # character class e.g. G_uc
    qs_filter = (Q(line__page__sequence=page_number) &
                 Q(line__sequence=line_number) &
                 Q(sequence=character_number) & Q(character_class=character_class))
    character = characters.filter(qs_filter)
    if character is None or len(character) == 0:
        return None
    if len(character) > 1:
        logging.error({"found multiple characters matching path": path})
        return None
    serializer = serializers.CharacterMatchSerializer(character[0], context={'request': request})
    return JSONRenderer().render(serializer.data)


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


def get_matched_characters(request, character_class_dir, characters):
    topk_csv_files = list(glob(os.path.join(character_class_dir, TOP_K_CSV_SUFFIX)))
    logging.info(topk_csv_files)
    result = []
    if len(topk_csv_files) > 0:
        topk_csv_file = topk_csv_files[0]
        with open(topk_csv_file, newline='') as csvfile:
            topk_reader = csv.reader(csvfile, delimiter=',')
            for idx, row in enumerate(topk_reader):
                target_image = row[0]
                target_character = _find_character_for_path(request, target_image, characters)
                result.append({})
                if target_character is None:
                    continue
                matched_images = row[1:10]
                result[idx]['target'] = target_character
                matched_image_characters = [_find_character_for_path(request, image, characters)
                                            for image in matched_images]
                result[idx]['matches'] = matched_image_characters
    return result
