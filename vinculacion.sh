#!/data/data/com.termux/files/usr/bin/bash

# === 1. Instalación de dependencias ===
pkg update -y && pkg upgrade -y
pkg install -y python git termux-api curl

# === 2. Variables de entorno ===
export PROJECT="NeuraforgeAI"
export TREASURY_URL="https://orion-treasury.supabase.co"
export VERTEX_WEBHOOK="https://vertexai.cloudfunctions.net/analyzer"
export AFFILIATE_BOT="https://api.telegram.org/bot<YOUR_TOKEN>"
export CHAT_ID="<TU_CHAT_ID>"

# === 3. Notificación inicial en móvil ===
termux-notification --title "NeuraForgeAI" \
  --content "Ceremonia de vinculación iniciada: Bot de afiliados activo" \
  --priority high

# === 4. Levantar módulo Python ===
python3 << 'EOF'
import requests, os

TREASURY_URL = os.getenv("TREASURY_URL")
VERTEX_WEBHOOK = os.getenv("VERTEX_WEBHOOK")
AFFILIATE_BOT = os.getenv("AFFILIATE_BOT")
CHAT_ID = os.getenv("CHAT_ID")

def registrar_afiliado(user_id, referral_code):
    payload = {
        "user_id": user_id,
        "referral_code": referral_code,
        "reward": "10 ForgeCoins"
    }
    r = requests.post(f"{TREASURY_URL}/affiliates", json=payload)
    return r.json()

def notificar_vertex(pr_data):
    r = requests.post(VERTEX_WEBHOOK, json=pr_data)
    return r.json()

def enviar_telegram(msg):
    requests.post(f"{AFFILIATE_BOT}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": msg
    })

# === Ejemplo de flujo ceremonial ===
afiliado = registrar_afiliado("user123", "REF-CODE-987")
enviar_telegram(f"Nuevo afiliado registrado: {afiliado}")
EOF

# === 5. Notificación final ===
termux-notification --title "NeuraForgeAI" \
  --content "Bot de afiliados vinculado y sincronizado con Vertex AI + Orion Treasury" \
  --priority high
