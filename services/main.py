import hashlib
import json
import logging.config
from settings import LOGGING_CONFIG


def generate_hash(string):
    hash_object = hashlib.sha256(string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def is_jsonable(data):
    try:
        json.dumps(data)
        return True
    except TypeError:
        return False


def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


def init_logger(app_name: str, config: dict = LOGGING_CONFIG) -> logging.Logger:
    logging.config.dictConfig(config)
    return logging.getLogger(app_name)
