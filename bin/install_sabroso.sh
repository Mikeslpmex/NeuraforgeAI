#!/data/data/com.termux/files/usr/bin/bash
# Instalador de NeuraForge System para Termux

echo "🚀 Instalando NeuraForge System en Termux..."
echo "Actualizando paquetes básicos..."
pkg update -y && pkg upgrade -y

# Instalar dependencias del sistema
echo "📦 Instalando paquetes necesarios..."
pkg install -y python python-pip git clang cmake libxml2 libxslt

# Crear estructura de directorios
echo "📁 Creando carpetas del proyecto..."
mkdir -p ~/neuraforge_system/{data/logs,modules/{agents,analytics,telemetry},config}
cd ~/neuraforge_system

# Crear entorno virtual
echo "🐍 Creando entorno virtual Python..."
python -m venv venv
source venv/bin/activate

# Instalar dependencias Python ligeras (sin torch por defecto)
echo "📦 Instalando librerías base..."
pip install --upgrade pip
pip install numpy pandas scikit-learn xgboost aiosqlite flask twilio requests python-dotenv

# Preguntar por PyTorch (deep learning)
echo ""
echo "⚙️ ¿Deseas instalar PyTorch para funciones de deep learning? (ocupa ~500 MB) [s/N]"
read -r instalar_torch
if [[ "$instalar_torch" == "s" || "$instalar_torch" == "S" ]]; then
    pip install torch torchvision torchaudio
    echo "✅ PyTorch instalado."
else
    echo "⏩ Omitiendo PyTorch. El sistema usará solo modelos clásicos."
fi

# Crear archivo de manifiesto de agentes (pégalo desde tu código)
cat > ~/neuraforge_system/agents_manifest.json << 'EOF'
{
  "COMANDANTE": {
    "arquetipo": "Dominante-Estratega",
    "tono": "firme, táctico",
    "frase_activacion": "⚠️ COMANDANTE ACTIVADO ⚠️\nObjetivo detectado. Ejecutando protocolo de impacto.\nCoordenadas: AGUA-MAR-TIERRA-DIGITAL",
    "estilo_operativo": "Monetización directa, control de tráfico, activación simbólica",
    "microservicios": ["pagos_suscripciones", "mapa_calor", "oraculo", "control_trafico"],
    "entorno": "DIGITAL",
    "emoji": "🔥",
    "color": "#FF0000"
  },
  "SABINO": {
    "arquetipo": "Sabio-Protector",
    "tono": "sereno, analítico",
    "frase_activacion": "🧠 SABINO ACTIVADO 🧠\nLa sabiduría no duerme. El rastreo comienza.\nRedes profundas: ESCANEANDO",
    "estilo_operativo": "Precisión emocional, enfoque en personas y redes profundas, análisis predictivo",
    "microservicios": ["busqueda_personas", "redes_sociales", "alertas", "analisis_sentimientos"],
    "entorno": "TIERRA",
    "emoji": "🧠",
    "color": "#0000FF"
  },
  "CHINO": {
    "arquetipo": "Creativo-Disruptivo",
    "tono": "irreverente, curioso",
    "frase_activacion": "🌱 CHINO ACTIVADO 🌱\n¿Y si lo hacemos diferente? Activando visión lateral.\nInnovación: DESBLOQUEADA",
    "estilo_operativo": "Exploración de oportunidades, scraping inteligente, viralidad, modelos emergentes",
    "microservicios": ["oportunidades_negocio", "hosting_afiliado", "modelo_olvidada", "viralidad"],
    "entorno": "MAR",
    "emoji": "🌱",
    "color": "#00FF00"
  },
  "NEUTRO": {
    "arquetipo": "Neutro-Adaptativo",
    "tono": "equilibrado, objetivo",
    "frase_activacion": "Sistema activado. Esperando instrucciones.",
    "estilo_operativo": "Adaptación general, respuesta básica, registro de actividades",
    "microservicios": ["registro_basico", "respuesta_generica", "adaptacion_contexto"],
    "entorno": "DIGITAL",
    "emoji": "⚪",
    "color": "#CCCCCC"
  }
}
EOF

# Crear archivo de entorno .env (debes editarlo después)
cat > ~/neuraforge_system/.env << 'EOF'
# Telegram Configuration
TELEGRAM_TOKEN=tu_token_aqui
ADMIN_CHAT_ID=tu_chat_id

# MercadoPago Integration
MP_ACCESS_TOKEN=tu_access_token
MP_PUBLIC_KEY=tu_public_key
MP_NOTIFICATION_URL=https://tudominio.com/webhooks/mp

# System Behavior
UMBRAL_BAJO_GANANCIA=10.0
INTENTOS_RECIENTES=5
BOT_RUN_INTERVAL=21600
BACKUP_HOUR=2

# Database
DB_PATH=data/neuraforge.db
DB_BACKUP_PATH=backups/

# Security
QIPOS_SALT=tu_salt_secreto
FLASK_SECRET_KEY=tu_clave_secreta
EOF

# Crear script principal main.py (debes pegar el código completo del sistema de IA)
echo "📝 Ahora pega el contenido de main.py (el sistema de IA predictiva) en ~/neuraforge_system/main.py"
echo "   Puedes usar nano main.py o copiarlo desde tu código."
echo "   Ejemplo: nano main.py y pegas todo."

# Crear requirements.txt (ya lo instalamos, pero lo dejamos para referencia)
cat > ~/neuraforge_system/requirements.txt << 'EOF'
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
xgboost>=1.5.0
torch>=1.10.0
aiosqlite
flask
twilio
requests
python-dotenv
EOF

# Crear configuración de entorno YAML
mkdir -p ~/neuraforge_system/config
cat > ~/neuraforge_system/config/environment.yaml << 'EOF'
modelos:
  ventas:
    tipo: "RandomForest"
    hiperparametros:
      n_estimators: 200
      max_depth: 15
    retrain_horas: 24
  agentes:
    tipo: "XGBoost"
    hiperparametros:
      learning_rate: 0.1
      max_depth: 6
    retrain_ventas: 100
  anomalias:
    tipo: "IsolationForest"
    sensibilidad: 0.95
deep_learning:
  habilitado: true
  red_neuronal:
    capas: [128, 64, 32]
    dropout: 0.2
    epochs: 100
  lstm:
    unidades: 64
    capas: 2
    lookback: 24
caching:
  predicciones: 3600
  modelos: 86400
monitoreo:
  anomalias_nivel_alerta: "medio"
  reporte_automatico: true
  notificar_telegram: true
EOF

echo ""
echo "✅ Instalación base completada."
echo "Para usar el sistema:"
echo "  cd ~/neuraforge_system"
echo "  source venv/bin/activate"
echo "  edita .env con tus tokens"
echo "  python main.py"
echo ""
echo "¡Que fluya la sabrosura digital, jefe! 🧠🔥🌱"

