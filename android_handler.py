from win32com.client import Dispatch
import psutil
from typing import List

class Android_Handler:

    identifier_list = [
        "Android",
        "Samsung",
        "S1",
        "S2",
        "S3",
        "S4"
    ]

    def __init__(self):
        print(f"This class '{Android_Handler.__name__}' is not intended for an object, please use the classmethods...")
        raise SyntaxError()

    @classmethod
    def get_pc_drives(cls) -> List[str]:
        o = []
        ds = psutil.disk_partitions(all = False)
        for d in ds:
            o.append(str(d.device))
        return o
            
    @classmethod
    def scan_for_phones(cls) -> List[str]:
        all_drives = cls.get_pc_drives()
        phone_names = []
        phone_paths = []
      
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17) #! 17 = ssfDRIVES = This PC

        for item in namespace.Items():
            name = item.Name
            path = item.Path

            if path in all_drives:
                continue

            for identifier in cls.identifier_list:
                if (identifier in name) or (identifier in path):
                    phone_names.append(name)
                    phone_paths.append(path)
          
        return (phone_names, phone_paths)

    @classmethod
    def get_internal_storage_name(cls) -> str:
        pass

    @classmethod
    def get_every_folder_in_DCIM(cls) -> List[str]:
        pass
    
    @classmethod
    def copy_file(cls) -> bool:
        pass

    @classmethod
    def run(cls) -> None:
        pass

if __name__ == "__main__":
    ph, pa = Android_Handler.scan_for_phones()
    print(ph)
    print(pa)
    #for i in o:
    #    print(i)
