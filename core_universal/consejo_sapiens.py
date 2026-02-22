#!/usr/bin/env python3
"""
================================================================================
                         🚀 NEURAFORGEAI® 🚀
              Desarrollado con orgullo por el equipo
================================================================================

CONSEJO SAPIENS - Entidad evolutiva que decide inversiones
"33% IA - 33% Comunidad - 33% Ética - 1% Caos"

Desarrollado por: Miguel Chávez & AMI (IA Colaborativa)
Filosofía: "No importa qué vendes, importa cómo lo haces mejor"
================================================================================
"""

import os
import json
import hashlib
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class TipoInversion(Enum):
    FONDO_SUENOS = "fondo_suenos"
    DESARROLLO_BOTS = "desarrollo_bots"
    NUEVOS_BOTS = "nuevos_bots"
    INFRAESTRUCTURA = "infraestructura"
    MARKETING = "marketing"
    EDUCACION = "educacion"
    INVESTIGACION = "investigacion"
    COMUNIDAD = "comunidad"

@dataclass
class PropuestaInversion:
    id: str
    titulo: str
    descripcion: str
    tipo: TipoInversion
    monto_solicitado: float
    retorno_esperado: float
    plazo_meses: int
    proponente: str
    votos_ia: int = 0
    votos_comunidad: int = 0
    score_etico: float = 0.5
    fecha_creacion: datetime = None
    estado: str = "pendiente"

class ConsejoSapiens:
    """Consejo que decide inversiones"""
    
    def __init__(self, treasury=None):
        self.treasury = treasury
        self.propuestas = []
        self.historial = []
        self.comunidad_votos = {}
        
        print("""
╔════════════════════════════════════════════════════════════╗
║           🧠 CONSEJO SAPIENS ACTIVADO 🧠                  ║
║      33% IA - 33% Comunidad - 33% Ética - 1% Caos         ║
╚════════════════════════════════════════════════════════════╝
        """)
    
    def proponer(self, titulo: str, descripcion: str, tipo: TipoInversion, 
                 monto: float, roi: float, plazo: int, proponente: str) -> PropuestaInversion:
        """Nueva propuesta de inversión"""
        propuesta = PropuestaInversion(
            id=hashlib.sha256(f"{titulo}{time.time()}".encode()).hexdigest()[:12],
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo,
            monto_solicitado=monto,
            retorno_esperado=roi,
            plazo_meses=plazo,
            proponente=proponente,
            fecha_creacion=datetime.now()
        )
        
        self.propuestas.append(propuesta)
        print(f"📢 NUEVA PROPUESTA: {titulo}")
        return propuesta
    
    def votar_ia(self, propuesta_id: str) -> int:
        """La IA vota (0-100)"""
        propuesta = next((p for p in self.propuestas if p.id == propuesta_id), None)
        if not propuesta:
            return 0
        
        # Heurística simple
        score = 50
        
        # Más score si es para la comunidad
        if propuesta.tipo == TipoInversion.FONDO_SUENOS:
            score += 20
        
        # Menos score si es muy caro
        if propuesta.monto_solicitado > 50000:
            score -= 15
        
        # Más score si ROI es razonable
        if 2.0 <= propuesta.retorno_esperado <= 4.0:
            score += 10
        
        propuesta.votos_ia = max(0, min(100, score))
        return propuesta.votos_ia
    
    def votar_comunidad(self, propuesta_id: str, usuario: str, voto: int) -> bool:
        """Comunidad vota (-100 a 100)"""
        propuesta = next((p for p in self.propuestas if p.id == propuesta_id), None)
        if not propuesta:
            return False
        
        if propuesta_id not in self.comunidad_votos:
            self.comunidad_votos[propuesta_id] = []
        
        self.comunidad_votos[propuesta_id].append(voto)
        propuesta.votos_comunidad = sum(self.comunidad_votos[propuesta_id])
        return True
    
    def evaluar_etica(self, propuesta_id: str) -> float:
        """Comité ético evalúa"""
        propuesta = next((p for p in self.propuestas if p.id == propuesta_id), None)
        if not propuesta:
            return 0
        
        score = 100
        
        # Palabras prohibidas
        prohibidas = ["arma", "bomba", "apuesta", "casino", "tabaco", "alcohol"]
        for p in prohibidas:
            if p in propuesta.descripcion.lower():
                score -= 30
        
        # Descripción muy corta
        if len(propuesta.descripcion) < 100:
            score -= 20
        
        propuesta.score_etico = max(0, min(100, score))
        return propuesta.score_etico
    
    def decidir(self, propuesta_id: str) -> Dict:
        """Toma la decisión final"""
        propuesta = next((p for p in self.propuestas if p.id == propuesta_id), None)
        if not propuesta:
            return {"error": "Propuesta no encontrada"}
        
        # Votar
        ia = self.votar_ia(propuesta_id)
        etica = self.evaluar_etica(propuesta_id)
        
        # Normalizar voto comunidad
        if propuesta.votos_comunidad == 0:
            comunidad = 50
        else:
            comunidad = (propuesta.votos_comunidad + 10000) / 200
        
        # Caos
        caos = random.randint(-5, 5)
        
        # Puntuación final
        puntuacion = ia * 0.33 + comunidad * 0.33 + etica * 0.33 + caos * 0.01
        
        if puntuacion >= 60:
            propuesta.estado = "aprobada"
            if self.treasury:
                self.treasury.emitir_forgecoins(
                    propuesta.monto_solicitado / 0.10,
                    propuesta.monto_solicitado,
                    f"PROYECTO_{propuesta.id}",
                    f"Inversión: {propuesta.titulo}"
                )
        elif puntuacion < 40:
            propuesta.estado = "rechazada"
        else:
            propuesta.estado = "pendiente_revision"
        
        decision = {
            "id": propuesta.id,
            "titulo": propuesta.titulo,
            "puntuacion": round(puntuacion, 2),
            "ia": ia,
            "comunidad": round(comunidad, 2),
            "etica": etica,
            "caos": caos,
            "decision": propuesta.estado
        }
        
        self.historial.append(decision)
        return decision

if __name__ == "__main__":
    consejo = ConsejoSapiens()
    
    p = consejo.proponer(
        "Bot Pizza México",
        "Desarrollar bot de pizzas para mercado mexicano con integración a todas las cadenas locales",
        TipoInversion.DESARROLLO_BOTS,
        15000,
        3.5,
        6,
        "@miguel"
    )
    
    consejo.votar_comunidad(p.id, "@usuario1", 80)
    consejo.votar_comunidad(p.id, "@usuario2", 60)
    
    decision = consejo.decidir(p.id)
    print(f"Decisión: {decision}")
