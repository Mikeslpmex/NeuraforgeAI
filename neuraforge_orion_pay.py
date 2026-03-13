import telebot
import requests
import time
import hashlib
import hmac
import json

# --- CONFIGURACIÓN DE CLASE MUNDIAL ---
TELEGRAM_TOKEN = "8140846319:AAGQ_znQZFjMPMgS9l6uf0kWINkDC5ZvImY"
# Consigue estas en tu cuenta de Binance Developer (Merchant)
BINANCE_API_KEY = "TU_BINANCE_API_KEY"
BINANCE_SECRET_KEY = "TU_BINANCE_SECRET_KEY"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generar_orden_binance(monto, producto):
    """Genera una orden en Binance Pay y devuelve el QR/Link"""
    endpoint = "https://bpay.binanceapi.com/binancepay/openapi/v2/order"
    
    nonce = str(int(time.time() * 1000))
    body = {
        "env": {"terminalType": "APP"},
        "merchantTradeNo": f"TRD{nonce}",
        "orderAmount": monto,
        "currency": "USDT",
        "goods": {"goodsType": "01", "goodsCategory": "D000", "referenceGoodsId": "abc", "goodsName": producto}
    }
    
    json_body = json.dumps(body)
    payload = f"{nonce}\n{json_body}\n"
    signature = hmac.new(BINANCE_SECRET_KEY.encode(), payload.encode(), hashlib.sha512).hexdigest().upper()
    
    headers = {
        "Content-Type": "application/json",
        "BinancePay-Timestamp": nonce,
        "BinancePay-Nonce": nonce,
        "BinancePay-Certificate-SN": BINANCE_API_KEY,
        "BinancePay-Signature": signature
    }

    try:
        response = requests.post(endpoint, headers=headers, data=json_body)
        res_data = response.json()
        if res_data['status'] == 'SUCCESS':
            return res_data['data']['checkoutUrl']
        return None
    except:
        return None

# --- COMANDOS DEL BOT ---

@bot.message_handler(commands=['start'])
def bienvenida(message):
    msg = (
        "🌲 **NeuraforgeAI - Orion Cash System**\n\n"
        "Bienvenido al núcleo de la nueva economía ágil. "
        "Adquiere tus Forgecoins® directamente con USDT.\n\n"
        "Usa /comprar_junior para el proyecto de educación financiera."
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(commands=['comprar_junior'])
def pagar_junior(message):
    bot.reply_to(message, "💎 Generando orden de pago en Binance Pay...")
    # Ejemplo: 10 USDT por el pack Junior
    url_pago = generar_orden_binance(10.0, "Junior Project Access")
    
    if url_pago:
        bot.reply_to(message, f"✅ **Orden Lista**\n\nPaga de forma segura aquí:\n{url_pago}\n\nUna vez confirmado, tus Forgecoins® se activarán.")
    else:
        bot.reply_to(message, "❌ Error al conectar con Binance. Revisa tu Treasury Core.")

print("🚀 Sistema NeuraforgeAI activo y cobrando en Cripto...")
bot.infinity_polling()
