#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import random
import logging
import sqlite3
from datetime import datetime
import requests
from threading import Thread
from flask import Flask, request, redirect, jsonify
import telebot

# ================= CONFIGURACIÓN =================
TELEGRAM_TOKEN = "8665608391:AAFs8OnNmbhFuADlPxD8ZEjCrSCubJiFkAU"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Links de Pago
LINK_149 = "https://mpago.li/1wbjMgo"
LINK_299 = "https://mpago.li/1ufHHLw"
LINK_499 = "https://mpago.li/1yg93jr"

AFILIADOS = {
    "google_cloud": "https://cloud.google.com/?referral=TU_ID",
    "didiapp": "https://www.didi.com/mx?ref=TU_ID"
}

# Configuración de base de datos en la nube
DB_PATH = "data/monetizacion.db"
if not os.path.exists("data"): os.makedirs("data")

app = Flask(__name__)

# ================= LÓGICA DE MONEDAS (FORGECOINS) =================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (user_id TEXT PRIMARY KEY, coins INTEGER DEFAULT 0, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS clicks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, tipo TEXT)''')
    conn.commit()
    conn.close()

def registro_nuevo_usuario(user_id):
    """Regala 50 Forgecoins al registrarse por primera vez"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO usuarios (user_id, coins, status) VALUES (?, ?, ?)", 
              (user_id, 50, 'preventa'))
    conn.commit()
    conn.close()

# ================= SERVER WEB (FLASK) =================
@app.route('/')
def home():
    return "Neuraforge AI Server Online", 200

@app.route('/google-home', methods=['POST'])
def google_home():
    # Respuesta para Google Assistant
    return jsonify({
        "fulfillmentText": "Hola de Neuraforge. He enviado el link de descarga y tus 50 Forgecoins de regalo a tu app."
    })

# ================= BOT DE TELEGRAM =================
@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = str(message.chat.id)
    registro_nuevo_usuario(user_id)
    texto = (f"🔥 **¡Bienvenido a NeuraforgeAI!** 🔥\n\n"
             f"Se han acreditado **50 Forgecoins®** en tu cuenta por preventa.\n"
             "Usa /preventa para comprar más o /bots para ver qué puedes activar.")
    bot.reply_to(message, texto, parse_mode="Markdown")

@bot.message_handler(commands=['preventa'])
def cmd_preventa(message):
    texto = (f"💰 **PREVENTA NEURAFORGE**\n\n"
             f"• Básico $149: {LINK_149}\n"
             f"• Pro $299: {LINK_299}\n")
    bot.reply_to(message, texto)

# ================= HILOS Y EJECUCIÓN =================
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    init_db()
    # Iniciar Bot en hilo separado
    Thread(target=run_bot).start()
    # Iniciar Flask en el hilo principal (requerido por Google Cloud)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
