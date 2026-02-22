#!/bin/bash
# Script para sincronizar el ecosistema NeuraforgeAI hacia producción

echo "🚀 Iniciando Sincronización de Monetización..."

# 1. Empaquetar el núcleo de afiliados para la nube
echo "📦 Preparando Nexus-Affi y Tesorería..."
cd ~/Neuraforge-Projects/afiliados_estrategicos
tar -czf cloud_deploy.tar.gz . 

# 2. Verificar estructura del Tesorero
if [ -f "../tesorero/orion_treasury.py" ]; then
    echo "💰 Tesorero Orion detectado y listo para proteger el Core."
else
    echo "⚠️ Alerta: Revisar ubicación de Orion Treasury."
fi

# 3. Comandos de Sincronización Git (Ajusta con tu repo)
echo "🔄 Sincronizando con el repositorio central..."
git add .
git commit -m "Despliegue de monetización inmediata - Escuadrón SABROSO"
# git push origin main  # Descomenta cuando conectes tu GitHub

echo "✅ Proceso completado. Sistema listo para el 'Junior Project' y Afiliados."
