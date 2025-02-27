# -*- coding: utf-8 -*-

# import modules
import os
import aiohttp
import asyncio
import requests

# aiohttp
from aiohttp import ClientSession

# typing
from typing import Dict, List

# HTTP session class
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
            return {}
    
    async def fetch_image(self, session: ClientSession, url: str,
                          filename: str) -> None:
        '''
        Fetches an image from a URL and saves it to the output directory.

        :param session: The aiohttp ClientSession object.
        :param url: The URL of the image to download.
        :param filename: The path (including filename) where the image will be
            saved.
        '''
        try:
            async with session.get(url) as res:
                if res.status == 200:
                    image_data = await res.read()
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                else:
                    print (
                        f'Failed to download {url}, status code: {res.status}'
                    )
        except Exception as e:
            print (f'An error occurred while downloading {url}: {e}')
    
    async def download_images(self, urls: List[str], links: List[str],
                              output: str) -> None:
        '''
        Downloads images from a list of URLs asynchronously.

        :param urls: A list of image URLs to download.
        :param links: A list of TikTok links corresponding to the images.
        :param output: The directory path where the images will be saved.
        '''
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_image(
                    session=session, url=url,
                    filename=self._build_filename_path(output, link)
                ) for url, link in zip(urls, links)
            ]
            await asyncio.gather(*tasks)
    
    def _build_filename_path(self, output: str, link: str) -> str:
        '''
        Builds the filename path for saving the image based on the TikTok link.

        :param output: The directory path where the images will be saved.
        :param link: The TikTok link from which to extract the post ID.
        :return: The full path (including filename) where the image will be
            saved.
        '''
        post_id = link.split('/')[-1].split('?')[0]
        return f'{output}/image_id_{post_id}.png'

    def start_images_download(self, urls: List[str], links: List[str],
                              output: str) -> None:
        '''
        Starts the asynchronous download of images from a list of URLs.

        :param urls: A list of image URLs to download.
        :param links: A list of TikTok links corresponding to the images.
        :param output: The directory path where the images will be saved.
        '''
        path = f'{output}/tiktok_thumbnails'
        if not os.path.exists(path):
            os.makedirs(path)
        
        self.loop.run_until_complete(
            self.download_images(urls=urls, links=links, output=path)
        )
