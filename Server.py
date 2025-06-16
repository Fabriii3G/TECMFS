# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from DataStructures.block_array import BlockArray
from DataStructures.hashmap import HashMap
import requests
import os

app = Flask(__name__)

# Parámetros del RAID
DISK_NODES = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003",
    "http://127.0.0.1:5004"
]
BLOCK_SIZE = 1024
MAX_BLOCKS = 5000
block_map = HashMap()

def split_into_blocks(data):
    blocks = BlockArray(MAX_BLOCKS)
    i = 0
    while i < len(data):
        block = data[i:i + BLOCK_SIZE]
        if len(block) < BLOCK_SIZE:
            block += b'\x00' * (BLOCK_SIZE - len(block))
        blocks.add(block)
        i += BLOCK_SIZE
    return blocks

def calculate_parity(block_array, count):
    result = bytearray(BLOCK_SIZE)
    for i in range(BLOCK_SIZE):
        val = 0
        for j in range(count):
            val ^= block_array.get(j)[i]
        result[i] = val
    return bytes(result)

def distribute_blocks(filename, file_data):
    blocks = split_into_blocks(file_data)
    group_size = len(DISK_NODES) - 1
    group_index = 0
    i = 0

    while i < blocks.length():
        chunk = BlockArray(group_size)
        j = 0
        while j < group_size and i + j < blocks.length():
            chunk.add(blocks.get(i + j))
            j += 1

        while chunk.length() < group_size:
            chunk.add(b'\x00' * BLOCK_SIZE)

        parity = calculate_parity(chunk, group_size)
        full_group = BlockArray(len(DISK_NODES))

        for k in range(group_size):
            full_group.add(chunk.get(k))
        full_group.add(parity)

        for node_index in range(len(DISK_NODES)):
            dest_node = (group_index + node_index) % len(DISK_NODES)
            block_data = full_group.get(node_index)
            block_id = f"{filename}_block_{i + node_index}"
            block_map.put(block_id, dest_node)

            response = requests.post(
                f"{DISK_NODES[dest_node]}/write_block",
                json={"block_id": block_id, "data": list(block_data)}
            )
            if response.status_code != 200:
                print(f"[ERROR] Block {block_id} failed to send to node {dest_node}")

        i += group_size
        group_index += 1

    print("[INFO] Archivo distribuido correctamente.")
    return True

# ----------- FLASK ROUTES -----------

@app.route('/upload_file', methods=['POST'])
def upload_file():
    data = request.get_json()
    filename = data.get('filename')
    file_bytes = bytes(data.get('data'))

    if not filename or not file_bytes:
        return jsonify({"error": "Datos inválidos"}), 400

    success = distribute_blocks(filename, file_bytes)
    return jsonify({"message": "Archivo distribuido correctamente" if success else "Error"}), 200

@app.route('/read_block', methods=['GET'])
def read_block():
    block_id = request.args.get('block_id')
    node_index = block_map.get(block_id)

    if node_index is None:
        return jsonify({"error": "Bloque no encontrado"}), 404

    response = requests.get(f"{DISK_NODES[node_index]}/read_block", params={"block_id": block_id})
    return jsonify(response.json()), response.status_code

# Iniciar servidor del Controller Node
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
