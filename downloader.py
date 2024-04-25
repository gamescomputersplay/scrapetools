''' Downloader (from a list of URLs or a simple rules)
'''

import os
import time
import concurrent.futures

import requests


class Downloader:
    ''' Class that provides functionality for mass download a list of URLs
    '''

    def __init__(self,
                 urls_filename=None,
                 urls_list=None,
                 target_folder="downloaded_data",
                 user_agent=None,
                 cookies=None,
                 binary=False,
                 path_in_filename=True,
                 pause=0,
                 threads=1):

        # Folder to put results in (will be created if doesn't exist)
        self.target_folder = target_folder

        # Variables to track progress
        self.total_tasks = 0
        self.completed_tasks = 0
        self.start_time = None

        # This list will contain "download tasks" as [(url, filepath), ...]
        self.download_list = []

        # Whether to use a full path in the filename
        self.path_in_filename = path_in_filename

        # Initiate the download_list
        self.compile_download_list(urls_filename, urls_list)

        # User Agent string to use
        if user_agent is None:
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' + \
                              'AppleWebKit/537.36 (KHTML, like Gecko) ' + \
                              'Chrome/109.0.0.0 Safari/537.36'
        else:
            self.user_agent = user_agent

        # Cookies (a dict)
        if cookies is None:
            self.cookies = {}
        else:
            self.cookies = cookies

        # Binary mode (for images, etc.)
        self.binary = binary

        # Pause between requests
        self.pause = pause

        # Threads
        self.threads = threads

    def compile_download_list(self, urls_file, urls_list):
        ''' Prepare everything for download:
        - generate all filenames
        - check if some of the files are already downloaded
        '''

        def load_urls_from_file():
            ''' Load and return the raw list of URLs
            '''
            urls = []
            with open(urls_file, "r", encoding="utf-8") as input_file:
                for line in input_file:
                    urls.append(line.strip())
            return urls

        def generate_filepaths():
            ''' Generate all filepaths from list of URLs.
            Rules are:
            - remove domain name
            - replace /, &, ? with hyphens
            '''
            filepaths = []
            for line_n, url in enumerate(list_of_urls):

                # Generate resulting filenames
                # Either from the full path
                if self.path_in_filename:
                    filename = url.replace("http://", "").replace("https://", "")
                    filename = filename.replace("?", "-").replace("&", "-")
                    filename = "-".join(filename.split("/")[1:])
                # Or just the filename
                else:
                    filename = url.split("/")[-1]
                    # Make it work even if it is just folders
                    if filename == "":
                        filename = f"_default_{line_n}"

                filepath = f"./{self.target_folder}/{filename}"
                filepaths.append(filepath)
            return filepaths

        def compile_download_list():
            ''' Prepare a download list: a list of tuples (url, urls_filename)
            Ignore files that already exist
            '''
            download_list = []
            for url, path in zip(list_of_urls, list_of_filepaths):
                if os.path.exists(path):
                    continue
                download_list.append((url, path))
            return download_list

        list_of_urls = []
        # Load the list of URLs from file
        if urls_file is not None:
            list_of_urls = load_urls_from_file()
            print(f"Loaded from {urls_file}: {len(list_of_urls)} URLs")

        # Extend it with the list of URLs from the url list
        if urls_list is not None:
            list_of_urls.extend(urls_list)
            print(f"Loaded from the list: {len(urls_list)} URLs")

        # Generate filepath names
        list_of_filepaths = generate_filepaths()

        # Compile final list, removing files already downloaded
        self.download_list = compile_download_list()

        self.total_tasks = len(self.download_list)
        print(f"Urls to download: {self.total_tasks}")

        return

    def run(self):
        ''' Do the downloading
        '''

        def time_format(secs):
            ''' Nice H:MM:SS format for period in seconds
            '''
            hours = int(secs // 3600)
            minutes = int((secs - hours * 3600) // 60)
            seconds = int(secs - hours * 3600 - minutes * 60)

            return f"{str(hours)}:" + \
                   f"{str(minutes).zfill(2)}:" + \
                   f"{str(seconds).zfill(2)}"

        def do_one_download(data):
            ''' The download itself
            '''

            url, path = data

            headers = {'User-agent': self.user_agent}
            the_request = requests.get(url, headers=headers, cookies=self.cookies, timeout=10)

            if self.binary:
                with open(path, "wb") as outfile:
                    outfile.write(the_request.content)
            else:
                with open(path, "w", encoding="utf-8") as outfile:
                    outfile.write(the_request.text)



            # Update the number of complete tasks, calculate ETA
            self.completed_tasks += 1
            elapsed = time.time() - self.start_time
            eta = (elapsed / self.completed_tasks) * self.total_tasks

            print(f"[{self.completed_tasks}/{self.total_tasks}, " +
                  f"{time_format(elapsed)}/{time_format(eta)}, {len(the_request.text)}]: {url}")

            time.sleep(self.pause)

        # Create target folder if it doesn't exist
        if not os.path.exists(f"./{self.target_folder}"):
            os.mkdir(f"./{self.target_folder}")

        # Start timing
        self.start_time = time.time()

        # Do the downloads
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) \
             as executor:
            executor.map(do_one_download, self.download_list)


if __name__ == "__main__":
    print("This is a module with the Downloader class.")
    print("Here's basic usage example:")
    print()
    print("from downloader import Downloader")
    print('download_job = Downloader("url_list.txt", target_folder="data")')
    print("download_job.run()")
    print()
