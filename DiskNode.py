# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import sys
import xml.etree.ElementTree as ET

app = Flask(__name__)
block_storage = {}
MAX_BLOCKS = 0
BLOCK_SIZE = 0

def load_config(path):
    global MAX_BLOCKS, BLOCK_SIZE
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        port = int(root.find("Port").text)
        MAX_BLOCKS = int(root.find("MaxBlocks").text)
        BLOCK_SIZE = int(root.find("BlockSize").text)
        return port
    except Exception as e:
        print(f"[ERROR] No se pudo cargar la configuracion XML: {e}")
        sys.exit(1)

@app.route('/write_block', methods=['POST'])
def write_block():
    data = request.get_json()
    block_id = data.get('block_id')
    content = data.get('data')
    if len(block_storage) >= MAX_BLOCKS:
        return jsonify({"error": "Disk full"}), 507  # Insufficient Storage
    block_storage[block_id] = content
    print(f"[{request.host}] Almacenado: {block_id}")
    return jsonify({"message": "Block stored"}), 200

@app.route('/read_block', methods=['GET'])
def read_block():
    block_id = request.args.get('block_id')
    content = block_storage.get(block_id)
    if content is None:
        return jsonify({"error": "Block not found"}), 404
    return jsonify({"block_id": block_id, "data": content}), 200

@app.route('/delete_block', methods=['DELETE'])
def delete_block():
    block_id = request.args.get('block_id')
    if block_id in block_storage:
        del block_storage[block_id]
        return jsonify({"message": f"Bloque {block_id} eliminado"}), 200
    return jsonify({"error": "Bloque no encontrado"}), 404

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python disk_node.py <archivo_config.xml>")
    else:
        port = load_config(sys.argv[1])
        app.run(host='127.0.0.1', port=port)
