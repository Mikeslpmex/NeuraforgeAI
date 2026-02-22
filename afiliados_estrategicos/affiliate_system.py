#!/usr/bin/env python3
"""
================================================================================
                         🚀 NEURAFORGEAI® 🚀
              Desarrollado con orgullo por el equipo
================================================================================

SISTEMA DE AFILIADOS PREDICTIVO
Maximiza ingresos por afiliación con IA

Desarrollado por: Miguel Chávez & AMI (IA Colaborativa)
================================================================================
"""

import random
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional

class ServicioCloud:
    """Servicios cloud disponibles para afiliación"""
    
    SERVICIOS = {
        "GOOGLE_CLOUD": {
            "nombre": "Google Cloud",
            "comision": 0.15,
            "url_base": "https://cloud.google.com/?affiliate=neuraforge",
            "categoria": "infraestructura"
        },
        "AWS": {
            "nombre": "Amazon Web Services",
            "comision": 0.10,
            "url_base": "https://aws.amazon.com/?affiliate=neuraforge",
            "categoria": "infraestructura"
        },
        "ORACLE_CLOUD": {
            "nombre": "Oracle Cloud",
            "comision": 0.20,
            "url_base": "https://www.oracle.com/cloud/?affiliate=neuraforge",
            "categoria": "infraestructura"
        },
        "DIGITAL_OCEAN": {
            "nombre": "Digital Ocean",
            "comision": 0.25,
            "url_base": "https://www.digitalocean.com/?affiliate=neuraforge",
            "categoria": "vps"
        },
        "VERCEL": {
            "nombre": "Vercel",
            "comision": 0.20,
            "url_base": "https://vercel.com/?affiliate=neuraforge",
            "categoria": "hosting"
        }
    }

class AffiliatePredictor:
    """Sistema predictivo de afiliados"""
    
    def __init__(self):
        self.clicks = []
        self.conversiones = []
        self.servicios = ServicioCloud.SERVICIOS
        
        print("""
╔════════════════════════════════════════════════════════════╗
║        📈 SISTEMA DE AFILIADOS PREDICTIVO ACTIVO         ║
║        Maximizando ingresos con IA en tiempo real         ║
╚════════════════════════════════════════════════════════════╝
        """)
    
    def recomendar(self, contexto: Dict) -> List[Dict]:
        """Recomienda servicios según contexto"""
        recomendaciones = []
        
        for codigo, servicio in self.servicios.items():
            # Probabilidad base
            prob = random.uniform(0.3, 0.8)
            
            # Ajustar por contexto
            if contexto.get('categoria') == servicio['categoria']:
                prob *= 1.2
            
            if prob > 0.5:
                url = self._generar_url(codigo, contexto)
                recomendaciones.append({
                    "servicio": servicio['nombre'],
                    "codigo": codigo,
                    "confianza": round(prob * 100, 1),
                    "comision": f"{servicio['comision']*100:.0f}%",
                    "url": url,
                    "categoria": servicio['categoria']
                })
        
        # Ordenar por confianza
        recomendaciones.sort(key=lambda x: x['confianza'], reverse=True)
        return recomendaciones[:3]
    
    def _generar_url(self, servicio: str, contexto: Dict) -> str:
        """Genera URL con tracking"""
        base = self.servicios[servicio]['url_base']
        ref = hashlib.md5(f"{contexto.get('usuario', 'anon')}_{time.time()}".encode()).hexdigest()[:8]
        
        if '?' in base:
            return f"{base}&ref={ref}&utm_source=neuraforge"
        return f"{base}?ref={ref}&utm_source=neuraforge"
    
    def registrar_click(self, servicio: str, usuario: str, contexto: Dict) -> str:
        """Registra un click para tracking"""
        click_id = hashlib.md5(f"{servicio}_{usuario}_{time.time()}".encode()).hexdigest()[:12]
        
        self.clicks.append({
            "id": click_id,
            "servicio": servicio,
            "usuario": usuario,
            "contexto": contexto,
            "timestamp": datetime.now().isoformat(),
            "convertido": False
        })
        
        return click_id
    
    def registrar_conversion(self, click_id: str, valor: float) -> bool:
        """Registra una conversión"""
        for click in self.clicks:
            if click['id'] == click_id and not click['convertido']:
                click['convertido'] = True
                click['valor'] = valor
                click['fecha_conversion'] = datetime.now().isoformat()
                
                comision = valor * self.servicios[click['servicio']]['comision']
                self.conversiones.append({
                    "click_id": click_id,
                    "valor": valor,
                    "comision": comision
                })
                
                return True
        return False
    
    def get_estadisticas(self) -> Dict:
        """Obtiene estadísticas de rendimiento"""
        total_clicks = len(self.clicks)
        total_conversiones = len(self.conversiones)
        
        return {
            "total_clicks": total_clicks,
            "total_conversiones": total_conversiones,
            "tasa_conversion": (total_conversiones / total_clicks * 100) if total_clicks > 0 else 0,
            "comisiones_generadas": sum(c['comision'] for c in self.conversiones),
            "valor_total": sum(c['valor'] for c in self.conversiones),
            "top_servicios": self._get_top_servicios()
        }
    
    def _get_top_servicios(self) -> List[Dict]:
        """Obtiene servicios con mejor rendimiento"""
        rendimiento = {}
        for conv in self.conversiones:
            click = next((c for c in self.clicks if c['id'] == conv['click_id']), None)
            if click:
                servicio = click['servicio']
                if servicio not in rendimiento:
                    rendimiento[servicio] = {"conversiones": 0, "comisiones": 0}
                rendimiento[servicio]["conversiones"] += 1
                rendimiento[servicio]["comisiones"] += conv['comision']
        
        return sorted(
            [{"servicio": s, **v} for s, v in rendimiento.items()],
            key=lambda x: x['comisiones'],
            reverse=True
        )[:3]

# Ejemplo de uso
if __name__ == "__main__":
    aff = AffiliatePredictor()
    
    contexto = {
        "usuario": "test_user",
        "categoria": "infraestructura",
        "pais": "MX"
    }
    
    recs = aff.recomendar(contexto)
    print(f"Recomendaciones: {recs}")
    
    click_id = aff.registrar_click("GOOGLE_CLOUD", "test_user", contexto)
    print(f"Click registrado: {click_id}")
    
    aff.registrar_conversion(click_id, 100)
    print(f"Estadísticas: {aff.get_estadisticas()}")
