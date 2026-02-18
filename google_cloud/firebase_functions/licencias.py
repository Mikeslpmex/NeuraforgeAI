# functions/licencias.py
from firebase_functions import auth_fn
from firebase_admin import firestore

db = firestore.client()

@auth_fn.on_user_created()
def asignar_licencia_gratis(user):
    """Cuando un usuario se registra, le asigna licencia gratis"""
    uid = user.uid
    # Crear documento de licencia
    db.collection('licencias').document(uid).set({
        'tipo': 'gratis',
        'ads_activos': True,
        'limite_bots': 1,
        'funciones_premium': [],
        'fecha_asignacion': firestore.SERVER_TIMESTAMP
    })
    # Crear wallet
    wallet_id = f"wallet_{uid}"
    db.collection('wallets').document(wallet_id).set({
        'uid': uid,
        'balance_fc': 0.0,
        'balance_usd': 0.0,
        'creada': firestore.SERVER_TIMESTAMP
    })
    print(f"Licencia gratis asignada a {uid}")
