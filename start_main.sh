#!/bin/bash
# Estación Neuraforge OSIN - Script de Arranq

clear
echo "--------------------------------------------------"
echo "   🛡️  NEURAFORGE AI: SCAN NETWORK TERMINAL  🛡️   "
echo "--------------------------------------------------"

# 1. Configurar variables de entorno para Rust/Pydantic en Termux
export ANDROID_API_LEVEL=24

# 2. Activar permisos de Root para la antena (Requerido para modo monitor)
echo "[*] Configurando interfaz wlan0 en modo monitor..."
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# 3. Verificar sensores (Termux:API)
echo "[*] Verificando sensores de orientación..."
termux-sensor -l | grep -q "orientation"
if [ $? -eq 0 ]; then
    echo "    [OK] Brújula detectada."
else
    echo "    [!] Error: No se detectan sensores. Revisa Termux:API."
fi

# 4. Lanzar servicio de visualización local (Opcional: para ver index.html)
echo "[*] Iniciando servidor web local en puerto 8080..."
python3 -m http.server 8080 > /dev/null 2>&1 &

# 5. Ejecutar motor principal
echo "[*] Iniciando motor main_radar.py..."
python3 main_radar.py
o

