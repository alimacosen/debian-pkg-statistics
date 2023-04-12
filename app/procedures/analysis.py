from app.config import Config
from app.components import Downloader, Parser
from app.utils.utils import calc_indent_space

config = Config()


def get_packages_cnt() -> None:
    """ Organize each stage and show the output of the statistics.

        Args:
            None

        Returns:
            None
    """
    # get configuration: taeget architecture and top k number
    arch = config.get_arch()
    k_statistics = config.get_statistics_num()

    # output format
    indent_space = calc_indent_space()
    package_name_space = config.get_package_name_space()
    files_num_space = config.get_files_num_space()
    index_number = 1

    # main logics of analyzing the contents file.
    downloader = Downloader(config)
    contents = downloader.download_contents_file()
    parser = Parser()
    package_counts = parser.parse_contents_file(contents)

    # show statistics
    print(f"Top {k_statistics} packages with the most files for {arch}:\n")
    print(f"{'':<{indent_space}} {'Package name':<{package_name_space}} {'Num of files':<{files_num_space}}")
    for package, count in package_counts.most_common(k_statistics):
        print(f"{str(index_number) + '.':<{indent_space}} {package:<{package_name_space}} {count:<{files_num_space}}")
        index_number += 1
    print("\n")
