from os import environ
from pathlib import Path
from sys import exit

from portl import create_app
from portl.config import config_dict

get_config_mode = environ.get("PORTL_CONFIG_MODE", "Debug")

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit("Error: Invalid portl_CONFIG_MODE environment variable entry.")

app = create_app(Path.cwd(), config_mode)
