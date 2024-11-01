import config
import json
from dataclasses import dataclass
from jsonschema import validate
from helpers import check_if_file
from .schema import schema
from .utils import json_to_config, config_to_json

@dataclass
class ConfigManager:
    data = None
    is_all_positions_set = False

    def __init__(self):
        self.__read()

    def __read(self) -> None:
        if check_if_file(config.config_path):
            with open(config.config_path, 'r', encoding = 'utf-8') as config_file:
                config_json = json.load(config_file)
                validate(instance = config_json, schema = schema)
                self.data = config_json
                self.is_all_positions_set = json_to_config(config_json)

    def save(self) -> None:
        with open(config.config_path, 'w', encoding = 'utf-8') as config_file:
            config_file.write(json.dumps(config_to_json(), indent = 4))

def init() -> ConfigManager:
    res = ConfigManager()
    res.save()
    return res