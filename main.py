import os
import requests

def verify_server_support_range(status_code):
    if status_code == 206:
        return True
    return False

def get_downloaded_size(filename):
    if os.path.exists(filename):
        return os.path.getsize(filename)
    return 0

class DownloadManager:
    def __init__(self, filename, url_for_download_file):
        self.filename = filename
        self.url_for_download_file = url_for_download_file
        self.downloaded_size = 0

    def download_file_with_range(self):
        self.downloaded_size = get_downloaded_size(self.filename)

        headers = {'Range': f"bytes={self.downloaded_size}-"}
        response = requests.get(url, headers=headers, stream=True)

        if (verify_server_support_range(response.status_code)):
            with open(self.filename, "ab") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"Download completed: {self.filename}")
        else:
            print("The server does not support resumable downloads (Range).")

class DownloadsPool:
     def __init__(self):
        pass

d1 = DownloadManager("filename", url)
d1.download_file_with_range()