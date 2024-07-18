# -*- coding: utf-8 -*-

# import modules
import time
import asyncio
import requests

# typing
from typing import Dict, List

# SerpAPI collector class
class RequestSession:
    '''
    RequestSession

    This class handles HTTP requests and asynchronous tasks for interacting
    with the SerpAPI response and processing related content links

    '''
    def __init__(self) -> None:
        '''
        Initializes the RequestSession object.
        '''
        # request session
        headers = {'accept': 'application/json'}
        self.req_session = requests.Session()
        self.req_session.headers.update(headers)

        # asynchronous event loop
        self.loop = asyncio.get_event_loop()
    
    def load_related_content(self, url: str, api_key: str) -> List[Dict]:
        '''
        Loads related content from the given URL using the provided API key.

        :param url: The URL to load related content from.
        :param api_key: SerpAPI key for authentication.
        :return: A list of dictionaries containing the related content data.
        '''
        params = {'api_key': api_key}

        def fetch_content(url: str) -> Dict:
            response = self.req_session.get(url, params=params)
            response.raise_for_status()
            return response.json()

        try:
            content = fetch_content(url)
            see_more_link = content.get('serpapi_see_more_link')
            if see_more_link:
                content = fetch_content(see_more_link)
            return content
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            return []
