# -*- coding: utf-8 -*-

# import modules
import time
import os

# import argparse
from argparse import (
	ArgumentParser, RawTextHelpFormatter, SUPPRESS
)

# import utils
from utils import get_config_attrs, verify_date_argument, \
    create_output_data_path, get_project_root

# TikTok data collector
from data_collectors import TikTokDataCollector

# video downloader
from media_handlers import VideoDownloader, RequestSession

def main():
    # Get current working directory (where command was executed)
    execution_dir = os.getcwd()
    
    # Get project root directory (where the package is installed)
    project_root = get_project_root()
    
    # Set up project paths for later use instead of changing directories
    project_paths = {
        'root': project_root,
        'config': os.path.join(project_root, 'config'),
        'execution': execution_dir
    }
    
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

    ''' tag '''
    serpapi_arguments.add_argument(
        '--tag',
        type=str,
        required=False,
        metavar='',
        help='Specify a TikTok tag to search for videos from.'
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

    ''' safe > adult content filter '''
    serpapi_arguments.add_argument(
        '--safe',
        type=str,
        required=False,
        default='active',
        choices=['active', 'off'],
        metavar='',
        help='Level of filtering for adult content. Options: active (default), off'
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

    # Apify optional arguments
    apify_arguments = parser.add_argument_group(
        'Optional Apify arguments'
    )

    ''' apify integration '''
    apify_arguments.add_argument(
        '--apify',
        action='store_true',
        required=False,
        help='Specify whether to use Apify integration.'
    )

    apify_arguments.add_argument(
        '--oldest-post-date',
        type=str,
        required=False,
        metavar='',
        help=(
            "Filter posts newer than the specified date. "
            "Format: YYYY-MM-DD."
        )
    )

    apify_arguments.add_argument(
        '--newest-post-date',
        type=str,
        required=False,
        metavar='',
        help=(
            "Filter posts older than the specified date. "
            "Format: YYYY-MM-DD."
        )
    )

    # optional arguments
    optional_arguments = parser.add_argument_group(
        'Optional arguments and parameters'
    )

    ''' use tor '''
    optional_arguments.add_argument(
        '--use-tor',
        action='store_true',
        required=False,
        help='Specify whether to use Tor for downloading TikTok videos.'
    )

    ''' download TikTok results '''
    optional_arguments.add_argument(
        '-d',
        '--download',
        action='store_true',
        required=False,
        help='Specify whether to download TikTok videos from SerpAPI and Apify.'
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
            "TikTok videos and extracting keyframes."
        )
    )

    ''' output '''
    optional_arguments.add_argument(
        '-o',
        '--output',
        type=str,
        required=False,
        default=f'./tikspyder-data/{int(time.time())}',
        metavar='',
        help=(
            "Specify output directory path. If not provided, data is "
            "saved in the current working directory in a folder named "
            "tikspyder-data"
        )
    )

    # parse arguments
    args = vars(parser.parse_args())

    # validate that either a query, username or tag was provided
    if all(arg is None for arg in [args['user'], args['q'], args['tag']]):
        raise ValueError('Either --user, --q or --tag must be provided.')
    
    # raise error if both user and tag are provided
    if args['user'] and args['tag']:
        raise ValueError('Both --user and --tag were provided. Only one can be used.')
    
    # merging SerpAPI configuration attrs with the existing arguments
    config_attrs = get_config_attrs(project_paths['config'])
    args = {**args, **config_attrs}

    # verify provided dates
    for date_key in ['before', 'after']:
        if args[date_key] is not None:
            verify_date_argument(args, date_key)
    
    # start process
    log_text = f'''
    > Starting program at: {time.ctime()}

    '''
    print ('\n\n' + ' '.join(log_text.split()).strip())

    # create the output data path if not exists
    output = args['output']
    create_output_data_path(output)

    # TikTokDataCollector instance
    collector = TikTokDataCollector(args=args)

    # TikTok data collection call
    collector.collect_search_data()

    # read SQL database and generate csv file
    collector.generate_data_files()

    # download videos
    if args['download']:
        print ('')
        print ('-' * 30)
        print ('> Downloading videos...')

        # get tiktok urls
        collected_videos = collector.get_collected_videos()

        if collected_videos:
            print (f'\n> Found {len(collected_videos)} videos to download.')

            # define max workers
            max_workers = args['max_workers'] if args['max_workers'] else 5
            downloader = VideoDownloader(output=output, use_tor=args['use_tor'])

            # start download
            downloader.start_download(urls=collected_videos, max_workers=max_workers)
        else:
            print ('\n> Search results did not return any videos to download.')
        
        # extract keyframes
        print ('\n')
        print ('-' * 30)
        print ('Extracting keyframes...')
        request_session = RequestSession()

        # define max workers
        max_workers = args['max_workers'] if args['max_workers'] else 3
        request_session.extract_keyframes_from_videos(output=output, max_concurrent=max_workers)
        print ('\n')
        print ('-' * 30)
    
    # end process
    log_text = f'''
    > Ending program at: {time.ctime()}

    '''
    print ('\n\n' + ' '.join(log_text.split()).strip())

if __name__ == '__main__':
    main()
