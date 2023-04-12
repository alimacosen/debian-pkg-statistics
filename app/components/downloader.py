from urllib.parse import urljoin
import requests
import gzip
from app.config import Config
import sys


class Downloader:
    """Debian contents gzip file downloader.

    This class aims to download target file from assigned source, and the downloading configuration can be changed.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def change_config(self, config: Config) -> "Downloader":
        self.config = config
        return self

    def download_contents_file(self) -> str:
        """Download target gzip file from assigned source and decompress it into a string.

        Args:
            None

        Returns:
            decompressed_contents (str): Decompressed and decoded contents.
        """
        arch = self.config.get_arch()
        base_url = self.config.get_mirror_src()
        contents_url = urljoin(base_url, f"Contents-{arch}.gz")

        # Use requests.get to download the bytes file included in the response
        try:
            print(f"Downloading Contents-{arch}.gz from {contents_url} ...\n")
            response = requests.get(contents_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            sys.exit(f"Failed downloading Contents file. Error details: {e}")

        # Decompress the file and decode it to string variable
        try:
            decompressed_contents = gzip.decompress(response.content).decode()
        except (TypeError, gzip.BadGzipFile, UnicodeDecodeError) as e:
            sys.exit(f"Failed decompressing or decoding Contents file. Error details: {e}")
        return decompressed_contents
