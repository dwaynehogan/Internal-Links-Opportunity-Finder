import pandas as pd
import requests
from urllib.parse import quote, urlparse, urlunparse
import re
import csv
import nltk

# Download NLTK sentence tokenizer if not already downloaded
nltk.download('punkt')

# Define the function for sentence tokenization
def sentence_tokenizer(text):
    """
    Tokenizes the text into sentences that end with punctuation (., ?, !, etc.).
    """
    if not isinstance(text, str):
        return []
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text.strip())
    return sentences

# Define function to normalize URLs
def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    if (scheme == 'http' and parsed.port == 80) or (scheme == 'https' and parsed.port == 443):
        netloc = netloc.split(':')[0]
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    path = parsed.path.rstrip('/')
    normalized = urlunparse((scheme, netloc, path, '', '', ''))
    return normalized

# Define function to extract unlinked keywords
def find_unlinked_keywords(source_url, body_text, keywords_list):
    normalized_source_url = normalize_url(source_url)
    sentences = sentence_tokenizer(body_text)

    results = []
    for sentence in sentences:
        sentence_stripped = sentence.strip()

        if not re.search(r'[.!?]$', sentence_stripped) or re.match(r'^#+\s', sentence_stripped):
            continue
        if sentence_stripped.startswith('**') and sentence_stripped.endswith('**'):
            continue
        if sentence_stripped.startswith('*') and sentence_stripped.endswith('*'):
            continue
        if re.search(r'\[([^\]]+)\]\([^\)]+\)', sentence_stripped):
            continue

        sentence_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', sentence_stripped)

        for keyword, target_url in keywords_list:
            normalized_target_url = normalize_url(target_url)

            if normalized_source_url == normalized_target_url:
                continue

            if re.search(rf'\b{re.escape(keyword)}\b', sentence_clean, re.IGNORECASE):
                results.append({
                    'Source URL': source_url,
                    'Sentence': sentence_stripped,
                    'Keyword': keyword,
                    'Target URL': target_url
                })
    return results

# Main function to combine both processes
def main():
    # Set your API key
    api_key = '{your Jina.ai API key here}'  # Replace with your actual API key
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Load the input data
    df = pd.read_csv('site_urls.csv', encoding='utf-8-sig', header=None)
    keywords_df = pd.read_csv('target_keywords.csv', header=None)

    # Assuming the columns in keywords.csv are: target_url, keyword
    keywords_list = keywords_df[[1, 0]].values.tolist()  # Adjusted for zero-indexing without headers

    # Initialize lists to store final results
    source_urls = []
    body_texts = []
    all_results = []

    # Iterate over each URL and get body content
    for idx, url in enumerate(df[0]):  # Assuming URLs are in the first column of the CSV
        url = url.strip()
        encoded_url = quote(url, safe='/:')
        api_url = f'https://r.jina.ai/{encoded_url}'

        # Print the progress of URL fetching
        print(f"Processing URL {idx+1}/{len(df)}: {url}")
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            text = response.text
            print(f"Successfully fetched content from {url}")
        except requests.exceptions.RequestException as e:
            text = f"Error: {e}"
            print(f"Failed to fetch content from {url}. Error: {e}")

        source_urls.append(url)
        body_texts.append(text)

        # Print progress of unlinked keyword search
        print(f"Searching for unlinked keywords in {url}...")
        results = find_unlinked_keywords(url, text, keywords_list)
        if results:
            print(f"Found {len(results)} unlinked keyword(s) in {url}")
        else:
            print(f"No unlinked keywords found in {url}")
        all_results.extend(results)

    # Create a DataFrame with the URLs and their body texts
    content_df = pd.DataFrame({'source_url': source_urls, 'body_text': body_texts})
    content_df.to_csv('content.csv', index=False, quoting=csv.QUOTE_ALL, lineterminator='\n', header=False)
    print("Body content saved to 'content.csv'.")


    # If unlinked keywords are found, save them to a CSV file
    if all_results:
        # Convert the results to a DataFrame and specify the correct column names
        results_df = pd.DataFrame(all_results)
        results_df = results_df.rename(columns={
            'Source URL': 'source_url',
            'Sentence': 'sentence/paragraph',
            'Keyword': 'link_text',
            'Target URL': 'target_url'
        })
        
        # Save the DataFrame to CSV with headers
        results_df.to_csv('unlinked_keywords.csv', index=False, header=True)
        print("Unlinked keywords found and saved to 'unlinked_keywords.csv'.")
    else:
        print("No unlinked keywords found.")


if __name__ == "__main__":
    main()
