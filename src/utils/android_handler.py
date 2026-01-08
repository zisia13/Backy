from win32com.client import Dispatch
import psutil, shutil
from typing import List, TypeAlias, Optional, Tuple
import pythoncom
import win32clipboard
import os, sys, time
import tempfile

try: from hash import get_file_hash
except: from .hash import get_file_hash

IGNORABLE: TypeAlias = Optional[bool]

class Android_Handler:

    PC_SAVE_PATH = None
    c_colors = None
    theme_color = None
    PROGRESSBAR_ASCII_COMPLETE = None
    PROGRESSBAR_ASCII_FINISHED = None
    db = None

    NOT_FOUND = "no_phone_found"

    identifier_list = [
        "Android",
        "Samsung",
        "S1",
        "S2",
        "S3",
        "S4"
    ]

    DCIM_FOLDER_NAMES = []

    def __init__(self):
        print(f"This class '{Android_Handler.__name__}' is not intended for an object, please use the classmethods...")
        raise SyntaxError()

    @classmethod
    def init(cls, colors_obj, pc_save_path: str, database, DCIM_folder_names: List[str]):
        cls.DCIM_FOLDER_NAMES = DCIM_folder_names
        cls.db = database
        cls.PC_SAVE_PATH = pc_save_path
        cls.c_colors = colors_obj
        cls.PROGRESSBAR_ASCII_COMPLETE = cls.c_colors.PASTELL_GREEN + "━" + cls.c_colors._reset #"█"
        cls.PROGRESSBAR_ASCII_FINISHED = cls.c_colors.PASTELL_RED + "━" + cls.c_colors._reset
        cls.theme_color = cls.c_colors._theme_color

    @classmethod
    def get_pc_drives(cls) -> List[str]:
        o = []
        ds = psutil.disk_partitions(all = False)
        for d in ds:
            o.append(str(d.device))
        return o
            
    @classmethod
    def scan_for_phones(cls) -> Tuple[List[str], List[str]]:
        all_drives = cls.get_pc_drives()
        phone_names = []
        phone_paths = []
      
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17) #! 17 = DRIVES = This PC

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
                            for item in dcim_folder.Items():
                                if str(item.Name) == wanted_folder_name:
                                    return True
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
                                            cls.c_colors.c_print(cls.c_colors.YELLOW, f"INFO: Folder: {media.Name} found in {sub_folder.Name}")
        return media_list    
                                    
    @classmethod
    def create_media_destination_path(cls, media) -> str:
        return os.path.join(cls.PC_SAVE_PATH, media)

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

        sys.stdout.write(f'\r[{bar}] {current}/{total} {percent * 100:.1f}% File: {cls.theme_color}{current_name}{cls.c_colors._reset}')
        sys.stdout.flush()
        sys.stdout.write("\033[A")
        time.sleep(0.01)

    @staticmethod
    def hide_CLI_cursor():
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_CLI_cursor():
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @classmethod
    def copy_media(cls, temp_dir: str, media_dir: str):
        try:
            shutil.copy2(temp_dir, media_dir)
        except Exception as copy_error:
            print(copy_error)
            raise SystemError()
        
    @classmethod
    def rename_file(cls, file_path: str, file_name: str):
        old_file_path = os.path.join(file_path, file_name)

        #! get unix timestamp
        addition = str(int(time.time())) #! convert to int first bc time() returns a float

        #! create new file path
        new_file_path = os.path.join(file_path, addition + "-" + file_name)

        #! rename file
        os.rename(old_file_path, new_file_path)

        return new_file_path

    @classmethod
    def get_file_name(cls, file_path: str) -> str:
        return os.path.basename(file_path)
        
    @classmethod
    def run(cls) -> None:

        #! hide cli cursor
        Android_Handler.hide_CLI_cursor()

        #! get device name
        device_names, phone_paths = cls.scan_for_phones()
        if len(device_names) > 1:
            cls.c_colors.c_print(cls.c_colors.RED, "ERROR: Multiple Phones found... (select feature will come later)")
        elif device_names[0] == cls.NOT_FOUND:
            cls.c_colors.c_print(cls.c_colors.RED, "No Phone Found!")
            time.sleep(10)
            sys.exit(1)
        else:
            selected_phone = device_names[0]
            print(cls.c_colors.WHITE + "Phone Found: " + cls.theme_color + selected_phone + cls.c_colors._reset)

        #! get medias in folders
        all_medias = []
        for folder in cls.DCIM_FOLDER_NAMES:
            if cls.check_if_media_folder_exists(selected_phone, folder):
                medias = cls.get_DCIM_folder_content(device_name = selected_phone, wanted_folder_name = folder)
                amount_of_medias = int(len(medias))
                print(cls.c_colors.WHITE + f"Medias in {folder}: " + cls.theme_color + str(amount_of_medias) + cls.c_colors._reset)
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
        with tempfile.TemporaryDirectory() as temp_media_dir:
            for media_obj in all_medias:
                #! copy media to temp path
                media = str(media_obj.Name)
                destination_path = cls.create_media_destination_path(media = media)
                temp_media_path = os.path.join(temp_media_dir, media)
                copy_success_state = cls.copy_shell_item(
                    phone_file = media_obj, 
                    destination_path = temp_media_path
                )
                cls.clear_clipboard()

                #! get hash and filename of media
                media_hash = get_file_hash(temp_media_path)
                file_name = cls.get_file_name(temp_media_path)

                #! add hash and filename to db and check
                if copy_success_state:

                    #! check hash
                    if cls.db.check(cls.db.hash_column_name, media_hash):
                        os.remove(temp_media_path)
                    else:
                        cls.db.save(cls.db.hash_column_name, media_hash)

                        #! check filename
                        new_media_path = None
                        if cls.db.check(cls.db.filename_column_name, file_name):
                            new_media_path = cls.rename_file(temp_media_dir, file_name)
                            new_destination_path = cls.create_media_destination_path(cls.get_file_name(new_media_path))
                        else:
                            cls.db.save(cls.db.filename_column_name, file_name)

                        #! check if it got renamed
                        if new_media_path == None:
                            cls.copy_media(temp_media_path, destination_path)
                            os.remove(temp_media_path)
                        else:
                            cls.copy_media(new_media_path, new_destination_path)
                            os.remove(new_media_path)
                  
                #! continue with progress bar
                if copy_success_state:
                    copied_medias += 1

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
            print(cls.c_colors._reset)

        #! get removed folders
        removed_folders = []
        for folder in cls.DCIM_FOLDER_NAMES: 
            if not cls.check_if_media_folder_exists(device_name = selected_phone, wanted_folder_name = folder):
                removed_folders.append(folder)
        
        #! print removed and existing folders
        removed_folders_string = ""

        for folder in removed_folders:
            removed_folders_string += folder + " "

        if removed_folders == []:
            print(f"{cls.c_colors.WHITE}Removed Folders: {cls.theme_color}Nothing deleted{cls.c_colors._reset}")
        else:
            print(f"{cls.c_colors.WHITE}Removed Folders: {cls.theme_color}{removed_folders_string}{cls.c_colors._reset}")

        #! show CLI cursor
        Android_Handler.show_CLI_cursor()

        #! close database
        try: cls.db.close()
        except: pass
