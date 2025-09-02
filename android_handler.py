from win32com.client import Dispatch
import psutil, shutil
from typing import List, TypeAlias, Optional, Tuple
import pythoncom
import win32clipboard
import os, sys, time
from datetime import datetime

from colors import Colors

IGNORABLE: TypeAlias = Optional[bool]

c_colors = Colors()

class Android_Handler:

    NOT_FOUND = "no_phone_found"
    PROGRESSBAR_ASCII_COMPLETE = c_colors.PASTELL_GREEN + "━" + c_colors._reset #"█"
    PROGRESSBAR_ASCII_FINISHED = c_colors.PASTELL_RED + "━" + c_colors._reset

    identifier_list = [
        "Android",
        "Samsung",
        "S1",
        "S2",
        "S3",
        "S4"
    ]

    DCIM_FOLDER_NAMES = [
        "Screenshots",
        "Camera"
    ]

    PC_SAVE_PATH = ""

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
    def copy_shell_item(cls, phone_file, destination_path) -> IGNORABLE:
        try:
            shell = Dispatch("Shell.Application")
            dest_namespace = shell.NameSpace(os.path.dirname(destination_path))
            if not dest_namespace:
                return False
            dest_namespace.CopyHere(phone_file)
            return True
        except:
            return False
        
    @classmethod
    def delete_shell_item(cls, device_name: str, wanted_folder_name: str) -> bool:
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
                                if str(sub_folder.Name) == str(wanted_folder_name):
                                    try:
                                        sub_folder.InvokeVerb("delete")
                                        return True
                                    except:
                                        return False

    @classmethod
    def get_existing_folders_in_DCIM_folder(cls, device_name: str) -> List[str]:
        pythoncom.CoInitialize()
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)

        DCIM_folders = []

        for item in namespace.Items():
            if item.Name == device_name:
                device_folder = item.GetFolder
                for storage_item in device_folder.Items():
                    storage_folder = storage_item.GetFolder
                    for storage_file in storage_folder.Items():
                        if storage_file.Name == "DCIM":
                            dcim_folder = storage_file.GetFolder
                            for folder in dcim_folder.Items():
                                DCIM_folders.append(str(folder))

        return DCIM_folders    

    @classmethod
    def check_if_media_folder_exists(cls, device_name: str, wanted_folder_name: str) -> bool:
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
                            if wanted_folder_name in dcim_folder.Items():
                                return True
                            else:
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
    def get_DCIM_folder_content(cls, device_name: str, wanted_folder_name: str) -> IGNORABLE:
        pythoncom.CoInitialize()
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)

        media_list = []

        for item in namespace.Items():
            if item.Name == device_name:
                device_folder = item.GetFolder
                for storage_item in device_folder.Items():
                    storage_folder = storage_item.GetFolder
                    for storage_file in storage_folder.Items():
                        if storage_file.Name == "DCIM":
                            dcim_folder = storage_file.GetFolder
                            for sub_folder in dcim_folder.Items():
                                media_folder = sub_folder.GetFolder
                                if sub_folder.Name == wanted_folder_name:
                                    for media in media_folder.Items():
                                        if not media.IsFolder: #! folder only
                                            media_list.append(media)
                                        else:
                                            c_colors.c_print(c_colors.YELLOW, f"INFO: Folder: {media.Name} found in {sub_folder.Name}")
                                else:
                                    continue
                        else:
                            continue
            else:
                continue

        return media_list    
                                    
    @classmethod
    def create_media_destination_path(cls, media) -> str:
        return os.path.join(cls.PC_SAVE_PATH, media.Name)
        
    @classmethod
    def get_every_folder_in_DCIM(cls) -> List[str]:
        pass
    
    @classmethod
    def copy_file(cls) -> bool:
        pass

    @classmethod
    def progress_bar(cls, current: str, current_name: str, total: int, width: int, longest_name: int):
        if len(str(current_name)) < longest_name:
            diff = longest_name - len(str(current_name))
            current_name = str(current_name) + str(" " * diff)

        i = total - (total - current)
        percent = i / total
        filled = int(width * percent)
        if int(current) == int(total):
            space = ""
        else:
            space = " "

        bar = cls.PROGRESSBAR_ASCII_COMPLETE * filled + space + cls.PROGRESSBAR_ASCII_FINISHED * (width - filled)
            
        sys.stdout.write(f'\r[{bar}] {current}/{total} {percent * 100:.1f}% File: {c_colors.PURPLE}{current_name}{c_colors._reset}')
        sys.stdout.flush()
        time.sleep(0.01)

    #! wtf is this cancer just delete it or something
    #todo FINISH THIS METHOD
    @classmethod
    def end_progress_bar(cls, current: str, current_name: str, total: int, width: int, longest_name: int) -> None:
        if len(str(current_name)) < longest_name:
            diff = longest_name - len(str(current_name))
            current_name = str(current_name) + str(" " * diff)

        i = total - (total - current)
        percent = i / total
        ausgefuellt = int(width * percent)
        balken = '█' * ausgefuellt + '-' * (width - ausgefuellt)
            
        sys.stdout.write(f'\r[{balken}] {current}/{total} {percent*100:.1f}% File: {current_name}')
        sys.stdout.flush()
        time.sleep(0.1)

    @staticmethod
    def hide_CLI_cursor():
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_CLI_cursor():
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @classmethod
    def run(cls) -> None:

        #! hide cli cursor
        Android_Handler.hide_CLI_cursor()

        #! init CLI color system
        os.system("") 

        #! get device name
        device_names, phone_paths = cls.scan_for_phones()
        if len(device_names) > 1:
            c_colors.c_print(c_colors.RED, "ERROR: Multiple Phones found... (select feature will come later)")
        elif device_names[0] == cls.NOT_FOUND:
            c_colors.c_print(c_colors.RED, "No Phone Found!")
            time.sleep(10)
            sys.exit(1)
        else:
            selected_phone = device_names[0]
            print(c_colors.WHITE + "Phone Found: " + c_colors.PURPLE + selected_phone + c_colors._reset)

        #! check how many folders exist on phone
        existing_folders_before = cls.get_existing_folders_in_DCIM_folder(device_name = selected_phone)
        #for folder in cls.DCIM_FOLDER_NAMES:
        #    if cls.check_if_media_folder_exists(device_name = selected_phone, wanted_folder_name = folder):
        #        existing_folders_before.append(folder)

        #! get medias in folders
        all_medias = []

        for folder in cls.DCIM_FOLDER_NAMES:
            medias = cls.get_DCIM_folder_content(device_name = selected_phone, wanted_folder_name = folder)
            amount_of_medias = int(len(medias))
            print(c_colors.WHITE + f"Medias in {folder}: " + c_colors.PURPLE + str(amount_of_medias) + c_colors._reset)
            for media in medias:
                all_medias.append(media)

        #! get longest string element of media
        longest_media_name = 0
        for media in all_medias:
            name = media.Name
            if len(name) > longest_media_name:
                longest_media_name = len(name)

        #! copy medias
        copied_medias = 0
        
        for media in all_medias:
            try:
                cls.copy_shell_item( #todo add security feature here check return value
                    phone_file = media, 
                    destination_path = cls.create_media_destination_path(media = media)
                )
                cls.clear_clipboard()
                copied_medias += 1 #todo add security feature here
            except:
                pass

            cls.progress_bar(
                total = len(all_medias),
                current = copied_medias,
                current_name = media,
                width = 30,
                longest_name = longest_media_name
            )

        #! remove folders
        if len(all_medias) == copied_medias:
            print("\nPlease confirm the request for folder deletion...")
            for folder in cls.DCIM_FOLDER_NAMES:
                cls.delete_shell_item(device_name = selected_phone, wanted_folder_name = folder)
        else:
            print("\nNo folder will be removed because of an internal error...")
            print(f"All Medias: {len(all_medias)}")
            print(f"Copied medias: {copied_medias}")
            print(c_colors._reset)

        #! get removed folders
        removed_folders = []
        for folder in cls.DCIM_FOLDER_NAMES:
            if not cls.check_if_media_folder_exists(device_name = selected_phone, wanted_folder_name = folder):
                removed_folders.append(folder)
        
        #! print removed and existing folders
        removed_folders_string = ""
        remaining_folders_string = ""

        for folder in removed_folders:
            removed_folders_string += folder + " "

        for folder in existing_folders_before:
            if not folder in removed_folders:
                remaining_folders_string += folder + ""

        print(f"{c_colors.WHITE}Removed Folders: {c_colors.PURPLE}{removed_folders_string}{c_colors._reset}")
        print(f"{c_colors.WHITE}Remaining Folders: {c_colors.PURPLE}{remaining_folders_string}{c_colors._reset}")

        #! show CLI cursor
        Android_Handler.show_CLI_cursor()

class Time_Handler:

    @classmethod
    def get_date(cls) -> str:
        now = datetime.now()
        date = now.strftime("%d_%m_%y")
        return date

    @classmethod
    def get_time(cls) -> str:
        now = datetime.now()
        time = now.strftime("%H_%M_%S")
        return time

if __name__ == "__main__":

    login_name = os.getlogin()

    if login_name == "zisia13":
        _date = Time_Handler.get_date()
        _time = Time_Handler.get_time()
        folder_name = "D_" + _date + "___" + _time

        base_path = rf"A:\Backup\Handy Bilder\S24 Ultra\WHITE_AUTOBACKUP_MEDIA"
        folder_path = os.path.join(base_path, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        Android_Handler.PC_SAVE_PATH = folder_path
        Android_Handler.run()
        sys.exit(1)

    else:
        Android_Handler.PC_SAVE_PATH = rf"C:\Users\{login_name}\Downloads\phone_media_folder_pc"
        Android_Handler.run()
        sys.exit(1)
