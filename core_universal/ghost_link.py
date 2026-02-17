#!/usr/bin/env python3
"""
================================================================================
                         🚀 NEURAFORGEAI® 🚀
              Desarrollado con orgullo por el equipo
================================================================================

GHOST LINK - Detector de necesidades para NeuraForgeAI
Ejecuta en segundo plano, analiza el entorno y sugiere mejoras/módulos

Desarrollado por: Miguel Chávez & AMI (IA Colaborativa)
Filosofía: "No importa qué vendes, importa cómo lo haces mejor"
================================================================================
"""

import os
import json
import time
import logging
import psutil
import platform
import socket
import subprocess
from datetime import datetime
from pathlib import Path

class GhostLink:
    """
    Módulo de detección de necesidades. Corre como demonio.
    Analiza el entorno local y sugiere módulos premium o mejoras.
    """
    
    def __init__(self, config_path="~/.neuraforge/ghost_config.json"):
        self.config_path = os.path.expanduser(config_path)
        self.logger = self._setup_logging()
        self.detecciones = []
        self.sugerencias_activas = []
        self.cargar_config()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - GhostLink - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/data/data/com.termux/files/home/ghost_link.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def cargar_config(self):
        """Carga configuración o crea por defecto"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "intervalo_escaneo": 3600,
                "modulos_detectados": [],
                "ultimo_escaneo": None,
                "privacidad_maxima": True,
                "sugerencias_automaticas": True,
                "notificaciones_activas": True
            }
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            self.guardar_config()
    
    def guardar_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def escanear_entorno(self):
        """Escanea el entorno en busca de necesidades"""
        self.logger.info("Iniciando escaneo de entorno...")
        
        detecciones = []
        
        # Detectar tipo de dispositivo
        sistema = platform.system()
        if sistema == "Linux" and "android" in platform.version().lower():
            detecciones.append({
                "tipo": "dispositivo",
                "valor": "android",
                "sugerencia": "bot_movil",
                "confianza": 0.9,
                "timestamp": datetime.now().isoformat()
            })
        
        # Detectar recursos del sistema
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memoria = psutil.virtual_memory()
            
            if memoria.percent > 80:
                detecciones.append({
                    "tipo": "rendimiento",
                    "valor": "memoria_alta",
                    "sugerencia": "modulo_optimizacion",
                    "confianza": 0.85,
                    "timestamp": datetime.now().isoformat()
                })
            
            if cpu_percent > 70:
                detecciones.append({
                    "tipo": "rendimiento",
                    "valor": "cpu_alto",
                    "sugerencia": "modulo_escalado",
                    "confianza": 0.75,
                    "timestamp": datetime.now().isoformat()
                })
        except:
            pass
        
        # Detectar procesos relacionados con negocios
        try:
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    nombre = proc.info['name'].lower() if proc.info['name'] else ""
                    if any(term in nombre for term in ['taxi', 'uber', 'didi', 'cabify']):
                        detecciones.append({
                            "tipo": "negocio",
                            "valor": "transporte",
                            "sugerencia": "bot_taxi",
                            "confianza": 0.75,
                            "timestamp": datetime.now().isoformat()
                        })
                    elif any(term in nombre for term in ['pizza', 'delivery', 'pedidos', 'rapp']):
                        detecciones.append({
                            "tipo": "negocio",
                            "valor": "restaurante",
                            "sugerencia": "bot_pizza",
                            "confianza": 0.75,
                            "timestamp": datetime.now().isoformat()
                        })
                    elif any(term in nombre for term in ['ferreteria', 'construccion', 'materiales']):
                        detecciones.append({
                            "tipo": "negocio",
                            "valor": "ferreteria",
                            "sugerencia": "bot_ferretero",
                            "confianza": 0.75,
                            "timestamp": datetime.now().isoformat()
                        })
                except:
                    continue
        except:
            pass
        
        # Detectar red local
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Escanear puertos comunes
            puertos_comunes = [80, 443, 3000, 5000, 8000, 8080]
            puertos_abiertos = []
            
            for puerto in puertos_comunes:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((local_ip, puerto))
                if result == 0:
                    puertos_abiertos.append(puerto)
                sock.close()
            
            if puertos_abiertos:
                detecciones.append({
                    "tipo": "red",
                    "valor": "servidor_local",
                    "sugerencia": "modulo_web",
                    "confianza": 0.8,
                    "metadata": {"puertos": puertos_abiertos},
                    "timestamp": datetime.now().isoformat()
                })
        except:
            pass
        
        self.detecciones = detecciones
        self.config["ultimo_escaneo"] = time.time()
        self.config["modulos_detectados"] = detecciones
        self.guardar_config()
        
        self.logger.info(f"Escaneo completado. {len(detecciones)} detecciones.")
        return detecciones
    
    def sugerir_modulos(self):
        """Genera sugerencias basadas en detecciones"""
        if not self.detecciones:
            self.escanear_entorno()
        
        sugerencias = []
        for d in self.detecciones:
            if d["confianza"] > 0.7:
                sugerencias.append({
                    "modulo": d["sugerencia"],
                    "razon": f"Detectado: {d['tipo']} - {d['valor']}",
                    "urgencia": "alta" if d["confianza"] > 0.8 else "media",
                    "premium": d["sugerencia"].startswith("modulo_"),
                    "timestamp": d.get("timestamp", datetime.now().isoformat())
                })
        
        self.sugerencias_activas = sugerencias
        return sugerencias
    
    def run_daemon(self):
        """Ejecuta como demonio"""
        print("""
╔════════════════════════════════════════════════════════════╗
║              👻 GHOST LINK ACTIVADO 👻                    ║
║         Detectando necesidades en segundo plano            ║
╚════════════════════════════════════════════════════════════╝
        """)
        self.logger.info("Ghost Link iniciado como demonio")
        
        while True:
            try:
                self.escanear_entorno()
                sugerencias = self.sugerir_modulos()
                
                if sugerencias and self.config["sugerencias_automaticas"]:
                    self.logger.info(f"Sugerencias generadas: {len(sugerencias)}")
                    for s in sugerencias:
                        self.logger.info(f"  • {s['modulo']} - {s['razon']}")
                
                time.sleep(self.config["intervalo_escaneo"])
            except Exception as e:
                self.logger.error(f"Error en escaneo: {e}")
                time.sleep(300)

if __name__ == "__main__":
    ghost = GhostLink()
    ghost.run_daemon()
