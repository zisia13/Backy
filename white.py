import os, sys, time, json, shutil
from typing import List, Union, TypeAlias
from colors import Colors
from exec_path import get_execution_path

#! create objects
c_colors = Colors()
exec_path: str = get_execution_path()

#! def functions
def exit_all(t:str = ""):
    c_colors.c_print(c_colors.RED, t)
    time.sleep(10)
    sys.exit(1)

def get_config_data():
    with open(os.path.join(exec_path, "config.json"), "r", encoding = "utf-8") as json_file:
        data = json_file.read()
    json_data = json.loads(data)
    return json_data


def copy_from_to(from_path: str, to_path: str) -> None:
    shutil.copy(from_path, to_path) #! copy file from - to

#! get settings from json file
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

#! def main function
def compare(p1: str, p2: str, verbose: bool = False) -> None:
    
    #! get all files in paths
    p1_items = set(os.listdir(p1))
    p2_items = set(os.listdir(p2))
    
    #! "compare" files and get only needed
    only_in_p1 = p1_items - p2_items
    
    #! copy missing files
    for item in only_in_p1:
        p1_item = os.path.join(p1, item)
        p2_item = os.path.join(p2, item)
        
        if os.path.isdir(p1_item):
            shutil.copytree(p1_item, p2_item)
            if verbose:
                c_colors.c_print(c_colors.YELLOW, f"Copied directory: {item}")
        else:
            shutil.copy2(p1_item, p2_item)
            if verbose:
                c_colors.c_print(c_colors.YELLOW, f"Copied file: {item}")



#! start (select mode)
if MODE == "onetime":
    compare(p1 = PATH_1, p2 = PATH_2)
    compare(p1 = PATH_2, p2 = PATH_1)
    c_colors.c_print(c_colors.GREEN, "Finished, Exit...")

elif MODE == "loop":
    while True:
        compare(p1 = PATH_1, p2 = PATH_2)
        compare(p1 = PATH_2, p2 = PATH_1)
        time.sleep(LOOP_INTERVAL)
