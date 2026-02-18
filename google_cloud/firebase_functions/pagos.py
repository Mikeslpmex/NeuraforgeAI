# functions/pagos.py
from firebase_functions import https_fn
import stripe  # o Openpay

@https_fn.on_request()
def actualizar_a_premium(req):
    """Endpoint llamado después de un pago exitoso"""
    data = req.get_json()
    uid = data['uid']
    
    # Actualizar licencia
    db.collection('licencias').document(uid).update({
        'tipo': 'premium',
        'ads_activos': False,
        'limite_bots': 5,
        'fecha_actualizacion': firestore.SERVER_TIMESTAMP
    })
    
    return {"status": "ok"}
