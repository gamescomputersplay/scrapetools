''' Downloader (from a list of URLs or a simple rules)
'''

import os
import requests
from tqdm import tqdm


# File with URLs to be downloaded (None to ignore)
URLS_FILE = None
# URL list (or comprehension) to be downloaded (None to ignore)
URLS_LIST = None

# Folder to put results in (will be created if doesn't exist)
RESULT_FOLDER = "raw_data"
# User Agent string to use
UA_STRING = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' + \
            'AppleWebKit/537.36 (KHTML, like Gecko) ' + \
            'Chrome/109.0.0.0 Safari/537.36'

def load_urls(filename):
    ''' Load and return the raw list of URLs
    '''
    urls = []
    with open(filename, "r", encoding="utf-8") as urls_file:
        for line in urls_file:
            urls.append(line.strip())
    return urls

def generate_filepaths(raw_list):
    ''' Generate all filepaths from list of URLs
    '''
    filepaths = []
    for url in raw_list:
        filename = url.replace("http://", "").replace("https://", "")
        filename = filename.replace("?", "-").replace("&", "-")
        filename = "-".join(filename.split("/")[1:])
        filepath = f"{RESULT_FOLDER}/{filename}"
        filepaths.append(filepath)
    return filepaths

def compile_dl_list(urls_list, filepaths):
    ''' Prepare a download list: a list of tuples (url, filename)
    '''
    download_list = []
    for url, path in zip(urls_list, filepaths):
        if os.path.exists(path):
            continue
        download_list.append((url, path))
    return download_list

def do_the_download(url, path):
    ''' The download itself
    '''
    headers={'User-agent': UA_STRING,}
    the_request = requests.get(url, headers=headers)
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(the_request.text)

def main():
    ''' Do the downloading
    '''

    # Load the list of URLs
    if URLS_FILE is not None:
        urls_list = load_urls(URLS_FILE)
    else:
        urls_list = URLS_LIST
    print(f"Loaded {len(urls_list)} URLs")

    # Generate filepath names
    filepaths = generate_filepaths(urls_list)

    # Compile final list, removing files already downloaded
    download_list = compile_dl_list(urls_list, filepaths)
    print(f"Urls to download {len(download_list)} URLs")

    # Create target folder if it doesn't exist
    if not os.path.exists(RESULT_FOLDER):
        os.mkdir(RESULT_FOLDER)

    # Do the downloads
    iterator = tqdm(download_list, leave=False, smoothing=0)
    for url, path in iterator:
        do_the_download(url, path)

if __name__ == "__main__":
    main()
