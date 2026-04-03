#!/bin/bash
# verify_neuraforge.sh

echo "🔍 Verificando NeuraforgeAI..."

# 1. Archivos accidentales
if ls | grep -qE "^(El|Hay|Transfer|carpeta)"; then
    echo "❌ Archivos accidentales detectados"
    exit 1
else
    echo "✅ Sin archivos accidentales"
fi

# 2. Git limpio
if git status --porcelain | grep -v ".gitignore" | grep -q .; then
    echo "❌ Git no está limpio"
    git status --short
    exit 1
else
    echo "✅ Git limpio"
fi

# 3. Imports Python
cd neuraforge
if PYTHONPATH=.. python -c "from api.main import app" 2>/dev/null; then
    echo "✅ Imports Python OK"
else
    echo "❌ Error en imports Python"
    exit 1
fi

echo ""
echo "🎉 ¡Todo listo para Render!"
