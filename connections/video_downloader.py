# -*- coding: utf-8 -*-

# import modules
import os

# threads
from concurrent.futures import ThreadPoolExecutor, as_completed

# typing
from typing import List

# pathlib
from pathlib import Path

# progress bar
from tqdm import tqdm

# yt_dlp module
from yt_dlp import YoutubeDL

# Video downloader class
class VideoDownloader:
    '''
    VideoDownloader class

    This class handles the downloading of TikTok videos using yt-dlp and
    threading for concurrent downloads.
    '''
    def __init__(self, output: str) -> None:
        '''
        Initializes the VideoDownloader with default download options.

        :param output: The original directory path provided by the user
        '''
        self.download_options = {
            'format': '(bv*+ba/b)[vcodec!=?h265]',
            'outtmpl': self._build_output_directory(output),
            'no_warnings' : True,
            'quiet': True,
            'ignoreerrors': True,
            'noprogress': True
        }
    
    def _sanitize_output_path(self, output: str) -> str:
        '''
        Ensures the given path uses forward slashes and does not end with a
        slash.

        :param output: The original directory path provided by the user
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
    
    def _build_output_directory(self, output: str) -> str:
        '''
        Builds and sanitizes the output directory path for downloading videos.

        :param output: The original directory path provided by the user
        :return: The full path for saving downloaded videos with the filename
            template.
        '''
        output = self._sanitize_output_path(output=output)
        path = f'{output}/downloaded_videos'

        # ensure the directory exists
        if not os.path.exists(path=path):
            os.makedirs(path)
        
        return f'{path}/%(id)s.%(ext)s'

    def download_video(self, url: str) -> None:
        '''
        Downloads a single video from the specified URL using yt-dlp.

        :param url: The URL of the TikTok video to download.
        '''
        try:
            with YoutubeDL(self.download_options) as ydl:
                ydl.download(url)
        except Exception as e:
            print (f'Error downloading {url}: {e}')
    
    def download_videos(self, urls: List[str], max_workers: int) -> None:
        '''
        Downloads multiple videos concurrently using a thread pool.

        :param urls: A list of TikTok video URLs to download.
        :param max_workers: The maximum number of threads to use for
            downloading.
        '''
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.download_video, url): url
                for url in urls
            }
            for future in tqdm(
                    as_completed(future_to_url),
                    total=len(future_to_url),
                    desc='Downloading videos'
                ):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as e:
                    print (f'{url} generated an exception: {e}')

    def start_download(self, urls: List[str], max_workers: int = 5) -> None:
        '''
        Starts the download process for a list of TikTok video URLs.

        :param urls: A list of TikTok video URLs to download.
        :param max_workers: The maximum number of threads to use for
            downloading. Default is 5.
        '''
        print('\n\n')
        print('-' * 30)
        print('Downloading videos')
        print('Starting download...\n')
        
        # download videos
        self.download_videos(urls=urls, max_workers=max_workers)

        print('\n\nDownload complete.')
        print('-' * 30)
