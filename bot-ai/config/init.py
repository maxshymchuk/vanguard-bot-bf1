import config
import json
from jsonschema import validate
from .schema import schema
from .utils import configure_positions, json_to_config, config_to_json

def init():
    if not config.config_path:
        return
    with open(config.config_path, 'r', encoding = 'utf-8') as config_file:
        config_json = json.load(config_file)
        validate(instance = config_json, schema = schema)
        is_all_positions_set = json_to_config(config_json)
        if not is_all_positions_set:
            configure_positions()
    with open(config.config_path, 'w', encoding = 'utf-8') as config_file:
        config_file.write(json.dumps(config_to_json(), indent = 4))