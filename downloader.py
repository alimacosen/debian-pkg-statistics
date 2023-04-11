from urllib.parse import urljoin
import requests
import gzip
from settings import Settings

class Downloader:
    def __init__(self, settings: Settings):
        self.settings = settings

    def change_config(self, settings: Settings):
        self.settings = settings
        return self
    
    def download_contents_file(self) -> str:
        # TODO modify the description
        """
        Download and decompress the Contents file for the given architecture.

        :param architecture: Architecture string, e.g., 'amd64', 'arm64', 'mips', etc.
        :param base_url: Base URL of the Debian mirror
        :return: Decompressed Contents file as a string
        """
        arch = self.settings.get_arch()
        base_url = self.settings.get_mirror_src()
        contents_url = urljoin(base_url, f"Contents-{arch}.gz")
        try:
            response = requests.get(contents_url)
            print(f"downloading Contents-{arch}.gz from {contents_url}\n...\n")  # TODO figure out if there's a better way to show prompt
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading Contents file: {e}")  # TODO figure out if there's a better way to show prompt
            exit(1)  # TODO find out a proper exit code
        
        try:
            decompressed_contents = gzip.decompress(response.content).decode()
        except (gzip.BadGzipFile, UnicodeDecodeError) as e:
            print(f"Error decompressing or decoding Contents file")  # TODO figure out if there's a better way to show prompt
            exit(1)  # TODO find out a proper exit code

        return decompressed_contents