#!/usr/bin/env python3
"""
Script de verificación para NeuraForgeAI
Detecta componentes existentes y faltantes según la arquitectura definida
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

class NeuraForgeVerifier:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.estructura_requerida = {
            "core_universal": {
                "archivos": [
                    "ghost_link.py",
                    "orion_broker.py",
                    "security_manager.py"
                ],
                "descripcion": "Módulos base del sistema"
            },
            "nexus_mente_factory": {
                "archivos": [
                    "factory_bot.py",
                    "bot_blueprint.py",
                    "suite_gratuita/bot_taxi.py",
                    "suite_gratuita/bot_pizza.py",
                    "suite_gratuita/bot_ferretero.py",
                    "suite_gratuita/bot_cerrajero.py",
                    "suite_gratuita/bot_administrativo.py",
                    "suite_gratuita/bot_sat.py",
                    "suite_pyme/__init__.py",
                    "suite_empresarial/__init__.py",
                    "modulos_mejora/modulo_multimedia.py",
                    "modulos_mejora/modulo_conocimiento_global.py"
                ],
                "descripcion": "Fábrica de bots y suites"
            },
            "economia_inteligente": {
                "archivos": [
                    "costos_ai.py",
                    "moneda_interna/forge_coin.py",
                    "moneda_interna/wallet_manager.py",
                    "financiamiento/evaluador_ideas.py",
                    "financiamiento/fondo_suenos.py"
                ],
                "descripcion": "Sistema económico y precios justos"
            },
            "afiliados_estrategicos": {
                "archivos": [
                    "affiliate_bot.py",
                    "referencias/referral_manager.py",
                    "promocion_bots/bot_promoter.py",
                    "cloud_afiliados/google_cloud.py",
                    "cloud_afiliados/aws.py",
                    "cloud_afiliados/oracle_cloud.py",
                    "cloud_afiliados/alibaba_cloud.py"
                ],
                "descripcion": "Sistema de afiliados"
            },
            "integraciones": {
                "archivos": [
                    "multimedia/spotify_connector.py",
                    "multimedia/deezer_connector.py",
                    "multimedia/amazon_music_connector.py",
                    "multimedia/apple_music_connector.py",
                    "asistentes_voz/google_home_handler.py"
                ],
                "descripcion": "Integraciones con servicios externos"
            },
            "premium_modules": {
                "archivos": [
                    "knowledge_exchange/knowledge_base.py",
                    "fiscal/sat_guardian.py",
                    "logistics/__init__.py",
                    "finance/__init__.py",
                    "legal/__init__.py"
                ],
                "descripcion": "Módulos premium"
            },
            "seguridad_privacidad": {
                "archivos": [
                    "oauth_guardian.py",
                    "datos_locales/encryptor.py",
                    "antivirus_predictivo/core.py",
                    "antivirus_predictivo/acoustic_odometry.py"
                ],
                "descripcion": "Seguridad y privacidad"
            },
            "tesorero": {
                "archivos": [
                    "quantum_treasury.py",
                    "distribucion_ganancias.py"
                ],
                "descripcion": "Sistema financiero"
            },
            "config": {
                "archivos": [
                    "system_config.yaml",
                    "costos_regiones.json",
                    "knowledge_pricing.json",
                    "firebase_config.json"
                ],
                "descripcion": "Configuración global"
            },
            "mobile_app": {
                "archivos": [
                    "NAIbots/app/src/main/AndroidManifest.xml",
                    "NAIbots/app/build.gradle"
                ],
                "descripcion": "App Android NAIbots"
            },
            "google_cloud": {
                "archivos": [
                    "firebase_functions/main.py",
                    "dialogflow/agent.json",
                    "cloud_run/Dockerfile"
                ],
                "descripcion": "Integración con Google Cloud"
            }
        }
        
        self.resultados = {
            "existente": [],
            "faltante": [],
            "parcial": []
        }
        
    def verificar(self):
        """Ejecuta verificación completa"""
        print("\n" + "="*60)
        print("🔍 VERIFICADOR DE ESTRUCTURA NEURAFORGEAI")
        print("="*60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Ruta base: {self.base_path.absolute()}")
        print("="*60 + "\n")
        
        # Verificar cada módulo
        for modulo, contenido in self.estructura_requerida.items():
            self._verificar_modulo(modulo, contenido)
        
        # Mostrar resumen
        self._mostrar_resumen()
        
        # Generar reporte
        self._generar_reporte()
        
    def _verificar_modulo(self, modulo, contenido):
        """Verifica un módulo específico"""
        print(f"\n📁 {modulo.upper()} - {contenido['descripcion']}")
        print("-" * 40)
        
        modulo_path = self.base_path / modulo
        archivos_modulo = []
        
        for archivo in contenido["archivos"]:
            archivo_path = modulo_path / archivo
            existe = archivo_path.exists()
            
            status = "✅" if existe else "❌"
            print(f"{status} {archivo}")
            
            if existe:
                self.resultados["existente"].append(f"{modulo}/{archivo}")
            else:
                self.resultados["faltante"].append(f"{modulo}/{archivo}")
                
            archivos_modulo.append({
                "nombre": archivo,
                "existe": existe,
                "ruta": str(archivo_path)
            })
        
        # Verificar si el módulo existe parcialmente
        if os.path.exists(modulo_path):
            self.resultados["parcial"].append({
                "modulo": modulo,
                "archivos": archivos_modulo
            })
    
    def _mostrar_resumen(self):
        """Muestra resumen de la verificación"""
        print("\n" + "="*60)
        print("📊 RESUMEN FINAL")
        print("="*60)
        
        total_requeridos = sum(len(m["archivos"]) for m in self.estructura_requerida.values())
        total_existentes = len(self.resultados["existente"])
        porcentaje = (total_existentes / total_requeridos) * 100 if total_requeridos > 0 else 0
        
        print(f"\n📦 Total archivos requeridos: {total_requeridos}")
        print(f"✅ Archivos existentes: {total_existentes}")
        print(f"❌ Archivos faltantes: {len(self.resultados['faltante'])}")
        print(f"📊 Progreso: {porcentaje:.1f}%")
        
        if self.resultados["faltante"]:
            print("\n🔴 PRIORIDADES ALTAS (Archivos críticos faltantes):")
            criticos = [f for f in self.resultados["faltante"] 
                       if any(c in f for c in ["ghost_link", "factory_bot", "quantum_treasury", "forge_coin"])]
            for f in criticos[:5]:  # Mostrar top 5
                print(f"   • {f}")
    
    def _generar_reporte(self):
        """Genera archivo JSON con resultados"""
        reporte = {
            "fecha": datetime.now().isoformat(),
            "estructura_verificada": self.resultados,
            "estadisticas": {
                "total_requeridos": sum(len(m["archivos"]) for m in self.estructura_requerida.values()),
                "total_existentes": len(self.resultados["existente"]),
                "total_faltantes": len(self.resultados["faltante"])
            }
        }
        
        with open("verificacion_neuraforge.json", "w") as f:
            json.dump(reporte, f, indent=2)
        print(f"\n📝 Reporte guardado en: verificacion_neuraforge.json")

if __name__ == "__main__":
    verifier = NeuraForgeVerifier()
    verifier.verificar()
