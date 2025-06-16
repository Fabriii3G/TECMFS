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

if __name__ == '__main__':
    upload_file('ejemplo.pdf')
