''' Example of using Downloader module
'''

from downloader import Downloader

download_job = Downloader("url_list.txt", target_folder="data")
download_job.run()
