# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta de prueba: guardar bloques
@app.route('/write_block', methods=['POST'])
def write_block():
    data = request.get_json()
    block_id = data.get('block_id')
    content = data.get('data')
    print(f"Received block {block_id} with data: {content}")
    return jsonify({"message": f"Block {block_id} stored successfully"}), 200

# Ruta de prueba: leer bloques
@app.route('/read_block', methods=['GET'])
def read_block():
    block_id = request.args.get('block_id')
    # Simulacion de contenido (en una version real se lee del disco o RAM)
    content = "Simulated block content for " + block_id
    return jsonify({"block_id": block_id, "data": content}), 200

# Inicio del servidor
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
