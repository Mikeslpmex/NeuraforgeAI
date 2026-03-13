import hashlib
import secrets
import base64
import os
import json
from datetime import datetime

def generar_llave_maestra_neuraforge():
    print("⛩️ Iniciando Forja de Seguridad QuantumShield...")
    
    # 1. Generar una entropía criptográfica (El ADN único de tu instalación)
    entropia = secrets.token_bytes(64)
    
    # 2. Tu frase de paso maestra (La que teclearás en la consola)
    password_plana = input("Introduce la contraseña maestra para el Oráculo/Tesorero: ")
    
    # 3. Derivación de claves usando PBKDF2 (Resistente a ataques de fuerza bruta)
    salt = secrets.token_hex(16)
    clave_derivada = hashlib.pbkdf2_hmac(
        'sha256', 
        password_plana.encode('utf-8'), 
        salt.encode('utf-8'), 
        250000 # Iteraciones de seguridad
    )
    
    # 4. El Hash Génesis (El que se guarda y se usa para verificar)
    genesis_hash = base64.b64encode(clave_derivada).decode('utf-8')
    
    # Empaquetar el manifiesto de seguridad
    manifiesto = {
        "timestamp_creacion": datetime.now().isoformat(),
        "algoritmo": "PBKDF2-HMAC-SHA256",
        "iteraciones": 250000,
        "salt": salt,
        "genesis_hash": genesis_hash,
        "advertencia": "ESTE ARCHIVO NUNCA DEBE SUBIRSE A GITHUB"
    }
    
    # Guardar en un archivo local oculto
    ruta_boveda = ".quantum_vault_keys.json"
    with open(ruta_boveda, "w") as f:
        json.dump(manifiesto, f, indent=4)
        
    print("\n✅ [ÉXITO] Hash Génesis Forjado.")
    print(f"🔒 El hash inmutable es: {genesis_hash}")
    print(f"🥷 Archivo de seguridad guardado localmente en: {ruta_boveda}")
    print("⚠️ IMPORTANTE: Asegúrate de añadir '.quantum_vault_keys.json' a tu archivo .gitignore")

if __name__ == "__main__":
    generar_llave_maestra_neuraforge()

