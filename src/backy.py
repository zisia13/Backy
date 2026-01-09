import os, sys, time
from banner import BANNER
from colors import Colors
from utils import Android_Handler
from database import Database
from config import load_config

#! get exec path
def get_execution_path() -> str:
    if getattr(sys, 'frozen', False): #! start from exe
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__)) #! start from vscode
    return script_dir

#! get config data
config_path = os.path.join(get_execution_path(), "config.json")
config_data = load_config(config_path)

#! global vars
SAVE_PATH = config_data["DCIM_transfer"]["save_path"]
DATABASE_PATH = os.path.join(SAVE_PATH, config_data["DCIM_transfer"]["database_name"])
FOLDERS_TO_BACKUP = config_data["DCIM_transfer"]["folders_to_backup"]
IDENTIFIER_LIST = config_data["DCIM_transfer"]["identifier_list"]

#! check if save path exists
if not os.path.exists(SAVE_PATH):
    print("Save path doesnt exists, check your config file and make sure the path is correct.")
    time.sleep(10)
    sys.exit()

#! create objects
colors = Colors()
database = Database(DATABASE_PATH)

#! start
if __name__ == "__main__":
    
    #! init win ansii and clear console
    os.system("cls")

    #! print banner
    print(BANNER)
    print(colors._reset)
    input()
    sys.exit()
    #! set color class to handler
    Android_Handler.init(
        colors_obj = colors,
        SAVE_PATH = SAVE_PATH,
        DCIM_folder_names = FOLDERS_TO_BACKUP,
        database = database,
        identifier_list = IDENTIFIER_LIST
    )

    #! run   
    Android_Handler.run()
    try: database.close()
    except: pass
    input()
