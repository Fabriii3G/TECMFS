# -*- coding: utf-8 -*-

import requests

# Direccion del servidor ControllerNode
BASE_URL = 'http://127.0.0.1:5000'

def send_block(block_id, data):
    payload = {
        "block_id": block_id,
        "data": data
    }
    response = requests.post(f"{BASE_URL}/write_block", json=payload)
    print("Respuesta del servidor:", response.json())

def get_block(block_id):
    response = requests.get(f"{BASE_URL}/read_block", params={"block_id": block_id})
    print("Contenido recibido:", response.json())

if __name__ == '__main__':
    send_block("block001", "contenido_de_prueba")
    get_block("block001")




