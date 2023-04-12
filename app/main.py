import argparse
from config import Config
from services.statistics import get_packages_cnt

def parse_args() -> argparse.Namespace:
    # TODO
    """
    """
    settings = Config()
    minimum_statistic_num = settings.get_minimum_statistic_num()
    statistics_num = settings.get_statistics_num()
    mirror_src = settings.get_mirror_src()

    parser = argparse.ArgumentParser(description=f"Debain contents indices statistical analyzer. Output the statistics of the top K (default by {statistics_num}) packages that have the most files associated with them.")
    parser.add_argument("-a", "--arch",type=str, required=True, help="Target architecture of the contents indices file (e.g. amd64, arm64, mips64el, i386)")
    parser.add_argument("-s", "--source", type=str, default=settings.get_mirror_src(), help=f"Debian repository mirror source, defualt by {mirror_src}")
    parser.add_argument("-k", "--K",type=int, default=settings.get_statistics_num(), help=f"Top k packages information, must be greater than or equal to {minimum_statistic_num}")
    args = parser.parse_args()
    if args.K < minimum_statistic_num:
        parser.error("number must be greater than or equal to 1")

    return args

def update_settings(args: argparse.Namespace) -> None:
    # TODO
    """
    """
    settings = Config()
    settings.set_arch(args.arch)
    settings.set_mirror_src(args.source)
    settings.set_statistic_num(args.K)

def main():
    args = parse_args()
    update_settings(args)
    get_packages_cnt()


if __name__ == "__main__":
    main()