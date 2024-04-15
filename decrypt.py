import os
import argparse
from cryptography.fernet import Fernet, InvalidToken
import sys


def decrypt_directory(path, key):
    """Desencripta todos los archivos en el directorio especificado usando la clave dada."""
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            decrypt_directory(file_path, key)  # Llamada recursiva para subdirectorios
        else:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            try:
                fernet = Fernet(key)
            except ValueError as e:
                print(f"Error: La clave proporcionada tiene un formato incorrecto, abortando ejecución.")
                sys.exit()
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)
            except InvalidToken:
                print(f"Error: La clave proporcionada no puede desencriptar el archivo {file}.")
                sys.exit()
            except Exception as e:
                print(f"Error al desencriptar {file}: {e}")
                sys.exit()

def main():
    parser = argparse.ArgumentParser(description="Desencripta un directorio de archivos.")
    parser.add_argument("path", help="Ruta del directorio a desencriptar")
    parser.add_argument("key_path", help="Ruta del archivo que contiene la clave de desencriptación")
    
    args = parser.parse_args()
    
    path = args.path
    key_file_path = args.key_path
    
    # Leer la clave de encriptación desde el archivo
    try:
        with open(key_file_path, "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("Archivo de clave no encontrado.")
        return
    
    decrypt_directory(path, key)
    print("Desencriptación completada.")

if __name__ == "__main__":
    main()
