#!/usr/bin/env python3
"""
Script de prueba para el bot de afiliados (Cloud Function)
Ejecuta: python test_affiliate.py
"""

import requests
import json

# Configura la URL de tu Cloud Function (reemplaza con la tuya)
BASE_URL = "https://us-central1-whatsappbotpro-c36801.cloudfunctions.net/affiliate-bot"

def probar_recomendar():
    """Prueba el endpoint /recomendar"""
    print("\n🔍 Probando /recomendar (GET con parámetro categoria)...")
    try:
        respuesta = requests.get(f"{BASE_URL}/recomendar", params={"categoria": "infraestructura"})
        if respuesta.status_code == 200:
            data = respuesta.json()
            print("✅ Éxito. Recomendaciones:")
            for r in data["recomendaciones"]:
                print(f"   - {r['servicio']} (confianza {r['confianza']}%)")
        else:
            print(f"❌ Error {respuesta.status_code}: {respuesta.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")

def probar_generar_enlace():
    """Prueba el endpoint /generar_enlace"""
    print("\n🔍 Probando /generar_enlace (POST)...")
    payload = {
        "servicio": "GOOGLE_CLOUD",
        "usuario": "test_user_123",
        "fuente": "test"
    }
    try:
        respuesta = requests.post(f"{BASE_URL}/generar_enlace", json=payload)
        if respuesta.status_code == 200:
            data = respuesta.json()
            print(f"✅ Éxito. URL generada: {data['url']}")
            print(f"   Click ID: {data['click_id']}")
            return data['click_id']
        else:
            print(f"❌ Error {respuesta.status_code}: {respuesta.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")
    return None

def probar_conversion(click_id):
    """Prueba el endpoint /conversion"""
    if not click_id:
        print("⚠️ No hay click_id para probar conversión")
        return
    print("\n🔍 Probando /conversion (POST)...")
    payload = {
        "click_id": click_id,
        "valor_usd": 100.0
    }
    try:
        respuesta = requests.post(f"{BASE_URL}/conversion", json=payload)
        if respuesta.status_code == 200:
            data = respuesta.json()
            print(f"✅ Éxito. Conversión registrada:")
            print(f"   Click ID: {data['click_id']}")
            print(f"   Servicio: {data['servicio']}")
            print(f"   Comisión: ${data['comision_usd']}")
        else:
            print(f"❌ Error {respuesta.status_code}: {respuesta.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")

def probar_estadisticas():
    """Prueba el endpoint /estadisticas"""
    print("\n🔍 Probando /estadisticas (GET)...")
    try:
        respuesta = requests.get(f"{BASE_URL}/estadisticas")
        if respuesta.status_code == 200:
            data = respuesta.json()
            print("✅ Éxito. Estadísticas:")
            print(f"   Total clicks: {data['total_clicks']}")
            print(f"   Conversiones: {data['total_conversiones']}")
            print(f"   Tasa conversión: {data['tasa_conversion']:.2f}%")
            print(f"   Comisiones generadas: ${data['comisiones_generadas_usd']}")
        else:
            print(f"❌ Error {respuesta.status_code}: {respuesta.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del bot de afiliados")
    print(f"📡 URL base: {BASE_URL}")
    
    click_id = None
    
    # Prueba 1: recomendaciones
    probar_recomendar()
    
    # Prueba 2: generar enlace
    click_id = probar_generar_enlace()
    
    # Prueba 3: simular conversión (si tenemos click_id)
    probar_conversion(click_id)
    
    # Prueba 4: estadísticas
    probar_estadisticas()
    
    print("\n🏁 Pruebas completadas.")
