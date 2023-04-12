from config import Config
from models import *

config = Config()

def calc_indent_space() -> int:
    k_statistics = config.get_statistics_num()
    num_digits = len(str(k_statistics))
    return num_digits + 1

def get_packages_cnt():
    # TODO
    """
    """
    arch = config.get_arch()
    k_statistics = config.get_statistics_num()
    indent_space = calc_indent_space()
    package_name_space = config.get_package_name_space()
    files_num_space = config.get_files_num_space()
    index_number = 1

    downloader = Downloader(config)
    contents = downloader.download_contents_file()
    parser = Parser()
    package_counts = parser.parse_contents_file(contents)

    print(f"Top {k_statistics} packages with the most files for {arch}:\n")
    print(f"{'':<{indent_space}} {'Package name':<{package_name_space}} {'Num of files':<{files_num_space}}")
    
    for package, count in package_counts.most_common(k_statistics):
        print(f"{str(index_number) + '.':<{indent_space}} {package:<{package_name_space}} {count:<{files_num_space}}")
        index_number += 1