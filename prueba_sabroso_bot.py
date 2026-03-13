import telebot
import requests
import os
import subprocess # Para disparar Termux API
--- CONFIGURACIÓN ---
TELEGRAM_TOKEN = "8140846319:AAE05LJCAZy-9gM-cL1YJOJLKIIzBlPvdYQ"
bot = telebot.TeleBot(TELEGRAM_TOKEN)
def enviar_notificacion_termux(titulo, mensaje):
    """Hace que tu celular vibre y muestre una notificación física"""
    try:
        # Comando: Título, Mensaje, Sonido y Vibración
        comando = f'termux-notification -t "{titulo}" -c "{mensaje}" --sound --vibrate 500'
        subprocess.run(comando, shell=True)
    except Exception as e:
        print(f"Error en notificación física: {e}")
@bot.message_handler(commands=['comprar_junior'])
def pagar_junior(message):
    usuario = message.from_user.first_name
# Notificación local para ti
enviar_notificacion_termux(
    "🚀 Intento de Compra", 
    f"El usuario {usuario} está generando una orden de Forgecoins."
)

# Simulación de generación de link (Aquí va tu lógica de Binance)
bot.reply_to(message, "💎 Generando orden en Binance Pay...")

# Simulamos éxito de pago para la prueba
link_pago = "https://bpay.binance.com/link_de_prueba"
bot.reply_to(message, f"✅ Orden lista: {link_pago}")

@bot.message_handler(commands=['confirmar_pago']) # Comando interno para pruebas
def confirmacion_test(message):
    # Esto es lo que se disparará cuando la API de Binance confirme el pago
    enviar_notificacion_termux(
        "💰 ¡INGRESO DETECTADO!", 
        "Se han recibido 10.00 USDT en el Treasury Core. Forgecoins liberados."
    )
    bot.reply_to(message, "¡Pago verificado! Tus Forgecoins® han sido acreditados.")
print("🚀 NeuraforgeAI con Notificaciones Físicas activo...")
bot.infinity_polling()
