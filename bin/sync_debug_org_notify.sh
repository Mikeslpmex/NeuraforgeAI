#!/bin/bash

# Script: Sincronización, depuración, organización y notificación con Termux API
# Autor: Tú y NeuraforgeAI
# Fecha: $(date)

echo "🚀 Iniciando script de sincronización, limpieza y organización..."

# === Configuración de Termux API ===
NOTIFY="termux-notification"

# === Función para enviar notificación ===
notify() {
    title="$1"
    content="$2"
    $NOTIFY -t "$title" -c "$content"
}

# === Actualizar desde Git ===
echo "🔄 Actualizando desde GitHub..."
if [ -d ".git" ]; then
    git fetch origin
    git pull origin main
    notify "Git actualizado" "El repositorio ha sido actualizado exitosamente."
else
    echo "⚠️ No se encontró un repositorio Git. Saltando actualización."
fi

# === Depuración de archivos ===
echo "🧹 Limpiando archivos temporales..."
find . -type f -name "*.tmp" -delete
find . -type f -name "*.log" -delete
find . -type f -name "*~" -delete
notify "Limpieza completada" "Archivos temporales eliminados."

# === Organizar archivos por extensión ===
echo "📂 Organizando archivos..."
mkdir -p bin docs src logs assets backups

find . -maxdepth 1 -name "*.sh" -exec mv {} bin/ \; 2>/dev/null
find . -maxdepth 1 -name "*.md" -exec mv {} docs/ \; 2>/dev/null
find . -maxdepth 1 -name "*.py" -exec mv {} src/ \; 2>/dev/null
find . -maxdepth 1 -name "*.json" -exec mv {} assets/ \; 2>/dev/null
find . -maxdepth 1 -name "*.keystore" -exec mv {} backups/ \; 2>/dev/null

notify "Organización completada" "Archivos movidos a sus respectivas carpetas."

# === Verificar espacio en disco ===
echo "📊 Revisando espacio en disco..."
df -h .
SPACE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//g')

if [ "$SPACE" -gt 80 ]; then
    notify "⚠️ Espacio bajo ⚠️" "Usado: $SPACE%. Considera liberar espacio."
    echo "⚠️ El uso de disco es del $SPACE%. Considera liberar espacio."
else
    notify "✅ Disco OK" "Espacio disponible suficiente."
fi

# === Fin del script ===
echo "✅ Proceso terminado exitosamente."
