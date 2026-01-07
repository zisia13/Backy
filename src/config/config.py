import os, json
from typing import Dict, Any

def load_config(config_file_path: str) -> Dict[str, Any]:
    if os.path.exists(config_file_path):
        with open(config_file_path, "r", encoding = "utf-8") as config_file:
            config_data = config_file.read()
        return json.loads(config_data)
    else:
        raise ValueError("Path to config file doesnt exist")