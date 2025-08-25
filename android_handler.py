from win32com.client import Dispatch
import psutil, shutil
from typing import List, TypeAlias, Optional
import pythoncom
import win32clipboard
import os, sys, time

from colors import Colors

IGNORABLE: TypeAlias = Optional[bool]

c_colors = Colors()

class Android_Handler:

    NOT_FOUND = "no_phone_found"

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

        if len(phone_names) == 0:
            phone_names.append(cls.NOT_FOUND)
            phone_paths.append(cls.NOT_FOUND)
          
        return (phone_names, phone_paths)

    @classmethod
    def copy_shell_item(cls, shell_item, destination_path) -> IGNORABLE:
        try:
            os.makedirs(os.path.dirname(destination_path), exist_ok = True)

            shell = Dispatch("Shell.Application")
            dest_namespace = shell.NameSpace(os.path.dirname(destination_path))

            if not dest_namespace:
                print(f"❌ Zielordner nicht gefunden: {os.path.dirname(destination_path)}")
                return False
            
            dest_namespace.CopyHere(shell_item)

            return True

        except Exception as e:
            print(f"❌ Kopieren fehlgeschlagen: {e}")
            return False

    @classmethod
    def clear_clipboard(cls) -> IGNORABLE:
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            return True
        except:
            return False

    @classmethod
    def get_internal_storage_name(cls, device_name: str) -> IGNORABLE:
        pythoncom.CoInitialize()
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)

        for item in namespace.Items():
            if item.Name == device_name:
                device_folder = item.GetFolder
        
                for storage_item in device_folder.Items():
                    storage_folder = storage_item.GetFolder

                    for storage_file in storage_folder.Items():
                        if storage_file.Name == "DCIM":
                            dcim_folder = storage_file.GetFolder
                        
                            for sub_folder in dcim_folder.Items():
                                c_colors.c_print(c_colors.GREEN, sub_folder.Name)

                                media_folder = sub_folder.GetFolder
                                if not str(sub_folder.Name) == "Screenshots":
                                    continue

                                for media in media_folder.Items():
                                    if not media.IsFolder: #! folder only
                                        print(media.Name)
                                        c_colors.c_print(c_colors.RED, media.Path)
                                        pc_path = r"C:\Users\AGL\Downloads\phone_media_folder_pc"
                                        destination_path = os.path.join(pc_path, media.Name)
                                    
                                        cls.clear_clipboard()
                                    
                                        cls.copy_shell_item(media, destination_path)
        
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

    Android_Handler.get_internal_storage_name(ph[0])
