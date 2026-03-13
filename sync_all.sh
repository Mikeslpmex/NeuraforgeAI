#!/bin/bash
# Script de Reacomodo y Sincronización Neuraforge AI

echo "[*] Organizando estructura de carpetas..."

# Crear carpetas si no existen
mkdir -p logs builds cloud_config

# 1. Corregir el script de arranque (cambiar de .py a .sh para evitar errores)
if [ -f "start_main.py" ]; then
    mv start_main.py start_main.sh
    chmod +x start_main.sh
    echo "[OK] start_main.py ahora es start_main.sh (Ejecutable)"
fi

# 2. Sincronización con GitHub
echo "[*] Sincronizando con GitHub..."
git add .
git commit -m "Update Neuraforge: Reacomodo y preparación para GCP"
git push origin main

# 3. Preparación para Google Cloud (creación de archivo de despliegue)
echo "[*] Generando manifiesto de producción..."
cat <<EOF > cloud_config/app.yaml
runtime: python39
instance_class: F1
entrypoint: python3 nexus_orquestador.py
EOF

echo "--------------------------------------------------"
echo " ✅ Sincronización Completa. Usa ./start_main.sh"
echo "--------------------------------------------------"
