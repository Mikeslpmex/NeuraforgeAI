# functions/whatsapp_webhook.py
from firebase_functions import https_fn
import json

@https_fn.on_request()
def whatsapp_webhook(req):
    """Recibe mensajes de WhatsApp y los dirige al bot correspondiente"""
    if req.method == 'GET':
        # Verificación del webhook (WhatsApp exige)
        verify_token = "neuraforge_whatsapp_123"
        mode = req.args.get('hub.mode')
        token = req.args.get('hub.verify_token')
        challenge = req.args.get('hub.challenge')
        if mode == 'subscribe' and token == verify_token:
            return challenge
        else:
            return "Verificación fallida", 403
    
    # POST: mensaje entrante
    data = req.get_json()
    numero_cliente = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    texto = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    
    # Buscar qué bot atiende este número (está asociado al número del negocio)
    # El número del negocio viene en el webhook como metadata
    negocio_numero = data['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']
    
    # Buscar en Firestore el bot asociado a negocio_numero
    bot_doc = db.collection('bots').where('telefono_whatsapp', '==', negocio_numero).limit(1).get()
    if not bot_doc:
        return "Bot no encontrado", 404
    
    bot_data = bot_doc[0].to_dict()
    bot_tipo = bot_data['tipo']
    
    # Ejecutar lógica del bot (pizza, taxi, etc.)
    respuesta = ejecutar_bot(bot_tipo, texto)
    
    # Enviar respuesta por WhatsApp (usando la API de WhatsApp)
    enviar_whatsapp(numero_cliente, respuesta)
    
    return "OK", 200
