import config
import json
from dataclasses import dataclass
from jsonschema import validate
from .schema import schema
from .utils import json_to_config, config_to_json

@dataclass
class ConfigResult:
    is_all_positions_set = False

def init() -> ConfigResult:
    res = ConfigResult()
    if config.config_path:
        with open(config.config_path, 'r', encoding = 'utf-8') as config_file:
            config_json = json.load(config_file)
            validate(instance = config_json, schema = schema)
            res.is_all_positions_set = json_to_config(config_json)
        with open(config.config_path, 'w', encoding = 'utf-8') as config_file:
            config_file.write(json.dumps(config_to_json(), indent = 4))
    return res