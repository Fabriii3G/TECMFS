@echo off
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Lanzando nodos...
python LaunchNodes.py
timeout /t 2

echo Iniciando Controller Node...
start cmd /k "python Server.py"

echo Iniciando Client Node...
start cmd /k "python Client.py"

echo Iniciando Interfaz Gráfica...
start python GUI.py

echo ---- SISTEMA LISTO PARA PRUEBAS ----
