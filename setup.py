# -*- coding: utf-8 -*-

# import modules
import os
from setuptools import setup, find_packages

setup(
    name="tikspyder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "apify-client",
        "pandas",
        "PySocks",
        "requests",
        "serpapi",
        "stem",
        "streamlit",
        "tqdm",
        "yt-dlp[default]"
    ],
    entry_points={
        'console_scripts': [
            'tikspyder=main:main',
        ],
    },
    python_requires='>=3.6',
    author="Esteban Ponce de Leon",
    description="A tool for collecting TikTok data",
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
)
