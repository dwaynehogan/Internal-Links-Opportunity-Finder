# Internal Link Opportunity Finder

This Python script identifies internal linking opportunities within a list of website URLs by searching for unlinked mentions of specified keywords. It fetches the content of the provided site URLs, tokenizes the text into sentences, and searches for sentences that contain the target keywords but do not already contain a link. If such sentences are found, they are recorded as potential internal link opportunities.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Input Files](#input-files)
  - [Setting the API Key](#setting-the-api-key)
  - [Running the Script](#running-the-script)
- [Output](#output)
- [Notes](#notes)

## Features

- Fetches content from a list of site URLs using the Jina AI API.
- Uses NLTK for sentence tokenization.
- Identifies sentences containing unlinked mentions of target keywords.
- Skips sentences that already contain links or are headings/formatting.
- Normalizes URLs to avoid linking to the same page.
- Handles errors during content fetching and continues processing.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `pandas`
  - `requests`
  - `nltk`
- An API key for the [Jina AI API](https://jina.ai/).

## Installation


**Required Python packages**:

   ```bash
   pip install pandas requests nltk
   ```

**Download NLTK data**:

   The script will automatically download the required NLTK data (`punkt`) if not already installed. Alternatively, you can download it manually:

   ```python
   import nltk
   nltk.download('punkt')
   ```

## Usage

### Input Files
1. **`target_keywords.csv`**:

   A CSV file containing the target URLs and associated keywords. Each line should contain a target URL and a keyword search for, separated by a comma. No headers are required.

   Format:

   ```
   target_url,keyword
   ```

   Example:

   ```
   https://example.com/pageA,keyword1
   https://example.com/pageB,keyword2
   https://example.com/pageC,keyword3
   ```

   **Note**: The first column is the target URL, and the second column is the keyword.


2. **`site_urls.csv`**:

   A CSV file containing the site URLs to scrape for internal linking opportunities. Each URL should be on a separate line, and no headers are required.

   Example:

   ```
   https://example.com/page1
   https://example.com/page2
   https://example.com/page3
   ```


### Setting the API Key

The script requires an API key for the Jina AI API to fetch the content of the URLs. You need to obtain an API key from [Jina AI](https://jina.ai/).

1. Open the script file in a text editor.

2. Replace the placeholder `{your Jina.ai API key here}` with your actual API key:

   ```python
   # Set your API key
   api_key = '{your Jini.ai API key here}'
   ```

### Running the Script

Ensure that the input files (`site_urls.csv` and `target_keywords.csv`) are in the same directory as the script.

Run the script using the following command:

```bash
python internal_link_optimizer.py
```

The script will process each URL, fetch the content, and search for unlinked mentions of the keywords.

## Output

The script generates the following output files:

1. **`content.csv`**:

   A CSV file containing the source URLs and their fetched body texts.

   Format:

   ```
   source_url,body_text
   ```

2. **`unlinked_keywords.csv`**:

   A CSV file containing the found internal link opportunities. Each row contains:

   - **Source URL**: The URL where the unlinked keyword was found.
   - **Sentence**: The sentence containing the unlinked keyword.
   - **Keyword**: The keyword found.
   - **Target URL**: The target URL associated with the keyword.

   Format:

   ```
   Source URL,Sentence,Keyword,Target URL
   ```

## Notes

- **Sentence Skipping Criteria**:

  The script skips sentences that:

  - Do not end with punctuation (e.g., `.`, `?`, `!`).
  - Are headings or formatted text (e.g., start and end with `#`, `**`, or `*`).
  - Already contain links (identified by markdown link syntax `[text](url)`).

- **URL Normalization**:

  The script normalizes URLs to:

  - Ensure consistent comparison between source and target URLs.
  - Avoid suggesting links to the same page.
  - Handle cases where URLs have different schemes (`http` vs. `https`), `www` prefixes, or trailing slashes.

- **Error Handling**:

  If an error occurs while fetching the content of a URL (e.g., network issues, invalid URLs), the script records the error and continues processing the remaining URLs.

- **NLTK Data Download**:

  The script checks if the required NLTK data (`punkt`) is downloaded. If not, it will automatically download it at runtime.

