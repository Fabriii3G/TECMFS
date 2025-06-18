# -*- coding: utf-8 -*-
import requests

BASE_URL = 'http://127.0.0.1:5000'

def upload_file(filename):
    with open(filename, 'rb') as f:
        file_data = list(f.read())

    response = requests.post(f"{BASE_URL}/upload_file", json={
        "filename": filename,
        "data": file_data
    })
    print("Respuesta:", response.json())

def download_file(filename):
    response = requests.get(f"{BASE_URL}/download_file", params={"filename": filename})
    if response.status_code == 200:
        data = response.json()
        file_data = bytes(data["data"])
        with open(f"descargado_{filename}", 'wb') as f:
            f.write(file_data)
        print(f"Archivo {filename} reconstruido y guardado como descargado_{filename}")
    else:
        print("Error al descargar:", response.json())

if __name__ == '__main__':
    upload_file('ejemplo.pdf')
    download_file('ejemplo.pdf')
