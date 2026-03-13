import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Inicialización de Firebase
# Al usar Application Default Credentials (ADC), este código funcionará 
# automáticamente con Workload Identity cuando lo configures, sin cambiar nada aquí.
try:
    firebase_admin.get_app()
except ValueError:
    # Si aún no tienes Workload Identity, por ahora usa tu JSON local de desarrollo
    # cred = credentials.Certificate("../config/firebase_credenciales.json")
    # firebase_admin.initialize_app(cred)
    
    # Lo ideal a futuro usando el entorno:
    firebase_admin.initialize_app()

db = firestore.client()

def registrar_interaccion(id_usuario, modulo_origen, accion, respuesta, exito=True, metadatos=None):
    """
    Envía un registro estructurado a la base de datos para futuro entrenamiento de IA.
    """
    coleccion = db.collection('neuraforge_analitica_ia')
    
    # Estructura del "Pensamiento" para la IA
    documento = {
        'timestamp': firestore.SERVER_TIMESTAMP,
        'id_usuario': str(id_usuario),
        'contexto': {
            'modulo': modulo_origen,       # Ej. 'Tesorero Orion', 'Bot Pizza'
            'estado_exito': exito          # True si la tarea se completó, False si falló
        },
        'interaccion': {
            'accion_usuario': accion,      # Ej. '/comprar_licencia', 'intento_pago_efectivo'
            'respuesta_sistema': respuesta # Ej. 'pago_aprobado', 'saldo_insuficiente'
        },
        'metricas': metadatos or {}        # Diccionario libre para valores (Ej. {'monto': 499, 'moneda': 'MXN'})
    }
    
    try:
        # Usamos add() para generar un ID de documento automático
        db.collection('neuraforge_analitica_ia').add(documento)
        print(f"[+] Dato analítico registrado en la colmena para el usuario: {id_usuario}")
    except Exception as e:
        print(f"[-] Error crítico al registrar en telemetría: {e}")

# Bloque de prueba local
if __name__ == "__main__":
    print("Iniciando prueba de conexión con Firebase Analítica...")
    registrar_interaccion(
        id_usuario="usr_alpha_001",
        modulo_origen="monetizador.py",
        accion="solicitud_pago_licencia",
        respuesta="generacion_referencia_oxxo",
        exito=True,
        metadatos={"precio": 499, "producto": "licencia_neuraforge"}
    )
