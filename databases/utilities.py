# -*- coding: utf-8 -*-

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
Get items and keys from data entries

'''
def get_items_from_data(entry: Dict) -> Tuple:
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