# -*- coding: utf-8 -*-

# import modules
import os
import time
import json

# typing
from typing import Dict, Tuple

# pathlib
from pathlib import Path

'''
Clean output format

'''
def sanitize_output_path(output: str) -> str:
    '''
    Ensures the given path uses forward slashes and does not end with a slash.

    :param output: The original directory path.
    :return: A sanitized directory path with forward slashes and no
        trailing slash.
    '''
    # create a Path object and normalize the path
    path = Path(output)

    # path with the correct separators for the current OS
    output = str(path.as_posix())

    # remove any trailing slashes
    output = output.rstrip('/')

    return output

'''
Get items and keys from search results entries

'''
def get_items_from_search_results(entry: Dict) -> Tuple:
    '''
    Extracts and processes specific fields from a data entry.

    :param entry: A dictionary containing the data entry.
    :return: A tuple containing the extracted and processed values for the
        fields.
    '''
    return (
        entry.get('source', None),
        entry.get('title', None),
        entry.get('snippet', None),
        entry.get('link', None),
        entry.get('thumbnail', None),
        entry.get('video_link', None),
        ', '.join(entry.get('snippet_highlighted_words', [])) if entry.get(
          'snippet_highlighted_words'  
        ) else None,
        entry.get('displayed_link', None)
    )

'''
Get items and keys from images results entries

'''
def get_items_from_images_results(entry: Dict) -> Tuple:
    '''
    '''
    return (
        entry.get('source', None),
        entry.get('title', None),
        entry.get('link', None),
        entry.get('thumbnail', None)
    )

'''
Save raw data response in a JSON file

'''
def save_raw_data(output: str, result_type: str, data: Dict) -> None:
    '''
    Saves the raw data response from SerpAPI in a JSON file.

    :param output: The directory path where the raw data should be saved.
    :param result_type: Type of SerpAPI response: 'search_result' or
        'images_result'
    :param data: The raw data response from SerpAPI to be saved.
    '''
     # create the directory structure if it does not exist
    folder = f'{output}/raw_data/{result_type}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # create a timestamp for the file name
    stamp = int(time.time())

    # convert the data to a JSON string
    obj = json.dumps(data, ensure_ascii=False, indent=2)

    # write the JSON string to a file
    file_path = f'{folder}/{result_type}_{stamp}.json'
    with open(file_path, encoding='utf-8', mode='w') as writer:
        writer.write(obj)

