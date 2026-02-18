import os
import json
import hashlib
import hmac
import time
import random
from datetime import datetime
from typing import Dict, List, Optional

import firebase_admin
from firebase_admin import firestore
import requests

# Inicializar Firebase
firebase_admin.initialize_app()
db = firestore.client()

# ==================== CONFIGURACIÓN ====================
SERVICIOS = {
    "GOOGLE_CLOUD": {
        "nombre": "Google Cloud",
        "comision": 0.15,
        "url_base": "https://cloud.google.com/?affiliate=neuraforge",
        "categoria": "infraestructura"
    },
    "AWS": {
        "nombre": "Amazon Web Services",
        "comision": 0.10,
        "url_base": "https://aws.amazon.com/?affiliate=neuraforge",
        "categoria": "infraestructura"
    },
    "ORACLE_CLOUD": {
        "nombre": "Oracle Cloud",
        "comision": 0.20,
        "url_base": "https://www.oracle.com/cloud/?affiliate=neuraforge",
        "categoria": "infraestructura"
    },
    "DIGITAL_OCEAN": {
        "nombre": "Digital Ocean",
        "comision": 0.25,
        "url_base": "https://www.digitalocean.com/?affiliate=neuraforge",
        "categoria": "vps"
    },
    "VERCEL": {
        "nombre": "Vercel",
        "comision": 0.20,
        "url_base": "https://vercel.com/?affiliate=neuraforge",
        "categoria": "hosting"
    }
}

# ==================== FUNCIONES PRINCIPALES ====================

def generar_id_unico(prefix=""):
    """Genera ID único basado en timestamp + random"""
    unique = f"{time.time()}{random.random()}"
    return prefix + hashlib.md5(unique.encode()).hexdigest()[:8]

def generar_url_afiliado(servicio: str, usuario: str, fuente: str = "web") -> str:
    """Genera URL de afiliado con parámetros de tracking"""
    if servicio not in SERVICIOS:
        return None
    
    base = SERVICIOS[servicio]["url_base"]
    ref = generar_id_unico("ref_")
    
    # Guardar click en Firestore
    click_data = {
        "click_id": ref,
        "servicio": servicio,
        "usuario": usuario,
        "fuente": fuente,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "convertido": False
    }
    db.collection("affiliate_clicks").document(ref).set(click_data)
    
    # Construir URL
    if '?' in base:
        url = f"{base}&ref={ref}&utm_source=neuraforge&utm_medium={fuente}"
    else:
        url = f"{base}?ref={ref}&utm_source=neuraforge&utm_medium={fuente}"
    
    return url

def recomendar_servicios(contexto: Dict) -> List[Dict]:
    """Recomienda servicios según contexto del usuario"""
    recomendaciones = []
    for codigo, servicio in SERVICIOS.items():
        # Simular puntuación de relevancia
        score = random.uniform(0.5, 0.95)
        # Ajustar por categoría si viene en contexto
        if contexto.get("categoria") == servicio["categoria"]:
            score += 0.2
        if score > 0.7:
            recomendaciones.append({
                "servicio": servicio["nombre"],
                "codigo": codigo,
                "comision": f"{servicio['comision']*100:.0f}%",
                "confianza": round(score * 100, 1),
                "categoria": servicio["categoria"]
            })
    # Ordenar por confianza
    recomendaciones.sort(key=lambda x: x["confianza"], reverse=True)
    return recomendaciones[:3]

def procesar_conversion(click_id: str, valor_usd: float) -> Dict:
    """Procesa una conversión (venta) desde un click"""
    click_ref = db.collection("affiliate_clicks").document(click_id)
    click = click_ref.get()
    if not click.exists:
        return {"error": "Click no encontrado"}
    
    if click.get("convertido"):
        return {"error": "Click ya convertido"}
    
    servicio = click.get("servicio")
    comision = valor_usd * SERVICIOS[servicio]["comision"]
    
    # Actualizar click
    click_ref.update({
        "convertido": True,
        "valor_usd": valor_usd,
        "comision_usd": comision,
        "fecha_conversion": firestore.SERVER_TIMESTAMP
    })
    
    # Registrar en Tesorero (simulado, luego lo conectamos)
    # Aquí llamarías a Orion Treasury para emitir Forge Coins
    # treasury.emitir_forgecoins(comision / 0.10, comision, "afiliados", click.get("usuario"))
    
    return {
        "exito": True,
        "click_id": click_id,
        "servicio": servicio,
        "valor_usd": valor_usd,
        "comision_usd": comision,
        "usuario": click.get("usuario")
    }

