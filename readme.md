![Backy Banner](./media/backy_banner_without_background.png)

# Backy
A lightweight backup utility designed for frequent, selective backups of specific folders from Android devices to your computer. Perfect for users who need regular backups of only certain directories without transferring everything.

## How to Use
1. Connect your phone to your PC or laptop via USB cable
2. Enable **File Transfer** mode on your phone when prompted (you should receive a system notification)
3. Configure the `config.json` file:
   - Set your backup destination in the `save_path` field
   - Specify which folders to back up in `folders_to_backup`
4. Run `Backy.exe` from the same directory as your configuration file

## Important
- Duplicate images will be deleted by hash (hash of every picture gets saved in `data.db`).
- If two pictures have the same name (this case is very rare) but different hashes, one of them gets renamed.

## Notes
- If your phone is not detected, check the `identifier_list` in the configuration file and add your device's name or company if necessary and try again
- When multiple phones are connected, Backy will select the first device recognized
- Ensure your phone remains unlocked and in file transfer mode during the backup process
- Ensure File Transfer mode is active on your phone!

## Example Configuration
```json
{   
    "DCIM_transfer" : {
        "save_path" : "S:\\_GITHUB\\White\\test",
        "database_name" : "data.db",
        "folders_to_backup" : [
            "test"
        ],
        "identifier_list" : [
            "Android",
            "Samsung",
            "S1",
            "S2",
            "S3",
            "S4"
        ]
    }
}
```

## Installation
1. Download the latest release from the Releases page
2. Save the downloaded folder to your preferred location
3. Configure config.json to match your backup needs
4. Make sure Backy.exe is in the same dir as config.json
