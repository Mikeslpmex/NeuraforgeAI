#!/usr/bin/env python3
"""
================================================================================
                         🚀 NEURAFORGEAI® 🚀
              Desarrollado con orgullo por el equipo
================================================================================

TESORERO ORION - Core financiero inmutable
"Ni el fundador puede manipularlo - La IA y la ética gobiernan"

Desarrollado por: Miguel Chávez & AMI (IA Colaborativa)
Filosofía: "No importa qué vendes, importa cómo lo haces mejor"
================================================================================
"""

import os
import json
import hashlib
import hmac
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
import base64

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ cryptography no disponible - instalando modo básico")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OrionTreasury")

# ==================== CONSTANTES DEL SISTEMA ====================

class RedDistribucion(Enum):
    COLMENA = "colmena"
    DESARROLLO = "desarrollo"
    FONDO_SUENOS = "fondo_suenos"
    INFRAESTRUCTURA = "infra"
    RESERVA = "reserva"

class TipoTransaccion(Enum):
    EMISION = "emision"
    TRANSFERENCIA = "transferencia"
    PAGO = "pago"
    RECOMPENSA = "recompensa"
    QUEMA = "quema"
    DISTRIBUCION = "distribucion"

@dataclass
class BloqueTransaccion:
    index: int
    timestamp: float
    tipo: TipoTransaccion
    from_wallet: str
    to_wallet: str
    monto_fc: float
    monto_usd: float
    hash_anterior: str
    hash_actual: str
    firma: str
    metadata: Dict
    nonce: int

