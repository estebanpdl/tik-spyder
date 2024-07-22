# -*- coding: utf-8 -*-

# import modules
import time
import pandas as pd

# typing
from typing import Dict, List

# SerpAPI utilities
from .utilities import search_query, select_serpapi_parameters, \
    extract_results_keys, extract_related_content_keys

# SerpAPI module
import serpapi

# SQLManager
from databases import SQLDatabaseManager

# Connections
from connections import RequestSession

# SerpAPI collector class
class SerpAPICollector:
    '''
    SerpAPICollector collects TikTok data from Google search results
    using SerpAPI.
    '''

    def __init__(self, args: Dict) -> None:
        '''
        Initializes SerpAPICollector with the given parameters and options
        from the command line.
        
        :param args: Dicti containing the command line arguments and options
        '''
        # get output data path
        self.output = args['output']

        # endpoint for SerpAPI
        self.api_key = args['api_key']
        self.endpoint = 'https://serpapi.com/search'

        # main site: tiktok.com
        self.site = 'tiktok.com'

        # build the search query string
        q = search_query(args=args)
        self.query = f'site:{self.site}/* {q}'

        # update the query parameter in args
        args['q'] = self.query

        # store the parameters
        self.parameters = select_serpapi_parameters(args)

        # SerpAPI client
        self.client = serpapi.Client(api_key=self.api_key)

        # database connection
        self.sql_database = SQLDatabaseManager(self.output)

        # connections
        self.related_content_urls = []
        self.related_content_depth = args['depth']
        self.req_session = RequestSession()
    
    def collect_search_results(self) -> None:
        '''
        Makes an API call to SerpAPI and processes the response data.

        Fetches data based on the initialized parameters and handles pagination
        to retrieve data from all available pages.
        '''
        print (f'\nAPI call to Google search results\n')
        print (f'> search query: {self.query}')
        try:
            iteration = 0
            api_response = self.client.search(self.parameters)
            print ('\n> Searching...')

            # process search results
            self._process_search_results(api_response.data, n=iteration)

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                next_response = api_response.next_page()

                # process search results
                self._process_search_results(next_response.data, n=iteration)

                # get next page
                next_page = next_response.next_page_url

                # update api_response for the next iteration
                api_response = next_response

                # chill out
                time.sleep(2)
                iteration += 1
            
            # api call status
            print ('> Done')
        
        except Exception as e:
            print (f'An error occurred during the API call: {e}')
    
    def _process_search_results(self, data: Dict, n: int) -> None:
        '''
        Processes the response data from SerpAPI, extracting organic results
        and inserting them into the SQL database.

        :param data: SerpAPI raw data response
        :param n: iterations
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
        else:
            if n == 0:
                print ('No organic results found in the response.')

    def collect_image_results(self) -> None:
        '''
        Makes an API call to SerpAPI to collect image thumbnails from Google
        Images.
        '''
        # Google Images API
        self.parameters['tbm'] = 'isch'

        # collect images
        print (f'\n\nAPI call to Google images')

        try:
            iteration = 0
            api_response = self.client.search(self.parameters)
            print ('\n> Searching images...')

            # process images results
            self._process_images_results(api_response.data, n=iteration)

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                next_response = api_response.next_page()

                # process image results
                self._process_images_results(next_response.data, n=iteration)

                # get next page
                next_page = next_response.next_page_url

                # update api_response for the next iteration
                api_response = next_response

                # chill out
                time.sleep(2)
                iteration += 1

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
    
    def _process_images_results(self, data: Dict, n: int) -> None:
        '''
        Processes the response data from SerpAPI, extracting thumbnails
        and inserting related data into the SQL database.

        :param data: SerpAPI raw data response
        :param n: iterations
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

                # save related content urls
                key = 'serpapi_related_content_link'
                self.related_content_urls += [
                    i[key] for i in d if key in i
                ]
        else:
            if n == 0:
                print ('No image results found in the response.')

    
    def _collect_related_content(self, url: str) -> None:
        '''
        Collects related content from the given URL.

        :param url: The URL to load related content from.
        '''
        content = self.req_session.load_related_content(
            url=url,
            api_key=self.api_key
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

    def collect_search_data(self) -> None:
        '''
        Collects both search results and corresponding image thumbnails.
        '''
        print('\n\n')
        print('-' * 30)
        print('Starting data collection process...\n')

        self.collect_search_results()
        self.collect_image_results()

        print('\n\nData collection complete.')
        print('-' * 30)
