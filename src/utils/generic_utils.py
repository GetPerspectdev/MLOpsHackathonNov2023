from typing import List, Any, Dict
import os
import json
from src.utils.schema import Statement


def read_json(paths: List[str]) -> List[Dict[Any, Any]]:
    """
    Load a list of json files from the given paths.
    :param paths:
    :return:
    """
    json_objects = list()
    for path in paths:
        with open(path, 'r') as file:
            json_objects.append(json.load(file))
    return json_objects

def load_json_paths(folder: str):
    """
    Load all json files from the given folder.
    :param folder:
    :return:
    """
    json_files = [folder + os.sep + file for file in os.listdir(folder) if file.endswith(".json")]
    return json_files


def combine_conversations(word_level_conversation: List[Dict[Any, Any]]) -> List[Statement]:
    """
    Combine the given word conversations into a single conversation.
    :param word_level_conversation:
    :return:
    """
    statement_level_conversation = list()
    for statement in word_level_conversation:
        speaker = statement['speaker']
        words = statement['words']
        start_time = float(words[0]['start_timestamp'])
        end_time = float(words[-1]['end_timestamp'])

        time_spoken = end_time - start_time
        text = ' '.join([word['text'] for word in words])
        # TODO: Add punctuation to the end of the sentences.
        cur_statement = Statement(speaker, text, time_spoken)
        statement_level_conversation.append(cur_statement)
    return statement_level_conversation

def edit_save_path(path: str) -> str:
    """
    Edit the save path to be more readable.
    :param path:
    :return:
    """
    path = path[:-5]
    path += '_processed.csv'
    return path
