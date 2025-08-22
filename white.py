import os, sys, time, json, shutil
from typing import List, Union, TypeAlias
from colors import Colors
from exec_path import get_execution_path

#text "mode" options: sync, transfer
#text "repeat" options: loop, onetime

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
REPEAT: str = JSON_SETTINGS["repeat"]
LOOP_INTERVAL: int = JSON_SETTINGS["loop_interval"]
PATH_1: str = JSON_SETTINGS["path1"]
PATH_2: str = JSON_SETTINGS["path2"]

#! check settings
if MODE not in ["sync", "transfer"]:
    exit_all("ERROR: Repeat in config file should be: sync or transfer")
if REPEAT not in ["onetime", "loop"]:
    exit_all("ERROR: Mode in config file should be: onetime or loop")
if type(LOOP_INTERVAL) != int:
    exit_all("ERROR: Loop Interval must be a int number")
if not os.path.exists(PATH_1):
    exit_all("ERROR: Path1 doesnt exist")
if not os.path.exists(PATH_2):
    exit_all("ERROR: Path2 doesnt exist")

def get_path_size(p: str) -> bool:
    return len(os.listdir(p))

class Progress_Bar:
    item_counter: int = 0
    sum_items: int = None
    all_items: list = []

    @classmethod
    def init(cls, items: list) -> None:
        cls.all_items = items
        cls.sum_items = len(items)
        cls.write(str(cls.all_items[cls.item_counter]))
        return None

    @classmethod
    def write(cls, text: str) -> None:
        sys.stdout.write('\r' + text)
        sys.stdout.flush()
        return None

    @classmethod
    def next(cls) -> None:
        cls.write(str(cls.all_items[cls.item_counter]))
        cls.item_counter += 1
        time.sleep(1)
        return None
    
    @classmethod
    def reset(cls) -> None:
        cls.item_counter = 0
        cls.sum_items = None
        cls.all_items = []
        return None

#! def main function
def sync(p1: str, p2: str, verbose: bool = False) -> None:
    
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

def transfer(p1: str, p2: str):
    
    Progress_Bar.init(os.listdir(p1))

    for file in os.listdir(p1):

        file_path = os.path.join(p1, file)
        copy_from_to(file_path, p2)
        Progress_Bar.next()
        try:
            os.remove(file_path)
        except PermissionError:
            print(c_colors.RED + f"No permission for file: {file}" + c_colors.WHITE)

#! start (select mode)
if REPEAT == "onetime":
    if MODE == "sync":
        sync(p1 = PATH_1, p2 = PATH_2)
        sync(p1 = PATH_2, p2 = PATH_1)
        
    elif MODE == "transfer":
        transfer(p1 = PATH_1, p2 = PATH_2)

    c_colors.c_print(c_colors.GREEN, "Finished, Exit...")

elif REPEAT == "loop":
    while True:
        if MODE == "sync":
            sync(p1 = PATH_1, p2 = PATH_2)
            sync(p1 = PATH_2, p2 = PATH_1)
            time.sleep(LOOP_INTERVAL)
            
        elif MODE == "transfer":
            transfer(p1 = PATH_1, p2 = PATH_2)
