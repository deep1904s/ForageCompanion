import os
import yaml


class Config:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.BASE_DIR = os.path.abspath(cfg.get("base_dir", "."))
        self.MAX_CONTENT_LENGTH = cfg.get("max_content_length", 16 * 1024 * 1024)
        self.ALLOWED_EXTENSIONS = set(cfg.get("allowed_extensions", []))


app_config = Config()
