#!/data/data/com.termux/files/usr/bin/bash

# =============================================================================
# Script de organización definitiva para NeuraForgeAI
# Unifica, mueve y limpia la estructura de archivos
# =============================================================================

set -e  # Salir si hay error

echo "🚀 Iniciando organización definitiva de NeuraForgeAI"
echo "===================================================="

# ---------- 1. Unificar las dos carpetas de afiliados_estrategicos ----------
if [ -d ~/afiliados_estrategicos ] && [ -d ~/Neuraforge-Projects/afiliados_estrategicos ]; then
    echo "📁 Detectadas dos carpetas de afiliados_estrategicos. Unificando..."
    
    # Mover contenido de la carpeta del home a la de Projects
    cp -rn ~/afiliados_estrategicos/* ~/Neuraforge-Projects/afiliados_estrategicos/ 2>/dev/null || true
    cp -rn ~/afiliados_estrategicos/.* ~/Neuraforge-Projects/afiliados_estrategicos/ 2>/dev/null || true
    
    echo "✅ Contenido copiado. ¿Eliminar la carpeta duplicada del home? (s/N)"
    read -r respuesta
    if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
        rm -rf ~/afiliados_estrategicos
        echo "   Carpeta eliminada."
    else
        echo "   Carpeta conservada (puedes borrarla manualmente después)."
    fi
else
    echo "ℹ️ No se detectaron dos carpetas de afiliados_estrategicos."
fi

# ---------- 2. Mover funciones (fuctions/) a google_cloud/firebase_functions ----------
if [ -d ~/Neuraforge-Projects/fuctions ]; then
    echo "📁 Moviendo archivos de fuctions/ a google_cloud/firebase_functions/..."
    mkdir -p ~/Neuraforge-Projects/google_cloud/firebase_functions
    mv ~/Neuraforge-Projects/fuctions/* ~/Neuraforge-Projects/google_cloud/firebase_functions/ 2>/dev/null || true
    rmdir ~/Neuraforge-Projects/fuctions 2>/dev/null || echo "   (la carpeta no estaba vacía, revisa)"
    echo "✅ Archivos movidos."
fi

# ---------- 3. Renombrar extensiones incorrectas ----------
if [ -f ~/Neuraforge-Projects/google_cloud/firebase_functions/whatsapp_webhook.ph ]; then
    echo "📄 Renombrando whatsapp_webhook.ph a .py..."
    mv ~/Neuraforge-Projects/google_cloud/firebase_functions/whatsapp_webhook.ph \
       ~/Neuraforge-Projects/google_cloud/firebase_functions/whatsapp_webhook.py
fi

# Corregir posible typo en el nombre del archivo de recomendación
if [ -f ~/Neuraforge-Projects/google_cloud/firebase_functions/afiliate_recomend.py ]; then
    echo "📄 Renombrando afiliate_recomend.py a affiliate_recommend.py..."
    mv ~/Neuraforge-Projects/google_cloud/firebase_functions/afiliate_recomend.py \
       ~/Neuraforge-Projects/google_cloud/firebase_functions/affiliate_recommend.py
fi

# ---------- 4. Eliminar test_affiliate.py duplicado en home ----------
if [ -f ~/test_affiliate.py ]; then
    echo "📄 Eliminando test_affiliate.py duplicado en home (ya existe en Neuraforge-Projects/afiliados_estrategicos/)."
    rm ~/test_affiliate.py
fi

# ---------- 5. Crear archivos requirements.txt en carpetas que lo necesiten ----------
# Para google_cloud/firebase_functions
if [ ! -f ~/Neuraforge-Projects/google_cloud/firebase_functions/requirements.txt ]; then
    echo "📝 Creando requirements.txt para las Cloud Functions..."
    cat > ~/Neuraforge-Projects/google_cloud/firebase_functions/requirements.txt << 'EOF'
requests>=2.28.0
firebase-admin>=6.0.0
python-dotenv>=1.0.0
EOF
fi

# Para afiliados_estrategicos (si no tiene)
if [ ! -f ~/Neuraforge-Projects/afiliados_estrategicos/requirements.txt ]; then
    cat > ~/Neuraforge-Projects/afiliados_estrategicos/requirements.txt << 'EOF'
requests>=2.28.0
firebase-admin>=6.0.0
EOF
fi

# ---------- 6. Crear .gitignore en la raíz del proyecto para evitar subir credenciales ----------
if [ ! -f ~/Neuraforge-Projects/.gitignore ]; then
    echo "📝 Creando .gitignore global..."
    cat > ~/Neuraforge-Projects/.gitignore << 'EOF'
# Credenciales y entornos
.env
*.env
credentials.json
service-account-key.json
*secret*

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/

# Termux
*.log
*.lock
ngrok
.DS_Store
EOF
fi

# ---------- 7. Verificar que todo quede ordenado ----------
echo ""
echo "🔍 Verificando estructura final..."
echo ""

# Mostrar árbol resumido
if command -v tree &> /dev/null; then
    tree -L 3 ~/Neuraforge-Projects --dirsfirst
else
    echo "Instala tree para ver la estructura (pkg install tree)"
fi

echo ""
echo "✅ Organización completada."
echo "   Revisa los mensajes anteriores por si hubo errores."
