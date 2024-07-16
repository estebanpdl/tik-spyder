# -*- coding: utf-8 -*-

# import modules
import time
import pandas as pd

# typing
from typing import Dict

# SerpAPI utilities
from .utilities import search_query, select_serpapi_parameters, \
    get_serpapi_response_keys

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
        args['query'] = self.query

        # store the parameters
        self.parameters = select_serpapi_parameters(args)

        # SerpAPI client
        self.client = serpapi.Client(api_key=self.api_key)

        # database connection
        self.sql_database = SQLDatabaseManager(self.output)
    
    def api_call(self) -> None:
        '''
        Makes an API call to SerpAPI and processes the response data.

        Fetches data based on the initialized parameters and handles pagination
        to retrieve data from all available pages.
        '''
        print (f'\nSearch query:\n{self.query}')
        try:
            api_response = self.client.search(self.parameters)
            print ('\n...Processing')

            # process data
            self._process_response_data(api_response.data)

            # get next page
            next_page = api_response.next_page_url
            while next_page:
                next_response = api_response.next_page()

                # process data
                self._process_response_data(next_response.data)

                next_page = next_response.next_page_url
                time.sleep(2)
        
        except Exception as e:
            print (f'An error occurred during the API call: {e}')
    
    def _process_response_data(self, data: Dict) -> None:
        '''
        Processes the response data from SerpAPI, extracting organic results
        and inserting them into the SQL database.

        :param data: SerpAPI raw data response
        '''
        # get organic search results
        field = 'organic_results'
        results = data.get(field, [])
        if results:
            d = get_serpapi_response_keys(results)
            
            # write results in SQL database
            if d:
                self.sql_database.insert_search_results(d)
        else:
            print ('No organic results found in the response.')

    def thumbnails_collector(self) -> None:
        '''
        '''
        self.parameters['tbm'] = 'isch'

    def related_content_links(self) -> None:
        '''
        '''
        pass

    def run(self) -> None:
        '''
        '''
        return self.parameters
