import json

class Config:
    """
    The global setting of this application.
    """
    _instance = None
    _config_file_path = "./config.json"
    _config = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self):
        with open(Config._config_file_path, "r") as config_file:
            self._config = json.loads(config_file.read())

    def get_arch(self) -> str:
        return self._config["arch"]
    
    def get_mirror_src(self) -> str:
        return self._config["debian_mirror_src"]
    
    def get_statistics_num(self) -> int:
        return self._config["top_k_statistic"]
    
    def get_package_name_space(self) -> int:
        return self._config["package_name_space"]
    
    def get_files_num_space(self) -> int:
        return self._config["files_num_space"]
    
    def set_arch(self, arch):
        self._config["arch"] = arch
    
    def set_mirror_src(self, mirror_src):
        self._config["debian_mirror_src"] = mirror_src

    def set_statistic_num(self, num):
        self._config["top_k_statistic"] = num
