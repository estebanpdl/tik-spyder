# -*- coding: utf-8 -*-

# import modules
import time
import pandas as pd

# typing
from typing import Dict

# SerpAPI utilities
from .utilities import search_query, select_serpapi_parameters, \
    extract_results_keys

# SerpAPI module
import serpapi

# SQLManager
from databases import SQLDatabaseManager

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
    
    def collect_search_results(self) -> None:
        '''
        Makes an API call to SerpAPI and processes the response data.

        Fetches data based on the initialized parameters and handles pagination
        to retrieve data from all available pages.
        '''
        print (f'\nAPI call to Google search results:\n> {self.query}')
        try:
            api_response = self.client.search(self.parameters)
            print ('\n...Searching')

            # process search results
            self._process_search_results(api_response.data)

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                next_response = api_response.next_page()

                # process search results
                self._process_search_results(next_response.data)

                # get next page
                next_page = next_response.next_page_url

                # update api_response for the next iteration
                api_response = next_response
                time.sleep(2)
            
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
        else:
            print ('No organic results found in the response.')

    def collect_image_thumbnails(self) -> None:
        '''
        Makes an API call to SerpAPI to collect image thumbnails from Google
        Images.
        '''
        # Google Images API
        self.parameters['tbm'] = 'isch'

        # collect images
        print (f'\nAPI call to Google images')

        try:
            api_response = self.client.search(self.parameters)
            print ('\n...Searching for thumbnails')

            # process images results
            self._process_images_results(api_response.data)

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                next_response = api_response.next_page()

                # process image results
                self._process_images_results(next_response.data)

                # get next page
                next_page = next_response.next_page_url

                # update api_response for the next iteration
                api_response = next_response
                time.sleep(2)

            # api call status
            print ('> Done')

        except Exception as e:
            print (f'An error occurred during the API call: {e}')
    
    def _process_images_results(self, data: Dict) -> None:
        '''
        Processes the response data from SerpAPI, extracting thumbnails
        and inserting related data into the SQL database.

        :param data: SerpAPI raw data response
        '''
        # get image results
        field = 'images_results'
        results = data.get(field, [])
        if results:
            d = extract_results_keys(results, result_type=field)

            # write results in SQL database
            if d:
                self.sql_database.insert_images_results(d)
        else:
            print ('No image results found in the response.')

    def _collect_related_content(self) -> None:
        '''
        '''
        pass

    def collect_search_data(self) -> None:
        '''
        '''
        pass
