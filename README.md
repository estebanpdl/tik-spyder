<div align="center">

# **TikSpyder**

</div>

<br />

`TikSpyder` is a command-line tool designed to collect TikTok data from Google's search results using SerpAPI and yt-dlp for downloading TikTok videos. This tool utilizes Python's asynchronous capabilities and multithreading to enable efficient data collection and video downloading.

<br />
<br />

<div align="center">

[![GitHub forks](https://img.shields.io/github/forks/estebanpdl/TikSpyder.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/estebanpdl/TikSpyder/network/)
[![GitHub stars](https://img.shields.io/github/stars/estebanpdl/TikSpyder?style=social)](https://github.com/estebanpdl/TikSpyder/stargazers)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://x.com/estebanpdl)
[![Made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Twitter estebanpdl](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://x.com/estebanpdl)

</div>

<hr />
<br />

## 🔍 **Description**

TikSpyder extracts TikTok video links from Google's search results and downloads the videos. It also supports storing and retrieving collected data in a SQLite database and exporting the data to CSV files.

<br />

## 🚀 **Features**

- Collects TikTok video links using SerpAPI.
- Collects and downloads thumbnails for TikTok videos.
- Collects related content to the search query.
- Stores collected data in a SQLite database.
- Exports data to CSV files.
- Downloads TikTok videos using yt-dlp.
- Supports asynchronous and multithreaded downloading for improved performance.

<br />

## ⚙️ **Requirements**

- [Python](https://www.python.org/) >= 3.11.7
- [SerpAPI key](https://serpapi.com/)
- Install the required Python libraries listed in `requirements.txt`:

<br />


## ⚙️ **Installation**

1. Clone the repository

```sh
git clone https://github.com/estebanpdl/TikSpyder.git
cd TikSpyder
```

2. Install the required packages

```sh
pip install -r requirements.txt
```

or

```sh
pip3 install -r requirements.txt
```

3. Once you obtain an API key from SerpAPI, populate the config/config.ini file with the described values. Replace api_key_value with your API key.

```sh
[SerpAPI Key]
api_key = api_key_value
```
