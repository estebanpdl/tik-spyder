# -*- coding: utf-8 -*-

# import modules
import os

# typing
from typing import Dict

# import submodules
from configparser import ConfigParser
from datetime import datetime

'''
Get configuration attributes

'''
def get_config_attrs():
    '''
    '''
    path = './config/config.ini'

    # config parser
    config = ConfigParser()
    config.read(path)

    # SerpAPI credentials
    attrs = config['SerpAPI Key']
    return dict(attrs)

'''
Verify date format

'''
def is_valid_date(date_str: str) -> bool:
    '''
    Verifies if the given date string is in the format YYYY-MM-DD.

    :param date_str: The date string to verify.
    :return: True if the date string is valid, False otherwise.
    '''
    try:
        # Attempt to parse the date string with the expected format
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        # If a ValueError is raised, the format is incorrect
        return False

def verify_date_argument(args: Dict, key: str) -> None:
    '''
    Verifies that a date argument in args is correctly formatted.

    :param args: Dictionary containing command line arguments and options.
    :param key: The key in args to check for a valid date.
    :raises ValueError: If the date is not in the correct format.
    '''
    if key in args:
        if not is_valid_date(args[key]):
            raise ValueError(
                f"The date for '{key}' argument is not in the correct "
                "format. Use this format: YYYY-MM-DD."
            )

'''
Create output data path

'''
def create_output_data_path(path: str) -> None:
    '''
    Creates the specified directory path if it does not already exist.

    :param path: The directory path to create.
    :return: None
    '''
    if not os.path.exists(path):
        os.makedirs(path)

