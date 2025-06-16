# disk_node.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulador simple: en memoria
block_storage = {}

@app.route('/write_block', methods=['POST'])
def write_block():
    data = request.get_json()
    block_id = data.get('block_id')
    content = data.get('data')

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

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Uso: python disk_node.py <puerto>")
    else:
        port = int(sys.argv[1])
        app.run(host='127.0.0.1', port=port)
