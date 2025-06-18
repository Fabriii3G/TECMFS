import subprocess
import time
import os
import sys

PYTHON_PATH = sys.executable

# Ruta al intérprete de Python del entorno virtual
#PYTHON_PATH = os.path.join("venv", "Scripts", "python.exe")

# Verifica que el ejecutable exista
if not os.path.exists(PYTHON_PATH):
    print("[ERROR] No se encontró el intérprete de Python del entorno virtual.")
    exit(1)

# Lista de puertos para los nodos
ports = [5001, 5002, 5003, 5004]

# Abre una terminal por cada puerto
for port in ports:
    subprocess.Popen(
        ['start', 'cmd', '/k', f'{PYTHON_PATH} DiskNode.py {port}'],
        shell=True
    )
    time.sleep(0.5)  # Pequeño retardo para evitar conflicto entre ventanas

print("[INFO] Se han lanzado los nodos en terminales separadas.")
