# -*- coding: utf-8 -*-

# import modules
import os

# typing
from typing import Dict

# import submodules
from configparser import ConfigParser
from datetime import datetime

def get_project_root():
    """Get the project root directory."""
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return current_dir

'''
Get configuration attributes

'''
def get_config_attrs(config_dir=None) -> Dict:
    '''
    Retrieves configuration attributes from configuration files.

    :param config_dir: Optional path to the config directory.
                       If None, uses the default path.
    :return: A dictionary containing the SerpAPI and Apify credentials.
    '''
    if config_dir is None:
        project_root = get_project_root()
        config_dir = os.path.join(project_root, 'config')
    
    path = os.path.join(config_dir, 'config.ini')

    # config parser
    config = ConfigParser()
    config.read(path)

    # Get credentials from both sections
    credentials = {}
    
    # SerpAPI credentials
    if 'SerpAPI Key' in config:
        credentials.update(dict(config['SerpAPI Key']))
    
    # Apify credentials
    if 'Apify Token' in config:
        credentials.update(dict(config['Apify Token']))
    
    return credentials

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

