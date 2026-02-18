# functions/google_home_fulfillment.py
from firebase_functions import https_fn

@https_fn.on_request()
def google_home_webhook(req):
    """Maneja las peticiones de Google Home"""
    body = req.get_json()
    
    intent = body['intent']['name']
    
    if intent == 'seleccionar_bot':
        bot_tipo = body['intent']['params']['bot_tipo']
        # Generar link de descarga personalizado
        link = f"https://neuraforge.ai/descargar?bot={bot_tipo}"
        respuesta = f"Has elegido el bot de {bot_tipo}. Te enviaremos un enlace a tu teléfono para descargar la app."
        
        # Opcional: enviar SMS con el enlace (usando Twilio)
        
        return {
            "fulfillment_response": {
                "messages": [{
                    "text": {
                        "text": [respuesta]
                    }
                }]
            }
        }
    
    return {"fulfillment_response": {"messages": [{"text": {"text": ["No entendí"]}}]}}
