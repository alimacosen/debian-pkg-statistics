from urllib.parse import urljoin
import requests
import gzip
from config import Config
import sys

class Downloader:
    # TODO
    """
    """
    def __init__(self, settings: Config) -> None:
        self.settings = settings

    def change_config(self, settings: Config) -> "Downloader":
        self.settings = settings
        return self
    
    def download_contents_file(self) -> str:
        # TODO description
        """
        """
        arch = self.settings.get_arch()
        base_url = self.settings.get_mirror_src()
        contents_url = urljoin(base_url, f"Contents-{arch}.gz")
        try:
            print(f"downloading Contents-{arch}.gz from {contents_url}\n...\n")
            response = requests.get(contents_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            sys.exit(f"Failed downloading Contents file:\n{e}")
        
        try:
            decompressed_contents = gzip.decompress(response.content).decode()
        except (TypeError, gzip.BadGzipFile, UnicodeDecodeError) as e:
            sys.exit(f"Error decompressing or decoding Contents file:\n{e}")
        return decompressed_contents