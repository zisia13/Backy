
#text modes: onetime, loop

import os, sys, time, json
from typing import List, Union, TypeAlias
from colors import Colors
from exec_path import get_execution_path

c_colors = Colors()
exec_path: str = get_execution_path()

def exit_all(t:str = ""):
    c_colors.c_print(c_colors.RED, t)
    time.sleep(10)
    sys.exit(1)

def get_config_data():
    with open(os.path.join(exec_path, "config.json"), "r", encoding = "utf-8") as json_file:
        data = json_file.read()
    json_data = json.loads(data)
    return json_data

JSON_SETTINGS = get_config_data()

MODE: str = JSON_SETTINGS["mode"]
LOOP_INTERVAL: int = JSON_SETTINGS["loop_interval"]
PATH_1: str = JSON_SETTINGS["path1"]
PATH_2: str = JSON_SETTINGS["path2"]

#! check settings
if MODE not in ["onetime", "loop"]:
    exit_all("ERROR: Mode in config file should be: onetime or loop")
if type(LOOP_INTERVAL) != int:
    exit_all("ERROR: Loop Interval must be a int number")
if not os.path.exists(PATH_1):
    exit_all("ERROR: Path1 doesnt exist")
if not os.path.exists(PATH_2):
    exit_all("ERROR: Path2 doesnt exist")
