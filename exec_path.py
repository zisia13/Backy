import sys
import os

def get_execution_path() -> str:
    if getattr(sys, 'frozen', False): #! start from exe
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__)) #! start from vscode
    return script_dir