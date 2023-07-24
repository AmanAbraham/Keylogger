import base64
import os
from cryptography.fernet import Fernet

def main(matching_files):
    decrypted_data_list = []
    for file in matching_files:
        with open(file, 'r') as log_file:
            lines = log_file.readlines()
            secret_key = lines[1].strip()  # Assuming the secret key is in the second line of each file
            print(secret_key)
            secret_key_bytes = base64.urlsafe_b64decode(secret_key.encode())
            encrypted_data = lines[2:]

        f = Fernet(secret_key_bytes)  
        decrypted_data = [f.decrypt(data.strip().encode()).decode() for data in encrypted_data]
        decrypted_data_list.extend(decrypted_data)

    return decrypted_data_list

if __name__ == '__main__':
    files_in_directory = os.listdir()
    matching_files = [file_name for file_name in files_in_directory if file_name.startswith('old_log_')]
    decrypted_data = main(matching_files)
    print(decrypted_data)