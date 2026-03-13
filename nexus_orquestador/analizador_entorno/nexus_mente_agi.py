import json
import logging
from typing import Dict, Any
# Importa la librería de tu modelo LLM (p. ej., gemini, openai, llama)
# from gemini_api import AGI_Client 

logger = logging.getLogger("NEXUS_MENTE")

# Simulación del cliente AGI para el ejemplo
class AGI_Client:
    def generate_strategy(self, prompt: str, context: Dict) -> str:
        # En una implementación real, esto sería una llamada a la API del modelo
        # que recibe el contexto y el prompt y devuelve un JSON.
        
        # Lógica SIMULADA del AGI basada en la tendencia:
        tendencia = context.get('tendencia_keyword', 'default')
        
        if 'hotmart' in tendencia.lower() or 'curso' in tendencia.lower():
            return json.dumps({
                "modo_contenido": "informativo",
                "canales": ["telegram", "whatsapp_premium"],
                "agresividad": "media"
            })
        elif 'moda' in tendencia.lower() or 'viral' in tendencia.lower():
            return json.dumps({
                "modo_contenido": "viral",
                "canales": ["twitter", "telegram_general"],
                "agresividad": "alta"
            })
        else:
            return json.dumps({
                "modo_contenido": "estándar",
                "canales": ["telegram_general"],
                "agresividad": "baja"
            })


def establecer_estrategia(datos_analizador: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recibe el contexto y llama al AGI para obtener la estrategia de acción.
    """
    logger.info("🧠 Consultado NEXUS-Mente para estrategia de campaña...")
    
    # 1. Preparar el Contexto para el AGI (RAG)
    contexto_llm = {
        "zona_caliente_principal": datos_analizador.get('zona_caliente_principal', 'N/A'),
        "tendencia_keyword": datos_analizador.get('tendencia_principal', 'N/A'),
        "lead_score_avg": datos_analizador.get('score_promedio', 0.5),
        "reporte_anterior": datos_analizador.get('reporte_campana_anterior', None)
    }

    # 2. El Prompt (Tu interfaz AGI)
    prompt_estrategia = (
        "Eres un estratega de marketing de afiliados. Analiza el contexto de operación "
        "y genera una estrategia de contenido y promoción en formato JSON. "
        "Prioriza el ROI sobre el volumen."
    )

    # 3. Llamada al AGI y parsing
    agi_client = AGI_Client()
    try:
        respuesta_json_str = agi_client.generate_strategy(prompt_estrategia, contexto_llm)
        estrategia = json.loads(respuesta_json_str)
        logger.info(f"✅ Estrategia AGI generada: {estrategia}")
        return estrategia
    except Exception as e:
        logger.error(f"❌ Fallo al obtener estrategia del AGI: {e}. Usando fallback.")
        return {"modo_contenido": "estándar", "canales": ["telegram_general"], "agresividad": "media"}

