#!/bin/bash
# Configuración de entorno en Termux/Linux

echo "🚀 Iniciando Estación Neuraforge OSIN..."

# 1. Permisos de ejecución
chmod +x *.py

# 2. Configurar Interfaz de Red (Requiere Root/Sudo)
# Cambia 'wlan0' por tu interfaz si es diferente
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

echo "✅ Modo Monitor activado."

# 3. Lanzar el sistema principal
python3 main_radar.py
