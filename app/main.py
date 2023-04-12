import argparse
from config import Config
from services.statistics import get_packages_cnt

def parse_args():
    """
    """
    settings = Config()
    parser = argparse.ArgumentParser(description="Debain contents indices statistical analyzer.")
    parser.add_argument("-a", "--arch",type=str, required=True, help="Target architecture of the contents indices file (e.g. amd64, arm64, mips64el, i386)")
    parser.add_argument("-s", "--source", type=str, default=settings.get_mirror_src(), help="Debian mirror source")
    parser.add_argument("-k", "--K",type=int, default=settings.get_statistics_num(), help="Output the statistics of the top K packages that have the most files associated with them.")
    args = parser.parse_args()
    return args

def update_settings(args):
    """
    """
    settings = Config()
    settings.set_arch(args.arch)
    settings.set_mirror_src(args.source)
    # TODO negative check
    settings.set_statistic_num(args.K)

def main():
    args = parse_args()
    update_settings(args)
    get_packages_cnt()


if __name__ == "__main__":
    main()