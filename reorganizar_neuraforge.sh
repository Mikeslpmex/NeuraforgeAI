#!/bin/bash
# Script de Reacomodo y Sincronización para NeuraforgeAI

echo "[*] Iniciando limpieza de NeuraforgeAI..."

# 1. Mover scripts de instalación a bin/ para limpiar la raíz
mkdir -p bin
mv bin/*.sh . 2>/dev/null # Evitar errores si ya están fuera
mv install_*.sh bin/ 2>/dev/null
mv organizar_*.sh bin/ 2>/dev/null
mv sync_*.sh bin/ 2>/dev/null

# 2. Corregir el script de arranque (evitar el SyntaxError de Python)
if [ -f "start_main.py" ]; then
    echo "[*] Convirtiendo start_main.py a Bash script..."
    mv start_main.py start_main.sh
    chmod +x start_main.sh
fi

# 3. Sincronización con GitHub (Rama Principal)
echo "[*] Sincronizando con GitHub: Mikeslpmex/NeuraforgeAI..."
git add .
git commit -m "Reorganización de estructura y corrección de scripts de arranque"
git push origin main

echo "--------------------------------------------------"
echo " ✅ Proyecto organizado y sincronizado con GitHub"
echo "--------------------------------------------------"
