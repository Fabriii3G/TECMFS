import subprocess
import time
import os
import sys

#YTHON_PATH = os.path.join("venv", "Scripts", "python.exe")
PYTHON_PATH = sys.executable
ports = [5001, 5002, 5003, 5004]

for port in ports:
    config_file = f"disk_config_{port}.xml"
    if not os.path.exists(config_file):
        print(f"[ERROR] Falta el archivo de configuracion: {config_file}")
        continue
    subprocess.Popen(
        ['start', 'cmd', '/k', f'{PYTHON_PATH} DiskNode.py {config_file}'],
        shell=True
    )
    time.sleep(0.5)

print("[INFO] Nodos lanzados con configuracion XML.")
