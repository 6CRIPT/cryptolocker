import argparse
import sys
import os
from cryptography.fernet import Fernet, InvalidToken

def decrypt_directory(path, key):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            decrypt_directory(file_path, key)
        else:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            try:
                fernet = Fernet(key)
            except ValueError as e:
                print(f"Error: la clave no es valida, abortando.")
                sys.exit()
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)
            except InvalidToken:
                print("Token invalido")
                sys.exit()
            except Exception as e:
                print("Error general al desencryptar, abortando....")
                sys.exit()

def main():
    parser = argparse.ArgumentParser(description="Desencripta el directorio objetivo.")
    parser.add_argument("path", help="Ruta a desencriptar.")
    parser.add_argument("key_path", help="ruta del archivo que contiene la key.")

    args = parser.parse_args()

    path = args.path
    key_file_path = args.key_path

    try:
        with open(key_file_path, "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("Archivo de key no encontrado, abortando...")
        sys.exit()
    decrypt_directory(path, key)
    print("Desencriptación completada.")

if __name__ == "__main__":
    main()