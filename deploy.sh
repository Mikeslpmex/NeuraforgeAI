#!/bin/bash
echo "🚀 Iniciando despliegue de NeuraForgeAI en modo producción..."

# Construir imagen
docker build -t neuraforgeai:latest .

# Detener contenedores previos
docker stop neuraforgeai || true
docker rm neuraforgeai || true

# Ejecutar nuevo contenedor
docker run -d \
  --name neuraforgeai \
  -p 8000:8000 \
  --env-file .env \
  neuraforgeai:latest

echo "✅ Despliegue completado. NeuraForgeAI está activo en https://app.neuraforge.ai"
echo "Equipo NeuraforgeAI & AI colaborativa"
