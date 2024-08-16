<div align="center">

# **TikSpyder**

</div>

<br />

`TikSpyder` is a command-line tool designed to collect TikTok data from Google's search results using SerpAPI and yt-dlp for downloading TikTok videos. This tool utilizes Python's asynchronous capabilities and multithreading to enable efficient data collection and video downloading.

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

TikSpyder extracts TikTok video links from Google's search results and downloads the videos. It also supports storing and retrieving collected data in a SQLite database and exporting the data to CSV files.

Given the dynamic nature of search results and the constantly evolving landscape of TikTok's platform, it's important to note that the data collected by TikSpyder represents a sample rather than a comprehensive dataset. However, this sample can still be valuable for monitoring trends and identifying emerging narratives.

To get the most out of TikSpyder, **it is recommended to test your query using Google's advanced search features. This can help refine your search query, improve the relevance of your results, and test specific keywords more effectively**. By taking advantage of these features, you can ensure that you're collecting the most relevant data for your research or analysis.

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
- Install the required Python libraries listed in `requirements.txt`.

<br />

## 🔧 **Installation**

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

3. Once you obtain an API key from SerpAPI, populate the config/config.ini file with the described values. Replace `api_key_value` with your API key.

```ini
[SerpAPI Key]
api_key = api_key_value
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
Help options:
  -h, --help        Show this help message and exit.

SerpAPI options:
  --q               The search term of phrase for which to retrieve TikTok data.
  --user            Specify a TikTok user to search for videos from.
  --google-domain   Defines the Google domain to use. It defaults to google.com.
  --gl              Defines the country to use for the search. Two-letter country code.
  --hl              Defines the language to use for the search. Two-letter language code.
  --cr              Defines one or multiple countries to limit the search to.
  --lr              Defines one or multiple languages to limit the search to.
  --depth           Depth of iterations to follow related content links.

Google advanced search options:
  --before          Limit results to posts published before the specified date. Format: YYYY-MM-DD.
  --after           Limit results to posts published after the specified date. Format: YYYY-MM-DD.

Optional arguments and parameters:
  -o , --output     Specify the output data path. By default, output is saved in the ./data/ directory with a timestamp as the filename.
  --download        Specify whether to download TikTok videos from SerpAPI response.
  --max-workers     Specify the maximum number of threads to use for downloading TikTok videos.

```

### **Search query**

```sh
python main.py --q "F-16 AND Enemy AND (Ukraine OR Russia)" --gl us --hl en --after 2024-02-01 --before 2024-05-31 --output {output_directory}/ --download

# Note: Replace '{output_directory}' with the desired output path.
```

#### Explanation

The search query `--q "F-16 AND Enemy AND (Ukraine OR Russia)"` specifies that TikSpyder should search for TikTok videos related to the keywords "F-16", "Enemy", "Ukraine", and "Russia".

The `--gl us` option specifies that the search should be limited to the **United States**, while the `--hl en` option specifies that the search results should be in **English**.

The `--after 2024-02-01` and `--before 2024-05-31` options limit the search results to **videos published between February 1, 2024 and May 31, 2024**.

By default, collected data is saved in the `./data/` directory with a timestamp as the filename. To customize the output location, use the `--output` option followed by the desired directory path. For example, `--output my_directory/` would save the data in the my_directory/ directory.

The `--download` option specifies that TikSpyder should download the TikTok videos associated with the search results.

<br />

## ☕ Support

If you find TikSpyder helpful, please consider buying me a coffee to support ongoing development and maintenance. Your donation will help me continue to improve the tool and add new features.

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/estebanpdl)

<br />

## 📝 TODO

- [ ] Image classification using AI multimodal models
- [ ] Whisper integration
- [ ] Network mapping
- [ ] Handle duplicate link values
