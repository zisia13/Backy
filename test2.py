import pythoncom
from win32com.client import Dispatch
import os



def get_everything_in_folder(device_name):
   
    folders = []
    
    try:
        # Shell initialisieren
        pythoncom.CoInitialize()
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)  # 17 = ssfDRIVES = Dieser PC
        
        # Durch alle Geräte unter "Dieser PC" iterieren
        for item in namespace.Items():
            if item.Name == device_name:
                try:
                    # In das Gerät navigieren
                    device_folder = item.GetFolder
                    
                    # Durch die Speicher des Geräts iterieren
                    for storage_item in device_folder.Items():

                        storage_folder = storage_item.GetFolder

                        for storage_file in storage_folder.Items():

                            print(storage_file)

                except:
                    pass
    except:
        pass

get_everything_in_folder("S24 Ultra von zisia13")










def get_folders_from_android_path(device_name, storage_name="Interner Speicher", android_folder="Android"):
    """
    Liest alle Ordner unter dem Android-Pfad eines Geräts aus
    
    :param device_name: Name des Android-Geräts (z.B. "S24 Ultra von zisia13")
    :param storage_name: Name des Speichers (z.B. "Interner Speicher")
    :param android_folder: Name des Android-Ordners (normalerweise "Android")
    :return: Liste der Ordner im Android-Verzeichnis
    """
    folders = []
    
    try:
        # Shell initialisieren
        pythoncom.CoInitialize()
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)  # 17 = ssfDRIVES = Dieser PC
        
        # Durch alle Geräte unter "Dieser PC" iterieren
        for item in namespace.Items():
            if item.Name == device_name:
                try:
                    # In das Gerät navigieren
                    device_folder = item.GetFolder
                    
                    # Durch die Speicher des Geräts iterieren
                    for storage_item in device_folder.Items():
                        if storage_item.Name == storage_name:
                            try:
                                # In den Speicher navigieren
                                storage_folder = storage_item.GetFolder
                                
                                # Durch die Ordner im Speicher iterieren
                                for android_item in storage_folder.Items():
                                    if android_item.Name == android_folder:
                                        try:
                                            # In den Android-Ordner navigieren
                                            android_folder_obj = android_item.GetFolder
                                            
                                            # Alle Unterordner im Android-Ordner auslesen
                                            for folder_item in android_folder_obj.Items():
                                                if folder_item.IsFolder:
                                                    folders.append({
                                                        'name': folder_item.Name,
                                                        'path': f"{device_name}\\{storage_name}\\{android_folder}\\{folder_item.Name}",
                                                        'type': 'Folder'
                                                    })
                                            
                                            break  # Android-Ordner gefunden, Schleife beenden
                                        except Exception as e:
                                            print(f"Fehler beim Zugriff auf Android-Ordner: {e}")
                                            folders.append({'error': f"Zugriff fehlgeschlagen: {e}"})
                                
                                break  # Speicher gefunden, Schleife beenden
                            except Exception as e:
                                print(f"Fehler beim Zugriff auf Speicher: {e}")
                                folders.append({'error': f"Zugriff auf Speicher fehlgeschlagen: {e}"})
                    
                    break  # Gerät gefunden, Schleife beenden
                except Exception as e:
                    print(f"Fehler beim Zugriff auf Gerät: {e}")
                    folders.append({'error': f"Zugriff auf Gerät fehlgeschlagen: {e}"})
    
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")
        folders.append({'error': f"Allgemeiner Fehler: {e}"})
    
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass
    
    return folders

def browse_android_device_interactive():
    """
    Interaktive Funktion zum Durchsuchen eines Android-Geräts
    """
    try:
        pythoncom.CoInitialize()
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)  # Dieser PC
        
        print("Verfügbare Geräte unter 'Dieser PC':")
        devices = []
        
        # Geräteliste erstellen
        for i, item in enumerate(namespace.Items()):
            devices.append(item)
            print(f"{i}: {item.Name}")
        
        if not devices:
            print("Keine Geräte gefunden!")
            return
        
        # Gerät auswählen
        try:
            selection = int(input("\nWähle ein Gerät (Nummer): "))
            selected_device = devices[selection]
            print(f"\nAusgewähltes Gerät: {selected_device.Name}")
            
            # Durch Gerät navigieren
            device_folders = selected_device.GetFolder
            print(f"\nVerfügbare Speicher auf {selected_device.Name}:")
            
            storages = []
            for i, storage in enumerate(device_folders.Items()):
                storages.append(storage)
                print(f"{i}: {storage.Name}")
            
            if not storages:
                print("Keine Speicher gefunden!")
                return
            
            # Speicher auswählen
            try:
                storage_selection = int(input("\nWähle einen Speicher (Nummer): "))
                selected_storage = storages[storage_selection]
                print(f"\nAusgewählter Speicher: {selected_storage.Name}")
                
                # Durch Speicher navigieren
                storage_folders = selected_storage.GetFolder
                print(f"\nOrdner in {selected_storage.Name}:")
                
                for i, folder in enumerate(storage_folders.Items()):
                    if folder.IsFolder:
                        print(f"{i}: [Ordner] {folder.Name}")
                    else:
                        print(f"{i}: [Datei] {folder.Name}")
                        
            except (ValueError, IndexError):
                print("Ungültige Auswahl für Speicher!")
                
        except (ValueError, IndexError):
            print("Ungültige Auswahl für Gerät!")
            
    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass



"""
# Beispielaufruf
if __name__ == "__main__":
    # Automatischer Versuch, den Android-Ordner zu finden
    device_name = "S24 Ultra von zisia13"  # Hier deinen Gerätenamen einsetzen
    print(f"Suche Ordner unter: {device_name}\\Interner Speicher\\Android")
    
    folders = get_folders_from_android_path(device_name)
    
    if folders:
        print(f"\nGefundene Ordner im Android-Verzeichnis:")
        for folder in folders:
            if 'error' in folder:
                print(f"FEHLER: {folder['error']}")
            else:
                print(f"- {folder['name']} (Pfad: {folder['path']})")
    else:
        print("Keine Ordner gefunden oder Zugriff nicht möglich!")
    
    # Interaktive Durchsicht anbieten
    print("\n" + "="*50)
    interactive = input("Möchtest du das Gerät interaktiv durchsuchen? (j/n): ")
    if interactive.lower() == 'j':
        browse_android_device_interactive()
"""