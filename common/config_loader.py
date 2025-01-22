import yaml
from pathlib import Path

class ConfigLoader:
    @staticmethod
    def load_config():
        config_path = f"{str(Path(__file__).parent.parent)}/config/config.yaml"
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)