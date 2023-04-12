from config import Config

config = Config()

def calc_indent_space() -> int:
    k_statistics = config.get_statistics_num()
    num_digits = len(str(k_statistics))
    return num_digits + 1