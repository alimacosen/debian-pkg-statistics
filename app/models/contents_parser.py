from collections import Counter


class Parser:
    """Debian contents file parser

    This class aims to properly parse the decompressed and decoded contents file.
    """

    def __init__(self) -> None:
        pass

    def parse_contents_file(self, contents: str) -> Counter:
        """process contents and do the statistics of each package.

        Args:
            contents (str): The decompressed and decoded contents file.
            
        Returns:
            package_counts (Counter): The statistics result. <key : value> is <package name : number of files related to this package>
        """
        print("Parsing the contents ...\n")
        package_counts = Counter()
        for line in contents.splitlines():
            columns = line.strip().split()
            # As it is described in https://wiki.debian.org/DebianRepository/Format?action=show&redirect=RepositoryFormat#A.22Translation.22_indices
            # Clients should ignore lines not conforming to this scheme.
            if len(columns) != 2:
                continue
            packages = columns[1].split(",")
            for package in packages:
                package_counts[package] += 1
        return package_counts
