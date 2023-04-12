from collections import Counter

class Parser:
    def __init__(self):
        pass
        # TODO

    def parse_contents_file(self, contents: str) -> Counter:
        # TODO
        """
        As it is described in https://wiki.debian.org/DebianRepository/Format?action=show&redirect=RepositoryFormat#A.22Translation.22_indices ,
        Clients should ignore lines not conforming to this scheme. Clients should correctly handle file names containing white space characters
        """
        package_counts = Counter()
        for line in contents.splitlines():
            columns = line.strip().split()
            if len(columns) != 2:
                continue
            packages = columns[1].split(",")
            for package in packages:
                package_counts[package] += 1
        return package_counts