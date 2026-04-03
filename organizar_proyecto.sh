#!/bin/bash
# Script de organización automática

echo "🔧 Iniciando organización de NeuraforgeAI..."

# 1. Crear estructura
echo "📁 Creando estructura de carpetas..."
mkdir -p neuraforge/{suite/bots,core/moneda,payments/stripe,orion/module,ui,data,logs}
touch neuraforge/__init__.py neuraforge/core/__init__.py neuraforge/payments/__init__.py
touch neuraforge/orion/__init__.py neuraforge/suite/__init__.py neuraforge/ui/__init__.py
touch requirements.txt main.py

# 2. Mover archivos existentes
echo "📦 Moviendo archivos existentes..."
[ -f "sabroso_bot.py" ] && mv sabroso_bot.py neuraforge/suite/bots/sabroso_bot.py && echo "✅ Moved sabroso_bot.py"
[ -f "prueba_sabroso_bot.py" ] && mv prueba_sabroso_bot.py neuraforge/suite/bots/prueba_sabroso_bot.py && echo "✅ Moved prueba_sabroso_bot.py"
[ -f "dashboard.html" ] && mv dashboard.html neuraforge/ui/dashboard.html && echo "✅ Moved dashboard.html"
[ -d "config" ] && mv config neuraforge/config_backup && echo "✅ Moved config"
[ -d "logs" ] && mv logs neuraforge/logs_backup && echo "✅ Moved logs"

# 3. Limpiar backups antiguos
echo "🗑️ Limpiando backups antiguos..."
rm -rf NeuraforgeAI_BACKUP_*

# 4. Verificar resultados
echo "✅ Organización completada!"
echo ""
echo "📊 Estructura final:"
ls -la neuraforge/
echo ""
echo "🐍 Archivos Python encontrados:"
find neuraforge -name "*.py" -type f
