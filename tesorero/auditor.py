import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import requests
import logging

logger = logging.getLogger(__name__)

class AuditorGlobalColmena:
    def __init__(self, ruta_credenciales="ruta/a/tu/firebase_credentials.json"):
        # Inicialización de Firebase (igual que antes)
        try:
            cred = credentials.Certificate(ruta_credenciales)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            logger.info("✅ Conexión al Auditor de Firebase establecida.")
        except Exception as e:
            logger.error(f"❌ Error al conectar con Firebase: {e}")
            self.db = None

    def obtener_pulso_global(self):
        """
        El bot "lee el periódico financiero" antes de guardar su registro.
        Extrae el precio del Bitcoin (como indicador cripto) y 
        podría extraer el tipo de cambio USD/BRL, oro, etc.
        """
        pulso = {}
        try:
            # Ejemplo: Obteniendo el precio global de Bitcoin y Ethereum vía API pública
            url_crypto = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
            respuesta = requests.get(url_crypto, timeout=3).json()
            pulso['btc_usd'] = respuesta.get('bitcoin', {}).get('usd', 0)
            pulso['eth_usd'] = respuesta.get('ethereum', {}).get('usd', 0)
            
            # Aquí podrías añadir llamadas a APIs de divisas (Forex) o índices de la bolsa
            # pulso['sp500'] = obtener_sp500()
            
        except Exception as e:
            logger.warning(f"No se pudo obtener el pulso global: {e}")
            pulso['error'] = "Datos globales no disponibles"
            
        return pulso

    def registrar_evento_macro(self, agente_id, accion, contexto, resultado=None):
        """
        Guarda la Acción local + El Contexto Macroeconómico Global.
        """
        if not self.db:
            return

        # El bot toma una fotografía de cómo está el mundo en este segundo
        estado_mundo = self.obtener_pulso_global()

        evento = {
            "timestamp": datetime.datetime.utcnow(),
            "agente_id": agente_id,      
            "accion": accion,            
            "contexto_local": contexto,  
            "contexto_global": estado_mundo, # <--- LA MAGIA ESTÁ AQUÍ
            "resultado_inmediato": resultado, 
            "analizado_por_ia": False    
        }

        try:
            self.db.collection("memoria_colmena_global").add(evento)
            logger.info(f"🧠 Memoria Macroeconómica registrada. BTC a ${estado_mundo.get('btc_usd', 'N/A')}")
        except Exception as e:
            logger.error(f"Error guardando memoria: {e}")

# ====================================================
# Ejecución:
# ====================================================
if __name__ == "__main__":
    auditor = AuditorGlobalColmena()
    
    # El Agente rescata un negocio, y guarda el estado del mundo en ese instante
    auditor.registrar_evento_macro(
        agente_id="Agente_Rescate_BR_045",
        accion="Inyeccion_Capital_Publicidad",
        contexto_local={"nicho": "Ferreteria", "monto_invertido": 500, "moneda_local": "BRL"},
        resultado="Campaña_Activada"
    )

