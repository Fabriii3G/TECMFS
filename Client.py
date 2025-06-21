# -*- coding: utf-8 -*-
import requests
import sys
import os

BASE_URL = 'http://127.0.0.1:5000'

def upload_file(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] El archivo '{filename}' no existe.")
        return

    with open(filename, 'rb') as f:
        file_data = list(f.read())

    response = requests.post(f"{BASE_URL}/upload_file", json={
        "filename": filename,
        "data": file_data
    })
    print("Subida:", response.json())

def download_file(filename):
    response = requests.get(f"{BASE_URL}/download_file", params={"filename": filename})
    if response.status_code == 200:
        with open(f"descargado_{filename}", 'wb') as f:
            f.write(bytes(response.json().get("data")))
        print(f"Archivo reconstruido como 'descargado_{filename}'")
    else:
        print("Error al descargar:", response.json())

def list_files():
    response = requests.get(f"{BASE_URL}/list_files")
    if response.status_code == 200:
        files = response.json().get("files", [])
        if not files:
            print("No hay archivos disponibles.")
        else:
            print("Archivos disponibles:")
            for f in files:
                print(" -", f)
    else:
        print("Error:", response.json())

def delete_file(filename):
    response = requests.delete(f"{BASE_URL}/delete_file", params={"filename": filename})
    print("Eliminacion:", response.json())

# --- CLI (Command Line Interface) ---
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python Client.py [upload|download|list|delete] <archivo>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "upload" and len(sys.argv) == 3:
        upload_file(sys.argv[2])
    elif command == "download" and len(sys.argv) == 3:
        download_file(sys.argv[2])
    elif command == "list":
        list_files()
    elif command == "delete" and len(sys.argv) == 3:
        delete_file(sys.argv[2])
    else:
        print("Comando invalido o argumentos incompletos.")
        print("Uso:")
        print("  python Client.py upload <archivo>")
        print("  python Client.py download <archivo>")
        print("  python Client.py list")
        print("  python Client.py delete <archivo>")
