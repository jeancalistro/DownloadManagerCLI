import os, argparse, time
from download_manager import DownloadManager

dm = DownloadManager()

def wait_for_downloads():
    while True:
        downloads = dm.get_downloads()
        active = [d for d in downloads if d['status'] == 'Downloading']
        
        if not active:
            print("Todos os downloads foram concluídos!")
            break
        
        for download in active:
            size_mb = download['downloaded_size'] / (1024 * 1024)
            os.system("cls||clear")
            print(f"{download['id']} - {download['filename']}: {size_mb:.2f} MB")
        
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="Download Manager")
    parser.add_argument("command", type=str, choices=["new", "view", "resume", "pause"])
    parser.add_argument("-f", "--filename", type=str, required=False)
    parser.add_argument("-u", "--url-file", type=str, required=False)
    parser.add_argument("-d", "--download-id", type=str, required=False)
    args = parser.parse_args()
    
    match args.command:
        case "new":
            if args.filename and args.url_file:
                dm.new_download(args.filename, args.url_file)
                time.sleep(5)
                wait_for_downloads()
            else:
                print("Filename and URL file are required for new download.")
        case "view":
            downloads = dm.get_downloads()
            for download in downloads:
                print("\n------------------------------------------")
                print(f"ID: {download['id']}")
                print(f"Filename: {download['filename']}")
                print(f"URL: {download['url_file']}")
                print(f"Downloaded Size: {download['downloaded_size']} bytes")
                print(f"Status: {download['status']}")
                print("------------------------------------------\n")
        case "resume":
            if args.download_id:
                dm.resume_download(args.download_id)
                time.sleep(5)
                wait_for_downloads()
            else:
                print("Download ID is required to resume a download.")
        case "pause":
            if args.download_id:
                dm.pause_download(args.download_id)
            else:
                print("Download ID is required to pause a download.")

if __name__ == "__main__":
    main()