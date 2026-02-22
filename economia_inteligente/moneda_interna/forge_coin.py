#!/usr/bin/env python3
"""
================================================================================
                         🚀 NEURAFORGEAI® 🚀
              Desarrollado con orgullo por el equipo
================================================================================

FORGE COIN - Moneda interna de NeuraForgeAI
"El primer Bitcoin gestionado por IA"

Desarrollado por: Miguel Chávez & AMI (IA Colaborativa)
================================================================================
"""

import hashlib
import json
import time
import uuid
import os
from typing import Dict, List, Optional
from datetime import datetime

class ForgeCoinWallet:
    """Cartera digital de Forge Coins"""
    
    def __init__(self, owner_id: str, owner_type: str = "usuario"):
        self.owner_id = owner_id
        self.owner_type = owner_type
        self.wallet_id = self._generate_id()
        self.balance = 0.0
        self.transactions = []
        self.created_at = time.time()
        
    def _generate_id(self) -> str:
        unique = f"{self.owner_id}_{self.owner_type}_{time.time()}"
        return hashlib.sha256(unique.encode()).hexdigest()[:16]
    
    def add_funds(self, amount: float, concept: str, source: str = "system") -> Dict:
        """Añade fondos a la wallet"""
        tx = {
            "id": str(uuid.uuid4()),
            "tipo": "credito",
            "from": source,
            "to": self.wallet_id,
            "amount": amount,
            "concept": concept,
            "timestamp": time.time(),
            "new_balance": self.balance + amount
        }
        
        self.balance += amount
        self.transactions.append(tx)
        
        return tx
    
    def spend(self, amount: float, concept: str, to_wallet: str) -> Optional[Dict]:
        """Gasta fondos de la wallet"""
        if self.balance < amount:
            return None
        
        tx = {
            "id": str(uuid.uuid4()),
            "tipo": "debito",
            "from": self.wallet_id,
            "to": to_wallet,
            "amount": amount,
            "concept": concept,
            "timestamp": time.time(),
            "new_balance": self.balance - amount
        }
        
        self.balance -= amount
        self.transactions.append(tx)
        
        return tx
    
    def get_balance(self) -> float:
        return self.balance
    
    def get_transactions(self, limit: int = 10) -> List[Dict]:
        return sorted(self.transactions, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def to_dict(self) -> Dict:
        return {
            "wallet_id": self.wallet_id,
            "owner_id": self.owner_id,
            "owner_type": self.owner_type,
            "balance": self.balance,
            "created_at": self.created_at,
            "transaction_count": len(self.transactions)
        }

class ForgeCoinSystem:
    """Sistema global de Forge Coins"""
    
    def __init__(self):
        self.wallets: Dict[str, ForgeCoinWallet] = {}
        self.exchange_rate_usd = 0.10
        
        print("""
╔════════════════════════════════════════════════════════════╗
║              💰 FORGE COIN SYSTEM ACTIVO 💰               ║
║      El primer Bitcoin gestionado por IA - NeuraForge     ║
╚════════════════════════════════════════════════════════════╝
        """)
    
    def create_wallet(self, owner_id: str, owner_type: str = "usuario") -> ForgeCoinWallet:
        """Crea una nueva wallet"""
        wallet = ForgeCoinWallet(owner_id, owner_type)
        self.wallets[wallet.wallet_id] = wallet
        return wallet
    
    def get_wallet(self, wallet_id: str) -> Optional[ForgeCoinWallet]:
        return self.wallets.get(wallet_id)
    
    def transfer(self, from_wallet: str, to_wallet: str, amount: float, concept: str) -> Optional[Dict]:
        """Transfiere fondos entre wallets"""
        if from_wallet not in self.wallets or to_wallet not in self.wallets:
            return None
        
        tx = self.wallets[from_wallet].spend(amount, concept, to_wallet)
        if tx:
            self.wallets[to_wallet].add_funds(amount, concept, from_wallet)
            return tx
        
        return None
    
    def convert_to_usd(self, fc_amount: float) -> float:
        """Convierte Forge Coins a USD"""
        return fc_amount * self.exchange_rate_usd
    
    def convert_from_usd(self, usd_amount: float) -> float:
        """Convierte USD a Forge Coins"""
        return usd_amount / self.exchange_rate_usd
    
    def get_total_supply(self) -> float:
        """Obtiene el total de Forge Coins en circulación"""
        return sum(w.balance for w in self.wallets.values())

# Ejemplo
if __name__ == "__main__":
    fc = ForgeCoinSystem()
    
    wallet1 = fc.create_wallet("miguel", "fundador")
    wallet2 = fc.create_wallet("comunidad", "colmena")
    
    wallet1.add_funds(1000, "Génesis")
    print(f"Wallet1 balance: {wallet1.get_balance()} FC")
    
    fc.transfer(wallet1.wallet_id, wallet2.wallet_id, 500, "Donación comunidad")
    print(f"Wallet1: {wallet1.get_balance()} FC")
    print(f"Wallet2: {wallet2.get_balance()} FC")
    print(f"Total supply: {fc.get_total_supply()} FC")
    print(f"En USD: ${fc.convert_to_usd(fc.get_total_supply())}")
