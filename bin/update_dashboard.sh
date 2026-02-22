#!/bin/bash

# update_dashboard.sh
# Script para actualizar el dashboard index.html y sincronizar con git

set -e  # Detener en caso de error

# Directorio del dashboard (ajusta si es necesario)
DASHBOARD_DIR="$HOME/Neuraforge-Projects/dashboard"
BACKUP_DIR="$HOME/Neuraforge-Projects/backups"  # opcional, para backups

# Crear carpeta de backups si no existe
mkdir -p "$BACKUP_DIR"

# Fecha actual para el backup
FECHA=$(date +"%Y%m%d_%H%M%S")

# Ir al directorio del proyecto (raíz git)
cd "$HOME/Neuraforge-Projects"

# Verificar si existe el index.html actual
if [ -f "$DASHBOARD_DIR/index.html" ]; then
    echo "📦 Haciendo backup del index.html actual..."
    cp "$DASHBOARD_DIR/index.html" "$BACKUP_DIR/index_$FECHA.html"
    echo "✅ Backup guardado en: $BACKUP_DIR/index_$FECHA.html"
fi

# Aquí asumimos que el nuevo contenido está en un archivo, por ejemplo nuevo_index.html
# Si lo tienes en el portapapeles, puedes crearlo con cat > nuevo_index.html y pegar.
# Por simplicidad, el script espera que el nuevo HTML esté en un archivo llamado nuevo_index.html en el mismo directorio.
# Si quieres pasarlo como argumento, se puede modificar.

NUEVO_ARCHIVO="nuevo_index.html"
if [ ! -f "$NUEVO_ARCHIVO" ]; then
    echo "❌ No se encuentra el archivo $NUEVO_ARCHIVO con el nuevo contenido."
    echo "Créalo con: cat > $NUEVO_ARCHIVO (luego pega el contenido y Ctrl+D)"
    exit 1
fi

echo "🚀 Copiando nuevo dashboard..."
cp "$NUEVO_ARCHIVO" "$DASHBOARD_DIR/index.html"

# Agregar a git
echo "📌 Añadiendo cambios a git..."
git add "$DASHBOARD_DIR/index.html"

# Commit
read -p "📝 Mensaje del commit (Enter para usar 'Actualiza dashboard'): " MSG
if [ -z "$MSG" ]; then
    MSG="Actualiza dashboard"
fi
git commit -m "$MSG"

# Push
read -p "☁️  ¿Hacer push al remoto? (s/N): " PUSH
if [[ "$PUSH" =~ ^[Ss]$ ]]; then
    git push
    echo "✅ Push completado."
else
    echo "⏸️  Push omitido. Puedes hacerlo luego con 'git push'."
fi

echo "🎉 ¡Proceso completado!"
