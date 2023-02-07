''' Downloader (from a list of URLs or a simple rules)
'''

import os
import time
import requests
import concurrent.futures

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

# Pause between requests
PAUSE = 1

# Threads
THREADS = 1

total_tasks = 0
completed_tasks = 0
start_time = None

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

def time_format(secs):
    ''' Nice H:MM:SS format for period in seconds
    '''
    hours = int(secs // 3600)
    minutes = int((secs - hours * 3600) // 60)
    seconds = int(secs - hours * 3600 - minutes * 60)

    return f"{str(hours)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

def do_the_download(data):
    ''' The download itself
    '''
    global completed_tasks

    url, path = data

    headers={'User-agent': UA_STRING,}
    the_request = requests.get(url, headers=headers)
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(the_request.text)

    time.sleep(PAUSE)

    completed_tasks += 1
    elapsed = time.time() - start_time
    eta = (elapsed / completed_tasks) * total_tasks

    print(f"[{completed_tasks}/{total_tasks}, {time_format(elapsed)}/{time_format(eta)}]: {url}")

def main():
    ''' Do the downloading
    '''

    global total_tasks
    global start_time

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
    total_tasks = len(urls_list)

    # Create target folder if it doesn't exist
    if not os.path.exists(RESULT_FOLDER):
        os.mkdir(RESULT_FOLDER)


    start_time = time.time()
    # Do the downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:        
        executor.map(do_the_download, download_list)

if __name__ == "__main__":
    main()
