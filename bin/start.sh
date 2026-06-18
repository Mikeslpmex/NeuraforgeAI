#!/bin/bash

# ==============================================================================
# 🔱 NEURAFORGE AI - SCRIPT DE ARRANQUE UNIVERSAL 🔱
# Compatible con AWS EC2, Render y Google Cloud Run
# ==============================================================================

echo "⚙️  Inicializando secuencia de arranque..."

# 1. Navegar a la raíz del repositorio (porque el script está dentro de bin/)
# Esto asegura que encuentre main.py y los logs sin importar desde dónde lo ejecutes
cd "$(dirname "$0")/.."

# 2. Limpieza de procesos (Útil para AWS, ignorado por Docker)
echo "🧹 Limpiando procesos antiguos..."
pkill -f "quality_agent.py" || true
pkill -f "uvicorn" || true
sleep 1

# 3. Preparación del entorno
mkdir -p logs
echo "📁 Directorios listos."

# 4. Lanzar trabajadores en SEGUNDO PLANO (Background)
echo "👁️  Iniciando Agente de Calidad (Modo Vigilante)..."
nohup python3 quality_agent.py auto > logs/quality_agent.log 2>&1 &

# 5. Lanzar el Servidor Web en PRIMER PLANO (Foreground) usando 'exec'
# ¡VITAL!: 'exec' hace que este proceso tome el control. Si se apaga, el contenedor se apaga.
echo "🚀 Iniciando Sapiens Core (API Gateway)..."

# Usamos la variable $PORT que inyecta Render/GCP, o el puerto 8000 por defecto en AWS
PUERTO="${PORT:-8000}" 

exec python3 -m uvicorn main:app --host 0.0.0.0 --port "$PUERTO"
