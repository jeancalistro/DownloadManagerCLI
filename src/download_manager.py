import urllib.request
import threading
import uuid
import json
import os

class DownloadManager:
    def __init__(self):
        self.downloads = self.retrieve_downloads()

    def get_downloads(self):
        return self.downloads

    def set_download(self, download):
        self.downloads.append(download)

    def get_download_by_id(self, download_id):
        for download in self.get_downloads():
            if download["id"] == download_id:
                return download

    def verify_server_support_range(self, status_code):
        if status_code == 206:
            return True
        return False

    def get_downloaded_size(self, filename):
        if os.path.exists(filename):
            return os.path.getsize(filename)
        return 0

    def generate_download_id(self):
        return str(uuid.uuid4())

    def persist_all_downloads_data(self, downloads):
        with open("outputs/downloads.json", "w") as f:
            json.dump([download for download in downloads], f, indent=4)

    def retrieve_downloads(self):
        try:
            with open("outputs/downloads.json", "r") as f:
                downloads_data = json.load(f)
                downloads = [dict(data) for data in downloads_data]
        except FileNotFoundError:
            downloads = []
        return downloads

    def update_download_status(self, download, status):
        download["status"] = status
        self.persist_all_downloads_data(self.get_downloads())

    def new_download(self, filename, url_file):
        download = dict (
            id = self.generate_download_id(),
            filename = filename,
            url_file = url_file,
            downloaded_size = 0,
            status = "")
        
        self.set_download(download)
        download_thread = threading.Thread(target=self.start_download, args=(download,), daemon=True)
        download_thread.start()
        self.update_download_status(download, "Downloading")
        print(f"Download {download['id']} Started.")

    def resume_download(self, download_id):
        download = self.get_download_by_id(download_id)
        if download:
            download["downloaded_size"] = self.get_downloaded_size(download["filename"])
            download_thread = threading.Thread(target=self.start_download, args=(download,), daemon=True)
            download_thread.start()
            self.update_download_status(download, "Downloading")
            print(f"Download {download_id} resumed.")
            return
        print("Download ID not found.")

    def pause_download(self, download_id):
        download = self.get_download_by_id(download_id)
        if download:
            self.update_download_status(download, "Paused")
            print(f"Download {download_id} paused.")
        else:
            print("Download ID not found.")

    def start_download(self, download):
        if download["status"] == "Completed":
            print("Download already completed.")
            return

        req = urllib.request.Request(download["url_file"])
        if download["downloaded_size"] > 0:
            req.add_header("Range", f"bytes={download['downloaded_size']}-")

        with urllib.request.urlopen(req) as res:
            if not self.verify_server_support_range(res.code):
                print("Server does not support resuming downloads.")

            with open(download["filename"], "ab") as output_file:
                while download["status"] != "Paused":
                    chunk = res.read(1024 * 1024)
                    if not chunk:
                        self.update_download_status(download, "Completed")
                        break
                    output_file.write(chunk)
                    download["downloaded_size"] += len(chunk)