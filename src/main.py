import os, sys
from banner import BANNER
from colors import Colors
from utils import Android_Handler
from database import Database
from config import get_config

#! get exec path
def get_execution_path() -> str:
    if getattr(sys, 'frozen', False): #! start from exe
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__)) #! start from vscode
    return script_dir

#! get config data
config_path = os.path.join(get_execution_path(), "config.json")
config_data = get_config(config_path)

#! global vars
PC_SAVE_PATH = config_data["DCIM_transfer"]["save_path"]
DATABASE_PATH = os.path.join(PC_SAVE_PATH, config_data["DCIM_transfer"]["database_name"])

colors = Colors()
database = Database(DATABASE_PATH)

#! start
if __name__ == "__main__":
    
    #! init win ansii
    os.system("")

    #! print banner
    print(BANNER)
    print(colors._reset)

    #! set color class to handler
    Android_Handler.init(
        colors_obj = colors,
        pc_save_path = PC_SAVE_PATH,
        DCIM_folder_names = config_data["DCIM_transfer"]["folders_to_backup"],
        database = database
    )

    #! run   
    Android_Handler.run()
    try: database.close()
    except: pass
