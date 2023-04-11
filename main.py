import argparse
from settings import Settings

def parse_args():
    """
    """
    settings = Settings()
    parser = argparse.ArgumentParser(description="Debain contents indices statistical analyzer.")
    parser.add_argument("-a", "--arch",type=str, default=settings.get_arch(), help="Target architecture of the contents indices file (e.g. amd64, arm64, mips64el, i386)")
    parser.add_argument("-s", "--source", type=str, default=settings.get_mirror_src(), help="Debian mirror source")
    parser.add_argument("-k", "--K",type=int, default=settings.get_statistics_num(), help="Output the statistics of the top K packages that have the most files associated with them.")
    args = parser.parse_args()
    return args

def update_settings(args):
    """
    """
    settings = Settings()
    settings.set_arch(args.arch)
    settings.set_mirror_src(args.source)
    settings.set_statistic_num(args.K)

def main():
    args = parse_args()
    update_settings(args)
    settings = Settings()
    print(settings._config)


if __name__ == "__main__":
    main()