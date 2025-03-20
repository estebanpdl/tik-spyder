<div align="center">

# **TikSpyder**

</div>

<br />

`TikSpyder` is a command-line tool designed to collect TikTok data using SerpAPI for Google search results and Apify for TikTok data extraction. The tool supports video downloading via yt-dlp and uses Python's asynchronous capabilities and multithreading for efficient data collection.

<br />
<br />

<div align="center">

[![GitHub forks](https://img.shields.io/github/forks/estebanpdl/tik-spyder.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/estebanpdl/tik-spyder/network/)
[![GitHub stars](https://img.shields.io/github/stars/estebanpdl/tik-spyder?style=social)](https://github.com/estebanpdl/tik-spyder/stargazers)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://x.com/estebanpdl)
[![Made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Twitter estebanpdl](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://x.com/estebanpdl)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/estebanpdl)

</div>

<hr />
<br />

## 🔍 **Description**

TikSpyder offers two main methods of data collection:
1. **Google Search Results**: Using SerpAPI to find TikTok videos based on search queries
2. **Direct Profile Scraping**: Using Apify to collect videos directly from TikTok profiles

The tool supports various filtering options, including date ranges and content types, and can download both videos and thumbnails. Data is stored in a SQLite database and can be exported to CSV files for further analysis.

Given the dynamic nature of search results and the constantly evolving landscape of TikTok's platform, it's important to note that the data collected by TikSpyder represents a sample rather than a comprehensive dataset. However, this sample can still be valuable for monitoring trends and identifying emerging narratives in the information ecosystem.

To get the most out of TikSpyder, **it is recommended to test your query using Google's advanced search features. This can help refine your search query, improve the relevance of your results, and test specific keywords more effectively**. By taking advantage of these features, you can ensure that you're collecting the most relevant data for your research or analysis.

<br />

## 🚀 **Features**

- Collects TikTok video links using SerpAPI and Apify.
- Collects and downloads thumbnails for TikTok videos.
- Collects related content to the search query.
- Stores collected data in a SQLite database.
- Exports data to CSV files.
- Downloads TikTok videos using yt-dlp.
- Supports asynchronous and multithreaded downloading for improved performance.
- Supports Tor network for downloading TikTok videos to enhance privacy and avoid rate limiting.

<br />

## ⚙️ **Requirements**

- [Python](https://www.python.org/) >= 3.11.7
- [SerpAPI key](https://serpapi.com/)
- [Apify API token](https://apify.com/) (optional)
- [Tor Browser](https://www.torproject.org/) (optional)
- [ffmpeg](https://ffmpeg.org/)
- Install the required Python libraries listed in `requirements.txt`.
- For the GUI app, tkinter is required. On Linux, install with `sudo apt-get install python3-tk` (Ubuntu/Debian) or your distribution's equivalent package.

<br />

## 🔧 **Installation**

1. Clone the repository

```sh
git clone https://github.com/estebanpdl/tik-spyder.git
cd tik-spyder
```

2. Install the required packages

```sh
pip install -r requirements.txt
```

or

```sh
pip3 install -r requirements.txt
```

3. Once you obtain an API key from SerpAPI and Apify, populate the config/config.ini file with the described values. Replace `api_key_value` and `apify_token_value` with your API key and token.

```ini

[SerpAPI Key]
api_key = your_serp_api_key

[Apify Token]
apify_token = your_apify_token
```

<br />

## 📚 **Usage**

```sh
python main.py [OPTIONS]
```

### **Command Line Arguments**

```sh
python main.py --help

# or

python main.py -h
```

```
Command Line Arguments.

Help options:
  -h, --help           Show this help message and exit.

SerpAPI options:
  --q                  The search term of phrase for which to retrieve TikTok data.
  --user               Specify a TikTok user to search for videos from.
  --google-domain      Defines the Google domain to use. It defaults to google.com.
  --gl                 Defines the country to use for the search. Two-letter country code.
  --hl                 Defines the language to use for the search. Two-letter language code.
  --cr                 Defines one or multiple countries to limit the search to.
  --safe               Level of filtering for adult content. Options: active (default), off
  --lr                 Defines one or multiple languages to limit the search to.
  --depth              Depth of iterations to follow related content links.

Google advanced search options:
  --before             Limit results to posts published before the specified date. Format: YYYY-MM-DD.
  --after              Limit results to posts published after the specified date. Format: YYYY-MM-DD.

Optional Apify arguments:
  --apify              Specify whether to use Apify integration.
  --oldest-post-date   Filter posts newer than the specified date. Format: YYYY-MM-DD.
  --newest-post-date   Filter posts older than the specified date. Format: YYYY-MM-DD.

Optional arguments and parameters:
  --use-tor            Specify whether to use Tor for downloading TikTok videos.
  -d, --download       Specify whether to download TikTok videos from SerpAPI and Apify.
  -w, --max-workers    Specify the maximum number of threads to use for downloading TikTok videos and extracting keyframes.
  -o, --output         Specify the output directory path. If not provided, data is saved in a timestamped subdirectory within the './tikspyder-data/' directory.
```

### **Example Usage**

1. Search-based collection:

```sh
python main.py --q "F-16 AND Enemy AND (Ukraine OR Russia)" --gl us --hl en --after 2024-02-01 --before 2024-05-31 --output {output_directory}/ --download

# Note: Replace '{output_directory}' with the desired output path.
```

2. Profile-based collection:

```sh
python main.py --q Trump --user username --output {output_directory}/ --download --apify --oldest-post-date 2025-01-01

# Note: Replace '{output_directory}' with the desired output path.
```

### Tor Integration
You can now use Tor network for downloading TikTok videos to enhance privacy and avoid rate limiting. To use this feature:

1. Make sure Tor Browser is installed and running
2. Configure your torrc file with:

```
## Enable SOCKS proxy
SocksPort 9050

## Enable Control Port for IP rotation
ControlPort 9051
CookieAuthentication 1
```

3. Use the `--use-tor` flag when running the script. If Tor connection fails, the script will automatically fall back to a normal connection.


<br />

## ☕ Support

If you find TikSpyder helpful, please consider buying me a coffee to support ongoing development and maintenance. Your donation will help me continue to improve the tool and add new features.

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/estebanpdl)

<br />
