import logging
import pandas as pd
import numpy as np
import json
from src.constants import COLUMN_WIDTHS

# configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


# functions to read and simplify json file
def _json_data_to_list(json_file):
    '''Returns the relevant entryText fields as a list of lists - grouped by entry in the json file'''
    return [[i['entryText'] for i in item['leaseschedule']['scheduleEntry']] for item in json_file]

def read_json_file(file_path):
    '''Reads the json file and stores it as a list of dictionaries'''
    try:
        with open(file_path) as f:
            json_data = json.load(f)
            return _json_data_to_list(json_data)
    except Exception as e:
        logging.error(f'Error reading JSON file: {e}', exc_info=True)
        return None


# functions for processing the data
def _remove_nulls(string_list):
    '''Removes null values from a list'''
    string_list = [i for i in string_list if not pd.isna(i)]
    return string_list

def _get_note_indexes(string_list):
    '''Reurns list of note indexes from a list of strings or None if note not found'''
    note_indexes = [i for i, s in enumerate(string_list) if isinstance(s, str) and s.startswith('NOTE')]
    return note_indexes
    
def _split_notes_from_entryText(entryText):
    '''Get the column text lines and the notes separately'''
    note_indexes = _get_note_indexes(entryText)
    if note_indexes:
        notes = entryText[note_indexes[0]:]
        entryText = entryText[0:note_indexes[0]]
    else:
        notes = []
    return entryText, notes

    
def _get_clean_notes(entryText):
    '''Returns dictionary of clean notes where one string represents one note, returns none if there are no notes'''
    entryText_note_indexes = _get_note_indexes(entryText)
    
    if not entryText_note_indexes:
        return None

    notes = entryText[entryText_note_indexes[0]:]
    note_indexes = _get_note_indexes(notes)

    if len(notes) > len(note_indexes):
        string_indexes_to_join = [i for i, s in enumerate(note_indexes) if i != s]
        for i in reversed(string_indexes_to_join):
            joined_string = ' '.join(notes[i - 1:i + 1])
            notes[i - 1:i + 1] = [joined_string]

    return {f'NOTE {index + 1}': value for index, value in enumerate(notes)}
    
def _get_clean_dict(entryText):
    '''Takes an entryText field, splits the notes from the other text and returns dictionary format column data'''
    entryText = _remove_nulls(entryText)
    entryText, notes = _split_notes_from_entryText(entryText)

    for line in entryText:
        entryTextDict = {
            k : ' '.join([line[slice(*v)].strip() for line in entryText]) for (k,v) in COLUMN_WIDTHS.items()
        }
    if notes:
        clean_notes = _get_clean_notes(notes)
        entryTextDict.update(clean_notes)
    return entryTextDict

def preprocess_data(data):
    clean_data = [_get_clean_dict(j) for i in data for j in i]
    output_dict = {index: d for index, d in enumerate(clean_data)}
    return output_dict