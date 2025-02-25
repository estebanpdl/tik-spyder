# -*- coding: utf-8 -*-

# import modules
import time

# import argparse
from argparse import (
	ArgumentParser, RawTextHelpFormatter, SUPPRESS
)

# import utils
from utils import get_config_attrs, verify_date_argument, \
    create_output_data_path

# SerpAPI collector
from serpapi_client import SerpAPICollector

# video downloader
from media_handlers import VideoDownloader

if __name__ == '__main__':

    '''
    Arguments

    '''
    formatter = lambda prog: RawTextHelpFormatter(
        prog,
        indent_increment=2,
        max_help_position=52,
        width=None
    )

    parser = ArgumentParser(
        prog='TikSpyder',
        description='Command Line Arguments.',
        formatter_class=formatter,
        add_help=False
    )

    # help arguments
    help_arguments = parser.add_argument_group('Help options')
    help_arguments.add_argument(
        '-h',
        '--help',
        action='help',
        default=SUPPRESS,
        help='Show this help message and exit.'
    )

    # SerpAPI arguments
    serpapi_arguments = parser.add_argument_group('SerpAPI options')

    ''' query '''
    serpapi_arguments.add_argument(
        '--q',
        type=str,
        required=False,
        metavar='',
        help='The search term of phrase for which to retrieve TikTok data.'
    )

    ''' user '''
    serpapi_arguments.add_argument(
        '--user',
        type=str,
        required=False,
        metavar='',
        help='Specify a TikTok user to search for videos from.'
    )

    ''' google domain '''
    serpapi_arguments.add_argument(
        '--google-domain',
        type=str,
        required=False,
        default='google.com',
        metavar='',
        help='Defines the Google domain to use. It defaults to google.com.'
    )

    ''' gl > country '''
    serpapi_arguments.add_argument(
        '--gl',
        type=str,
        required=False,
        metavar='',
        help=(
            "Defines the country to use for the search. Two-letter country "
            "code."
        )
    )

    ''' hl > language '''
    serpapi_arguments.add_argument(
        '--hl',
        type=str,
        required=False,
        metavar='',
        help=(
            "Defines the language to use for the search. Two-letter language "
            "code."
        )
    )

    ''' cr > multiple countries '''
    serpapi_arguments.add_argument(
        '--cr',
        type=str,
        required=False,
        metavar='',
        help='Defines one or multiple countries to limit the search to.'
    )

    ''' lr > one or multiple languages '''
    serpapi_arguments.add_argument(
        '--lr',
        type=str,
        required=False,
        metavar='',
        help='Defines one or multiple languages to limit the search to.'
    )

    ''' depth > defines number of iterations for related content '''
    serpapi_arguments.add_argument(
        '--depth',
        type=int,
        required=False,
        default=3,
        metavar='',
        help='Depth of iterations to follow related content links.'
    )

    # Google advanced search arguments
    google_advanced_search_arguments = parser.add_argument_group(
        'Google advanced search options'
    )

    ''' search for posts before a given date '''
    google_advanced_search_arguments.add_argument(
        '--before',
        type=str,
        required=False,
        metavar='',
        help=(
            "Limit results to posts published before the specified date. "
            "Format: YYYY-MM-DD."
        )
    )

    ''' search for posts after a given date '''
    google_advanced_search_arguments.add_argument(
        '--after',
        type=str,
        required=False,
        metavar='',
        help=(
            "Limit results to posts published after the specified date. "
            "Format: YYYY-MM-DD."
        )
    )

    # optional arguments
    optional_arguments = parser.add_argument_group(
        'Optional arguments and parameters'
    )

    ''' output '''
    optional_arguments.add_argument(
        '-o',
        '--output',
        type=str,
        required=False,
        default=f'./data/{int(time.time())}',
        metavar='',
        help=(
            "Specify the output directory path. If not provided, data is "
            "saved in a timestamped subdirectory within the './data/' "
            "directory."
        )
    )
    
    ''' max workers > maximum number of threads '''
    optional_arguments.add_argument(
        '-w',
        '--max-workers',
        type=int,
        required=False,
        metavar='',
        help=(
            "Specify the maximum number of threads to use for downloading "
            "TikTok videos."
        )
    )

    ''' download TikTok results '''
    optional_arguments.add_argument(
        '-d',
        '--download',
        action='store_true',
        required=False,
        help='Specify whether to download TikTok videos from SerpAPI response.'
    )

    ''' apify integration '''
    optional_arguments.add_argument(
        '--apify',
        action='store_true',
        required=False,
        help='Specify whether to use Apify integration.'
    )

    optional_arguments.add_argument(
        '--oldest-post-date',
        type=str,
        required=False,
        metavar='',
        help=(
            "Filter posts newer than the specified date. "
            "Format: YYYY-MM-DD."
        )
    )

    optional_arguments.add_argument(
        '--newest-post-date',
        type=str,
        required=False,
        metavar='',
        help=(
            "Filter posts older than the specified date. "
            "Format: YYYY-MM-DD."
        )
    )

    # parse arguments
    args = vars(parser.parse_args())

    # validate that either a username or search query was provided
    if args['user'] is None and args['q'] is None:
        raise ValueError('Either --user or --q must be provided.')

    # merging SerpAPI configuration attrs with the existing arguments
    config_attrs = get_config_attrs()
    args = {**args, **config_attrs}

    # verify provided dates
    for date_key in ['before', 'after']:
        if args[date_key] is not None:
            verify_date_argument(args, date_key)
    
    # Start process
    log_text = f'''
    > Starting program at: {time.ctime()}

    '''
    print ('\n\n' + ' '.join(log_text.split()).strip())

    # create the output data path if not exists
    output = args['output']
    create_output_data_path(output)

    # # SerpAPICollector instance
    serp_api_collector = SerpAPICollector(args=args)

    # SerpAPI call
    serp_api_collector.collect_search_data()

    # read SQL database and generate a csv file
    serp_api_collector.generate_data_files()

    # download videos
    if args['download']:
        downloader = VideoDownloader(output=output)

        # get tiktok urls
        collected_videos = serp_api_collector.get_collected_videos()

        # start download
        downloader.start_download(urls=collected_videos)

    # End process
    log_text = f'''
    > Ending program at: {time.ctime()}

    '''
    print ('\n\n' + ' '.join(log_text.split()).strip())