def obtener_estadisticas(usuario: Optional[str] = None) -> Dict:
    """Obtiene estadísticas de clicks y conversiones"""
    query = db.collection("affiliate_clicks")
    if usuario:
        query = query.where("usuario", "==", usuario)
    
    clicks = list(query.stream())
    
    total_clicks = len(clicks)
    convertidos = [c for c in clicks if c.get("convertido")]
    total_conversiones = len(convertidos)
    comisiones = sum(c.get("comision_usd", 0) for c in convertidos)
    
    return {
        "total_clicks": total_clicks,
        "total_conversiones": total_conversiones,
        "tasa_conversion": (total_conversiones / total_clicks * 100) if total_clicks > 0 else 0,
        "comisiones_generadas_usd": round(comisiones, 2),
        "servicios": {
            s: {
                "clicks": sum(1 for c in clicks if c.get("servicio") == s),
                "conversiones": sum(1 for c in convertidos if c.get("servicio") == s)
            }
            for s in SERVICIOS
        }
    }

# ==================== ENDPOINTS HTTP ====================

def generar_enlace(request):
    """Endpoint: POST con JSON {servicio, usuario, fuente}"""
    if request.method != 'POST':
        return {"error": "Método no permitido"}, 405
    
    data = request.get_json()
    servicio = data.get("servicio")
    usuario = data.get("usuario", "anonimo")
    fuente = data.get("fuente", "web")
    
    url = generar_url_afiliado(servicio, usuario, fuente)
    if not url:
        return {"error": "Servicio no válido"}, 400
    
    return {
        "url": url,
        "click_id": url.split("ref=")[-1].split("&")[0]
    }

def recomendar(request):
    """Endpoint: POST con JSON {contexto} o GET con parámetros"""
    if request.method == 'GET':
        # Desde web, parámetros en query string
        categoria = request.args.get("categoria", "infraestructura")
        contexto = {"categoria": categoria}
    else:
        data = request.get_json() or {}
        contexto = data.get("contexto", {})
    
    recomendaciones = recomendar_servicios(contexto)
    return {"recomendaciones": recomendaciones}

def conversion_webhook(request):
    """Endpoint para notificaciones de conversión (desde el servicio afiliado simulado o real)"""
    if request.method != 'POST':
        return {"error": "Método no permitido"}, 405
    
    data = request.get_json()
    click_id = data.get("click_id")
    valor_usd = data.get("valor_usd")
    
    if not click_id or not valor_usd:
        return {"error": "Faltan datos"}, 400
    
    resultado = procesar_conversion(click_id, valor_usd)
    return resultado

def estadisticas(request):
    """Endpoint para obtener estadísticas (público o privado)"""
    usuario = request.args.get("usuario")
    stats = obtener_estadisticas(usuario)
    return stats

# ==================== ENTRY POINT (Cloud Function) ====================

def affiliate_bot(request):
    """Dispatcher principal para manejar múltiples rutas"""
    path = request.path
    
    if path == "/generar_enlace" or path == "/enlace":
        return generar_enlace(request)
    elif path == "/recomendar":
        return recomendar(request)
    elif path == "/conversion":
        return conversion_webhook(request)
    elif path == "/estadisticas":
        return estadisticas(request)
    else:
        # Ruta raíz: mostrar información
        return {
            "servicio": "NeuraForge Affiliate Bot",
            "version": "1.0",
            "endpoints": ["/generar_enlace", "/recomendar", "/conversion", "/estadisticas"]
        }
