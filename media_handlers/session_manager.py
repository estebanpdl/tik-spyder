# -*- coding: utf-8 -*-

# import modules
import os
import glob
import aiohttp
import asyncio
import requests
import subprocess

# progress bar
from tqdm import tqdm

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
            print (f'An error occurred: {e}')
            return {}
    
    def _build_media_filename_path(self, output: str, link: str, file_extension: str) -> str:
        '''
        Builds the filename path for saving the image based on the TikTok link.

        :param output: The directory path where the images will be saved.
        :param link: The TikTok link from which to extract the post ID.
        :param file_extension: The file extension of the media file.
        :return: The full path (including filename) where the image will be
            saved.
        '''
        post_id = link.split('/')[-1].split('?')[0]
        return f'{output}/{post_id}.{file_extension}'
    
    async def fetch_file(self, session: ClientSession, url: str,
                         filename: str) -> None:
        '''
        Fetches a file from a URL and saves it to the output directory.

        :param session: The aiohttp ClientSession object.
        :param url: The URL of the file to download.
        :param filename: The path (including filename) where the file will be
            saved.
        '''
        try:
            async with session.get(url) as res:
                if res.status == 200:
                    file_data = await res.read()
                    with open(filename, 'wb') as f:
                        f.write(file_data)
                else:
                    print (
                        f'Failed to download {url}, status code: {res.status}'
                    )
        except Exception as e:
            print (f'An error occurred while downloading {url}: {e}')
    
    async def download_files(self, urls: List[str], links: List[str],
                             output: str, file_extension: str) -> None:
        '''
        Downloads files from a list of URLs asynchronously.

        :param urls: A list of file URLs to download.
        :param links: A list of TikTok links corresponding to the files.
        :param output: The directory path where the files will be saved.
        :param file_extension: The file extension of the media file.
        '''
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_file(
                    session=session, url=url,
                    filename=self._build_media_filename_path(output, link, file_extension)
                ) for url, link in zip(urls, links)
            ]
            await asyncio.gather(*tasks)
    
    def start_media_download(self, urls: List[str], links: List[str],
                             output: str, media_type: str) -> None:
        '''
        Starts the asynchronous download of files from a list of URLs.

        :param urls: A list of file URLs to download.
        :param links: A list of TikTok links corresponding to the files.
        :param output: The directory path where the files will be saved.
        :param media_type: The type of media to download.
        '''
        media_object = {
            'image': {
                'path': 'thumbnails',
                'file_extension': 'png'
            },
            'video': {
                'path': 'downloaded_videos',
                'file_extension': 'mp4'
            }
        }

        path = f'{output}/{media_object[media_type]["path"]}'
        if not os.path.exists(path):
            os.makedirs(path)
        
        file_extension = media_object[media_type]['file_extension']
        self.loop.run_until_complete(
            self.download_files(urls=urls, links=links, output=path,
                                file_extension=file_extension)
        )

    def extract_audio_from_videos(self, output: str) -> None:
        '''
        Extracts audio from video files.

        :param output: The directory path where audios will be saved.
        '''
        # build audio path
        audio_path = f'{output}/downloaded_audios'
        if not os.path.exists(audio_path):
            os.makedirs(audio_path)

        # get all video files
        path = f'{output}/downloaded_videos'
        files = glob.glob(f'{path}/*.mp4')

        # extract audio from each video
        for file in files:
            try:
                # get id from video filename
                video_id = os.path.basename(file).split('.')[0]

                # FFmpeg command to extract audio
                cmd = [
                    'ffmpeg',
                    '-i', file,
                    '-q:a', '0',
                    '-map', 'a',
                    '-y',
                    f'{audio_path}/{video_id}.mp3'
                ]

                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                print (f'Error extracting audio: {e}')

    def extract_keyframes_from_videos(self, output: str, max_concurrent: int) -> None:
        '''
        Extracts keyframes from video files.

        :param output: The directory path where keyframes will be saved.
        :param max_concurrent: Maximum number of concurrent ffmpeg processes.
        '''
        # build keyframes path
        keyframes_path = f'{output}/keyframes'
        if not os.path.exists(keyframes_path):
            os.makedirs(keyframes_path)

        # get all video files
        path = f'{output}/downloaded_videos'
        files = glob.glob(f'{path}/*.mp4')

        # videos ids already processed
        processed_videos = [i.split('\\')[-1] for i in glob.glob(f'{keyframes_path}/*')]

        async def extract_keyframes(file, pbar):
            try:
                # get id from video filename
                video_id = os.path.basename(file).split('.')[0]
                if video_id not in processed_videos:
                    # create subdirectory for this video_id
                    video_keyframes_dir = f'{keyframes_path}/{video_id}'
                    if not os.path.exists(video_keyframes_dir):
                        os.makedirs(video_keyframes_dir)
                    
                    # FFmpeg command to extract keyframes
                    cmd = [
                        'ffmpeg',
                        '-i', file,
                        '-vf', 'select=eq(pict_type\\,I)',
                        '-vsync', 'vfr',
                        '-q:v', '2',
                        f'{video_keyframes_dir}/keyframe_%04d.jpg'
                    ]

                    # run FFmpeg as async subprocess
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    await process.communicate()
            except Exception as e:
                print (f'Error extracting keyframes: {e}')
            finally:
                pbar.update(1)

        async def process_all_videos():
            # create progress bar in the main thread
            pbar = tqdm(total=len(files), desc='Extracting keyframes', unit='video')
            
            # use semaphore to limit concurrent processes
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def process_with_semaphore(file):
                async with semaphore:
                    await extract_keyframes(file, pbar)
            
            # create tasks for all videos
            tasks = [process_with_semaphore(file) for file in files]
            await asyncio.gather(*tasks)
            
            pbar.close()

        # run the async event loop
        self.loop.run_until_complete(process_all_videos())
