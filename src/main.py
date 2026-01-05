import os

from banner import BANNER
from colors import Colors
from utils import Android_Handler, get_execution_path

#! global
exec_path = get_execution_path()
login_name = os.getlogin()
colors = Colors()

if __name__ == "__main__":
    
    #! init win ansii
    os.system("")

    #! print banner
    print(BANNER)
    print(colors._reset)

    #! set color class to handler
    Android_Handler.init(
        colors_obj = colors,
        pc_save_path = r"S:\_GITHUB\White\test"
    )

    #! run   
    Android_Handler.run()

    #todo close the database connection
