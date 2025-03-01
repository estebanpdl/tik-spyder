# -*- coding: utf-8 -*-

# import modules
import os
import time
import json
import uuid

# typing
from typing import Dict, List

# SerpAPI utilities
from .utilities import search_query, select_serpapi_parameters, \
    extract_results_keys, extract_related_content_keys

# SerpAPI module
import serpapi

# Apify client
from apify_client import ApifyClient

# pathlib
from pathlib import Path

# SQLManager
from databases import SQLDatabaseManager

# Media handlers
from media_handlers import RequestSession

# SerpAPI collector class
class TikTokDataCollector:
    '''
    TikTokDataCollector collects TikTok data from Google search results
    using SerpAPI.
    '''

    def __init__(self, args: Dict) -> None:
        '''
        Initializes TikTokDataCollector with the given parameters and options
        from the command line.
        
        :param args: Dict containing the command line arguments and options
        '''
        # get output data path
        self.output = self._sanitize_output_path(args['output'])

        # endpoint for SerpAPI
        self.api_key = args['api_key']
        self.endpoint = 'https://serpapi.com/search'

        # Apify token
        self.apify_token = args['apify_token']

        # main site: tiktok.com
        self.site = 'tiktok.com'

        # build the search query string
        q = search_query(args=args)

        # get provided user
        self.user = args['user']
        if self.user is not None:
            self.user = self.user[1:] if self.user.startswith('@') \
                else self.user

        # build advanced search query
        self.query = f'site:{self.site}/* {q}' if self.user is None \
            else f'site:{self.site}/@{self.user}/* {q}'

        # update the query parameter in args
        args['q'] = self.query

        # store the parameters
        self.parameters = select_serpapi_parameters(args)

        # SerpAPI client
        self.client = serpapi.Client(api_key=self.api_key)

        # Apify client
        self.run_apify = False
        if args['apify']:
            self.run_apify = True
            self.should_download_videos = args['download']
            self.apify_client = ApifyClient(self.apify_token)

            # optional date filters
            self.oldest_post_date = args['oldest_post_date']
            self.newest_post_date = args['newest_post_date']

        # database connection
        self.sql_database = SQLDatabaseManager(self.output, self.run_apify)

        # connections
        self.related_content_urls = []
        self.related_content_depth = args['depth']
        self.http_session = RequestSession()
    
    def _sanitize_output_path(self, output: str) -> str:
        '''
        Ensures the given path uses forward slashes and does not end with a
        slash.

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

    def collect_search_results(self) -> None:
        '''
        Makes an API call to SerpAPI and processes the response data.

        Fetches data based on the initialized parameters and handles pagination
        to retrieve data from all available pages.
        '''
        print (f'\nAPI call to Google search results\n')
        print (f'> search query: {self.query}')
        result_type = 'search_result'
        try:
            api_response = self.client.search(self.parameters)
            print ('\n> Searching...')

            # save raw data
            self._save_raw_data(
                self.output,
                result_type=result_type,
                data=api_response.data
            )

            # found results
            found_results = False

            # process search results
            self._process_search_results(api_response.data)
            if api_response.data.get('organic_results', []):
                found_results = True

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                # get new API response
                next_response = api_response.next_page()

                # save raw data
                self._save_raw_data(
                    self.output,
                    result_type=result_type,
                    data=next_response.data
                )

                # process search results
                self._process_search_results(next_response.data)

                # get next page
                next_page = next_response.next_page_url

                # update api_response for the next iteration
                api_response = next_response

                # chill out
                time.sleep(2)
            
            if not found_results:
                print('No organic results found.')

            # api call status
            print ('> Done')
        
        except Exception as e:
            print (f'An error occurred during the API call: {e}')
    
    def _process_search_results(self, data: Dict) -> None:
        '''
        Processes the response data from SerpAPI, extracting organic results
        and inserting them into the SQL database.

        :param data: SerpAPI raw data response
        '''
        # get organic search results
        field = 'organic_results'
        result_type = 'search_result'
        results = data.get(field, [])
        if results:
            d = extract_results_keys(results, result_type=result_type)
            
            # write results in SQL database
            if d:
                self.sql_database.insert_search_results(d)

    def collect_image_results(self) -> None:
        '''
        Makes an API call to SerpAPI to collect image thumbnails from Google
        Images.
        '''
        # Google Images API
        self.parameters['tbm'] = 'isch'

        # collect images
        print (f'\n\nAPI call to Google images')
        result_type = 'image_result'
        try:
            api_response = self.client.search(self.parameters)
            print ('\n> Searching images...')

            # save raw data
            self._save_raw_data(
                self.output,
                result_type=result_type,
                data=api_response.data
            )

            # found results
            found_results = False

            # process images results
            self._process_images_results(api_response.data)
            if api_response.data.get('images_results', []):
                found_results = True

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                next_response = api_response.next_page()

                # save raw data
                self._save_raw_data(
                    self.output,
                    result_type=result_type,
                    data=next_response.data
                )

                # process image results
                self._process_images_results(next_response.data)

                # get next page
                next_page = next_response.next_page_url

                # update api_response for the next iteration
                api_response = next_response

                # chill out
                time.sleep(2)

            if not found_results:
                print ('No image results found in the response.')

            # api call status
            print ('> Done')

        except Exception as e:
            print (f'An error occurred during the API call: {e}')
        
        # collect related content
        print (f'\n\nCollecting related content')
        if self.related_content_urls:
            self.related_content_urls = self.related_content_urls[
                :self.related_content_depth
            ]
            for url in self.related_content_urls:
                self._collect_related_content(url=url)
            print ('> Done')
        else:
            print ('No related content found.')
    
    def _process_images_results(self, data: Dict) -> None:
        '''
        Processes the response data from SerpAPI, extracting thumbnails
        and inserting related data into the SQL database.

        :param data: SerpAPI raw data response
        '''
        # get image results
        field = 'images_results'
        result_type = 'image_result'
        results = data.get(field, [])
        if results:
            d = extract_results_keys(results, result_type=result_type)

            # write results in SQL database
            if d:
                self.sql_database.insert_images_results(d)

                # download images
                print (f'\n\nDownloading images results')
                thumbnails = [i['thumbnail'] for i in d]
                links = [i['link'] for i in d]
                self.http_session.start_images_download(
                    urls=thumbnails,
                    links=links,
                    output=self.output
                )
                print ('> Done')

                # save related content urls
                key = 'serpapi_related_content_link'
                self.related_content_urls += [
                    i[key] for i in d if key in i
                ]
    
    def _collect_related_content(self, url: str) -> None:
        '''
        Collects related content from the given URL.

        :param url: The URL to load related content from.
        '''
        result_type = 'related_content'
        content = self.http_session.load_related_content(
            url=url,
            api_key=self.api_key
        )

        # save raw data
        self._save_raw_data(
            self.output,
            result_type=result_type,
            data=content
        )

        # process related content
        self._process_related_content(content)
    
    def _process_related_content(self, content: Dict) -> None:
        '''
        Processes the related content data.

        :param content: A dictionary containing the related content data.
        '''
        # get related content
        possible_fields = ['related_content', 'images_results']
        related_content = []
        for field in possible_fields:
            related_content = content.get(field, None)
            if related_content is not None:
                break
        
        if related_content:
            d = extract_related_content_keys(related_content)

            # write results in SQL database
            if d:
                self.sql_database.insert_related_content(d)
        else:
            print ('No results found in this URL')

    def _apify_tiktok_profile_scraper(self) -> None:
        '''
        Collects search data using Apify.
        '''
        print ('\n\nCollecting user data with Apify')

        # get the search results
        run_input = {
            'profiles': [self.user],
            'profileScrapeSections': ['videos'],
            'profileSorting': 'latest',
            'resultsPerPage': 100,
            'excludePinnedPosts': False,
            'shouldDownloadVideos': self.should_download_videos,
            'shouldDownloadCovers': True,
            'shouldDownloadSubtitles': False,
            'shouldDownloadSlideshowImages': False,
            'shouldDownloadAvatars': True
        }

        # add optional date filters
        if self.oldest_post_date:
            run_input['oldestPostDate'] = self.oldest_post_date
        if self.newest_post_date:
            run_input['newestPostDate'] = self.newest_post_date

        # run the Apify actor
        apify_actor_key = '0FXVyOXXEmdGcV88a'
        run = self.apify_client.actor(apify_actor_key).call(
            run_input=run_input
        )

        # store data
        store_data = []
        for item in self.apify_client.dataset(run['defaultDatasetId']).iterate_items():
            store_data.append(item)

        # write raw data
        self._save_raw_data(
            self.output,
            result_type='apify_profile_data',
            data=store_data
        )

        # process data
        self._process_apify_profile_data(store_data)
        
    def _process_apify_profile_data(self, data: Dict) -> None:
        '''
        Processes the Apify profile data.

        :param data: A dictionary containing the Apify profile data.
        '''
        # insert data into SQL database
        self.sql_database.insert_apify_profile_data(data)

        '''
        - download videos
        - download audio
        - download covers/thumbnails
        '''
        x = 1

        return
    
    def _save_raw_data(self, output: str, result_type: str, data: Dict) -> None:
        '''
        Saves the raw data response from SerpAPI in a JSON file.

        :param output: The directory path where the raw data should be saved.
        :param result_type: Type of SerpAPI response: 'search_result',
            'image_result', or 'related_content'
        :param data: The raw data response from SerpAPI to be saved.
        '''
        # create the directory structure if it does not exist
        folder = f'{output}/raw_data/{result_type}'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # create a timestamp for the file name
        stamp = int(time.time())
        uuid_code = str(uuid.uuid4()).split('-')[-1]

        # convert the data to a JSON string
        obj = json.dumps(data, ensure_ascii=False, indent=2)

        # write the JSON string to a file
        file_path = f'{folder}/{result_type}_{stamp}_{uuid_code}.json'
        with open(file_path, encoding='utf-8', mode='w') as writer:
            writer.write(obj)
    
    def collect_search_data(self) -> None:
        '''
        Collects both search results and corresponding image thumbnails.
        '''
        print('\n\n')
        print('-' * 30)
        print('Starting data collection process...\n')

        self.collect_search_results()
        self.collect_image_results()

        if self.run_apify:
            self._apify_tiktok_profile_scraper()

        print('\n\nData collection complete.')
        print('-' * 30)

    def generate_data_files(self) -> None:
        '''
        Selects all data from SQL tables and generates CSV files
        '''
        print (f'\n\nGenerating CSV files')
        self.sql_database.fetch_all_data()
        print ('> Done')

    def get_collected_videos(self) -> List[str]:
        '''
        Retrieves all collected video links from the SQL database.

        :return: A list of unique video links.
        '''
        return self.sql_database.get_collected_videos()
    