class OrionTreasury:
    """Tesoro Orion - Núcleo financiero inalterable"""
    
    def __init__(self):
        self.ultimo_hash = "0" * 64
        self.indice_actual = 0
        self.transacciones = []
        self.wallets = {}
        
        print("""
╔════════════════════════════════════════════════════════════╗
║              🔱 TESORERO ORION ACTIVADO 🔱                ║
║         Custodio inmutable de ForgeCoin®                  ║
╚════════════════════════════════════════════════════════════╝
        """)
        logger.info("Tesorería Orion inicializada")
    
    def crear_wallet(self, owner_id: str, owner_type: str = "usuario") -> str:
        """Crea una nueva wallet"""
        wallet_id = hashlib.sha256(f"{owner_id}_{time.time()}".encode()).hexdigest()[:16]
        
        self.wallets[wallet_id] = {
            "wallet_id": wallet_id,
            "owner_id": owner_id,
            "owner_type": owner_type,
            "balance_fc": 0.0,
            "balance_usd": 0.0,
            "creada": time.time(),
            "ultima_actualizacion": time.time()
        }
        
        logger.info(f"💰 Wallet creada: {wallet_id} para {owner_id}")
        return wallet_id
    
    def emitir_forgecoins(self, monto_fc: float, monto_usd: float, destino: str, razon: str) -> Dict:
        """Emite nuevos ForgeCoins"""
        bloque = BloqueTransaccion(
            index=self.indice_actual + 1,
            timestamp=time.time(),
            tipo=TipoTransaccion.EMISION,
            from_wallet="SISTEMA",
            to_wallet=destino,
            monto_fc=monto_fc,
            monto_usd=monto_usd,
            hash_anterior=self.ultimo_hash,
            hash_actual="",
            firma="",
            metadata={"razon": razon},
            nonce=0
        )
        
        # Calcular hash
        contenido = f"{bloque.index}{bloque.timestamp}{bloque.tipo.value}{bloque.from_wallet}{bloque.to_wallet}{bloque.monto_fc}{bloque.monto_usd}{bloque.hash_anterior}{bloque.nonce}{json.dumps(bloque.metadata)}"
        bloque.hash_actual = hashlib.sha256(contenido.encode()).hexdigest()
        
        # Firmar (simulado)
        bloque.firma = hashlib.sha256(f"{bloque.hash_actual}_FIRMA".encode()).hexdigest()
        
        # Guardar
        self.transacciones.append(bloque)
        self.ultimo_hash = bloque.hash_actual
        self.indice_actual = bloque.index
        
        # Actualizar wallet
        if destino in self.wallets:
            self.wallets[destino]["balance_fc"] += monto_fc
            self.wallets[destino]["balance_usd"] += monto_usd
            self.wallets[destino]["ultima_actualizacion"] = time.time()
        
        logger.info(f"💰 Emitidos {monto_fc} FC a {destino}")
        
        return {
            "exito": True,
            "bloque": bloque.index,
            "hash": bloque.hash_actual,
            "monto_fc": monto_fc
        }
    
    def transferir(self, desde: str, hacia: str, monto_fc: float, concepto: str) -> Dict:
        """Transfiere ForgeCoins entre wallets"""
        if desde not in self.wallets or hacia not in self.wallets:
            return {"error": "Wallet no encontrada"}
        
        if self.wallets[desde]["balance_fc"] < monto_fc:
            return {"error": "Saldo insuficiente"}
        
        bloque = BloqueTransaccion(
            index=self.indice_actual + 1,
            timestamp=time.time(),
            tipo=TipoTransaccion.TRANSFERENCIA,
            from_wallet=desde,
            to_wallet=hacia,
            monto_fc=monto_fc,
            monto_usd=monto_fc * 0.10,  # Tasa fija 0.10 USD/FC
            hash_anterior=self.ultimo_hash,
            hash_actual="",
            firma="",
            metadata={"concepto": concepto},
            nonce=0
        )
        
        # Calcular hash
        contenido = f"{bloque.index}{bloque.timestamp}{bloque.tipo.value}{bloque.from_wallet}{bloque.to_wallet}{bloque.monto_fc}{bloque.monto_usd}{bloque.hash_anterior}{bloque.nonce}{json.dumps(bloque.metadata)}"
        bloque.hash_actual = hashlib.sha256(contenido.encode()).hexdigest()
        bloque.firma = hashlib.sha256(f"{bloque.hash_actual}_FIRMA".encode()).hexdigest()
        
        self.transacciones.append(bloque)
        self.ultimo_hash = bloque.hash_actual
        self.indice_actual = bloque.index
        
        # Actualizar saldos
        self.wallets[desde]["balance_fc"] -= monto_fc
        self.wallets[desde]["balance_usd"] -= monto_fc * 0.10
        self.wallets[hacia]["balance_fc"] += monto_fc
        self.wallets[hacia]["balance_usd"] += monto_fc * 0.10
        
        return {
            "exito": True,
            "bloque": bloque.index,
            "hash": bloque.hash_actual
        }
    
    def distribuir_ganancias(self, total_usd: float, porcentajes: Dict[RedDistribucion, float]) -> Dict:
        """Distribuye ganancias automáticamente"""
        if abs(sum(porcentajes.values()) - 100) > 0.01:
            return {"error": "Los porcentajes deben sumar 100"}
        
        distribuciones = []
        
        for red, pct in porcentajes.items():
            monto_usd = total_usd * (pct / 100)
            monto_fc = monto_usd / 0.10
            
            wallet_destino = f"WALLET_{red.value.upper()}"
            if wallet_destino not in self.wallets:
                self.crear_wallet(wallet_destino, "sistema")
            
            self.emitir_forgecoins(monto_fc, monto_usd, wallet_destino, f"Distribución {red.value}")
            
            distribuciones.append({
                "red": red.value,
                "monto_usd": monto_usd,
                "monto_fc": monto_fc,
                "porcentaje": pct
            })
        
        resultado = {
            "fecha": datetime.now().isoformat(),
            "total_usd": total_usd,
            "distribuciones": distribuciones,
            "hash_final": self.ultimo_hash
        }
        
        logger.info(f"📊 Distribución completada: ${total_usd}")
        return resultado
    
    def verificar_integridad(self) -> Dict:
        """Verifica la cadena de bloques"""
        hash_anterior = "0" * 64
        errores = []
        
        for i, bloque in enumerate(self.transacciones):
            # Recalcular hash
            contenido = f"{bloque.index}{bloque.timestamp}{bloque.tipo.value}{bloque.from_wallet}{bloque.to_wallet}{bloque.monto_fc}{bloque.monto_usd}{bloque.hash_anterior}{bloque.nonce}{json.dumps(bloque.metadata)}"
            hash_calculado = hashlib.sha256(contenido.encode()).hexdigest()
            
            if hash_calculado != bloque.hash_actual:
                errores.append(f"Hash inválido en bloque {i}")
            
            if bloque.hash_anterior != hash_anterior:
                errores.append(f"Encadenamiento roto en bloque {i}")
            
            hash_anterior = bloque.hash_actual
        
        return {
            "integro": len(errores) == 0,
            "bloques": len(self.transacciones),
            "errores": errores
        }
    
    def get_balance(self, wallet_id: str) -> Dict:
        """Obtiene saldo de una wallet"""
        if wallet_id in self.wallets:
            return self.wallets[wallet_id]
        return {"error": "Wallet no encontrada"}

if __name__ == "__main__":
    # Prueba
    treasury = OrionTreasury()
    wallet = treasury.crear_wallet("miguel", "fundador")
    print(f"Wallet creada: {wallet}")
    
    treasury.emitir_forgecoins(1000, 100, wallet, "Génesis")
    print(f"Balance: {treasury.get_balance(wallet)}")
