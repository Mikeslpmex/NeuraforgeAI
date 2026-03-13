cat << 'EOF' > sabroso_bot.py
import telebot
import mercadopago
import os

# Tu Token Real de Telegram
TOKEN = "8140846319:AAE05LJCAZy-9gM-cL1YJOJLKIIzBlPvdYQ"
bot = telebot.TeleBot(TOKEN)

# Función para generar el link de cobro seguro
def generar_link_pago():
    token_mp = os.getenv('MP_ACCESS_TOKEN')
    if not token_mp:
        return "❌ Error: Llave de Tesorería no configurada."
    
    sdk = mercadopago.SDK(token_mp)
    preference_data = {
        "items": [
            {
                "title": "NeuraforgeAI - Membresía Junior / Forgecoins®",
                "quantity": 1,
                "unit_price": 100, # Precio en tu moneda local
                "currency_id": "MXN"
            }
        ],
        "auto_return": "approved",
        "back_urls": {"success": "https://t.me/NAI_sabroso_bot"}
    }
    try:
        result = sdk.preference().create(preference_data)
        return result["response"]["init_point"]
    except Exception as e:
        return "❌ Error en pasarela de pagos. Sistema en mantenimiento."

# --- COMANDOS DEL BOT ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    texto = (
        "🔥 ¡Bienvenido a **NeuraforgeAI®** y la era de **Forgecoins®**!\n\n"
        "Soy el bot oficial del **Escuadrón SABROSO** (Orion Cash System).\n"
        "Has llegado desde las nubes (Google/AWS) buscando algo mejor.\n\n"
        "Usa /comprar para adquirir tu acceso inicial o /info para saber más."
    )
    bot.reply_to(message, texto, parse_mode="Markdown")

@bot.message_handler(commands=['comprar'])
def send_payment(message):
    bot.reply_to(message, "⚙️ Conectando con el Treasury Core... generando tu acceso cifrado.")
    link = generar_link_pago()
    
    if "Error" in link:
        bot.reply_to(message, link)
    else:
        texto_pago = (
            "💰 **ACCESO GENERADO** 💰\n\n"
            "Haz clic en el siguiente enlace para completar tu aporte y recibir tus Forgecoins®:\n"
            f"🔗 {link}\n\n"
            "¡El mundo ágil te espera!"
        )
        bot.reply_to(message, texto_pago, parse_mode="Markdown")

@bot.message_handler(commands=['info'])
def send_info(message):
    texto = "Nuestra meta es crear un mundo más ágil reciclando hardware a cambio de la moneda global del futuro: **Forgecoins®**."
    bot.reply_to(message, texto, parse_mode="Markdown")

print("🚀 ESCUADRÓN SABROSO EN LÍNEA: @NAI_sabroso_bot está escuchando...")
bot.infinity_polling()
EOF
