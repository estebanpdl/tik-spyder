# -*- coding: utf-8 -*-

# import modules
import os
import time

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

# stem module
from stem import Signal
from stem.control import Controller

# Video downloader class
class VideoDownloader:
    '''
    VideoDownloader class

    This class handles the downloading of TikTok videos and their audio using
    yt-dlp and threading for concurrent downloads.
    '''
    def __init__(self, output: str, use_tor: bool = False) -> None:
        '''
        Initializes the VideoDownloader with default download options.
        Downloads both video and audio when initialized.

        :param output: The original directory path provided by the user
        :param use_tor: Boolean indicating whether to use Tor for downloads
        '''
        # initialize Tor proxy settings
        self.use_tor = use_tor
        self.proxy = 'socks5://127.0.0.1:9050'

        # Common options for both video and audio
        common_options = {
            'no_warnings': True,
            'quiet': True,
            'ignoreerrors': True,
            'noprogress': True
        }

        if self.use_tor:
            common_options['proxy'] = self.proxy

        # video download options
        self.video_options = {
            **common_options,
            'format': '(bv*+ba/b)[vcodec!=?h265]',
            'outtmpl': self._build_output_directory(output, 'downloaded_videos')
        }

        # audio download options
        self.audio_options = {
            **common_options,
            'format': 'bestaudio/best',
            'outtmpl': self._build_output_directory(output, 'downloaded_audios'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
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
    
    def _build_output_directory(self, output: str, dir_name: str) -> str:
        '''
        Builds and sanitizes the output directory path for downloading videos.

        :param output: The original directory path provided by the user
        :param dir_name: Name of the subdirectory (videos or audio)
        :return: The full path for saving downloaded files with the filename
            template.
        '''
        output = self._sanitize_output_path(output=output)
        path = f'{output}/{dir_name}'

        # ensure the directory exists
        if not os.path.exists(path):
            os.makedirs(path)
        
        return f'{path}/%(id)s.%(ext)s'

    def renew_tor_ip(self) -> None:
        '''
        Requests a new Tor circuit to change the IP address.
        '''
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                time.sleep(5)
        except Exception as e:
            print (f'Error renewing Tor IP: {e}')

    def download_content(self, url: str) -> None:
        '''
        Downloads both video and audio from the specified URL using yt-dlp.

        :param url: The URL of the TikTok video to download.
        '''
        max_attempts = 3 if self.use_tor else 1
        for attempt in range(max_attempts):
            try:
                # download video
                with YoutubeDL(self.video_options) as ydl:
                    ydl.download(url)

                # download audio
                with YoutubeDL(self.audio_options) as ydl:
                    ydl.download(url)
                
                return
                
            except Exception as e:
                print (f'Error downloading {url}: {e}')
                
                if self.use_tor and attempt < max_attempts - 1:
                    print ('Renewing Tor circuit...')
                    self.renew_tor_ip()

                    # wait for circuit to be established
                    time.sleep(5)
                else:
                    break

    def download_videos(self, urls: List[str], max_workers: int) -> None:
        '''
        Downloads multiple videos concurrently using a thread pool.

        :param urls: A list of TikTok video URLs to download.
        :param max_workers: The maximum number of threads to use for
            downloading.
        '''
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.download_content, url): url
                for url in urls
            }
            for future in tqdm(
                    as_completed(future_to_url),
                    total=len(future_to_url),
                    desc='Downloading content'
                ):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as e:
                    print (f'{url} generated an exception: {e}')

    def _test_tor_connection(self) -> bool:
        '''
        Tests if Tor is available and working.
        
        :return: True if Tor is available and working, False otherwise.
        '''
        try:
            # test if port is open
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 9050))
            if result != 0:
                print ('\n\n')
                print ('Tor SOCKS port (9050) is not open. Is Tor running?')
                print ('Falling back to normal connection.\n')
                return False
            
            # if port is open, test connection
            import requests
            print ('\n\nTesting Tor connection...')
            response = requests.get(
                'https://check.torproject.org/api/ip',
                proxies={
                    'http': self.proxy,
                    'https': self.proxy
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print (f'Tor connection successful. Exit node IP: {data.get("IP")}\n\n')
                return True
            else:
                print ('Tor enabled but connection check failed. Using normal connection.\n\n')
                return False
        
        except Exception as e:
            print (f'\nTor connection failed ({e}). Using normal connection.\n')
            return False

    def start_download(self, urls: List[str], max_workers: int) -> None:
        '''
        Starts the download process for a list of TikTok video URLs.

        :param urls: A list of TikTok video URLs to download.
        :param max_workers: The maximum number of threads to use for
            downloading. Default is 5.
        '''
        if self.use_tor:
            # test Tor connection and update use_tor flag accordingly
            self.use_tor = self._test_tor_connection()
            
            # remove proxy settings if Tor connection failed
            if not self.use_tor:
                for options in [self.video_options, self.audio_options]:
                    options.pop('proxy', None)
        
        print ('> Starting download...\n')
        
        # download videos
        self.download_videos(urls=urls, max_workers=max_workers)

        print ('\n\nDownload complete.')
