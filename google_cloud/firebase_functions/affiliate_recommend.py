# functions/affiliate_recommend.py
from firebase_functions import https_fn
from afiliados_estrategicos.affiliate_system import AffiliatePredictor

predictor = AffiliatePredictor()

@https_fn.on_request()
def recomendar_para_usuario(req):
    """Dado un usuario, recomienda servicios cloud"""
    data = req.get_json()
    uid = data['uid']
    
    # Obtener contexto del usuario desde Firestore
    user_doc = db.collection('usuarios').document(uid).get()
    contexto = {
        'categoria': user_doc.get('intereses', 'infraestructura'),
        'pais': user_doc.get('pais', 'MX'),
        'tipo_usuario': user_doc.get('tipo_usuario', 'emprendedor')
    }
    
    recomendaciones = predictor.recomendar(contexto)
    
    # Guardar en Firestore para mostrarlas en la app
    db.collection('recomendaciones').document(uid).set({
        'lista': recomendaciones,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    
    return {"recomendaciones": recomendaciones}
