import pythoncom
from win32com.client import Dispatch
import os

def get_all_devices_in_this_pc():
    """
    Gibt alle Geräte unter 'Dieser PC' zurück, inklusive Android-Geräte
    """
    devices = []
    
    try:
        # Shell initialisieren
        shell = Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)  # 17 = ssfDRIVES = Dieser PC
        
        # Durch alle Elemente iterieren
        for item in namespace.Items():
            device_name = item.Name
            device_path = item.Path if hasattr(item, 'Path') else ""
            
            # Besondere Behandlung für Android-Geräte
            if "Android" in device_name or "S2" in device_name or "S3" in device_name:
                # Versuche, Unterordner zu finden
                try:
                    for sub_item in item.GetFolder.Items():
                        sub_name = sub_item.Name
                        sub_path = sub_item.Path if hasattr(item, 'Path') else ""
                        full_path = f"{device_name}\\{sub_name}"
                        devices.append({
                            'name': full_path,
                            'path': sub_path,
                            'type': 'Android Device'
                        })
                except:
                    devices.append({
                        'name': device_name,
                        'path': device_path,
                        'type': 'Android Device'
                    })
            else:
                devices.append({
                    'name': device_name,
                    'path': device_path,
                    'type': 'Drive' if ':\\' in device_path else 'Device'
                })
                
    except Exception as e:
        print(f"Fehler: {e}")
    
    return devices

def find_android_storage():
    """
    Speziell für Android-Geräte: Versucht, den Speicherpfad zu finden
    """
    android_paths = []
    
    try:
        import win32com.client
        shell = win32com.client.Dispatch("Shell.Application")
        namespace = shell.NameSpace(17)  # Dieser PC
        
        for item in namespace.Items():
            name = item.Name
            # Nach Android-Geräten suchen
            if "Android" in name or "S2" in name or "S3" in name or "SM-" in name:
                try:
                    # Versuche, in das Gerät zu navigieren
                    folder = item.GetFolder
                    for sub_item in folder.Items():
                        if "Interner Speicher" in sub_item.Name or "SD" in sub_item.Name:
                            android_paths.append({
                                'device': name,
                                'storage': sub_item.Name,
                                'full_path': f"{name}\\{sub_item.Name}"
                            })
                except:
                    android_paths.append({
                        'device': name,
                        'storage': 'Zugriff nicht möglich',
                        'full_path': name
                    })
    
    except Exception as e:
        print(f"Fehler beim Zugriff auf Android-Gerät: {e}")
    
    return android_paths

# Beispielaufruf
if __name__ == "__main__":
    
    all_devices = get_all_devices_in_this_pc()
    for device in all_devices:
        print(f"{device['name']} ({device['type']})")
    """
    print("\n=== Android-Geräte mit Speicher ===")
    android_devices = find_android_storage()
    for device in android_devices:
        print(f"Gerät: {device['device']}")
        print(f"Speicher: {device['storage']}")
        print(f"Vollständiger Pfad: {device['full_path']}")
        print()
    """