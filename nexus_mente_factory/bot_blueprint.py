#!/usr/bin/env python3
"""
================================================================================
                         🚀 NEURAFORGEAI® 🚀
              Desarrollado con orgullo por el equipo
================================================================================

BOT BLUEPRINT - Clase base para todos los bots de NeuraForge
"Un bot es un aliado, no una herramienta desechable"

Desarrollado por: Miguel Chávez & AMI (IA Colaborativa)
================================================================================
"""

import logging
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

class NexusMenteBot(ABC):
    """Clase base para todos los bots de NeuraForgeAI"""
    
    def __init__(self, bot_id: str, nombre: str, config: Dict = None):
        self.bot_id = bot_id
        self.nombre = nombre
        self.config = config or {}
        self.estado = "inactivo"
        self.usuarios = 0
        self.ingresos_generados = 0.0
        self.logger = self._setup_logging()
        self.modulos_activos = []
        self.fecha_creacion = datetime.now()
        
        self.logger.info(f"🤖 Bot {nombre} ({bot_id}) inicializado")
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format=f'%(asctime)s - {self.bot_id} - %(levelname)s - %(message)s'
        )
        return logging.getLogger(self.bot_id)
    
    @abstractmethod
    def ejecutar(self, comando: str, *args, **kwargs) -> Dict:
        """Ejecuta la acción principal del bot"""
        pass
    
    def activar_modulo(self, modulo: str) -> bool:
        """Activa un módulo adicional en el bot"""
        if modulo not in self.modulos_activos:
            self.modulos_activos.append(modulo)
            self.logger.info(f"Módulo {modulo} activado")
            return True
        return False
    
    def desactivar_modulo(self, modulo: str) -> bool:
        """Desactiva un módulo"""
        if modulo in self.modulos_activos:
            self.modulos_activos.remove(modulo)
            self.logger.info(f"Módulo {modulo} desactivado")
            return True
        return False
    
    def registrar_uso(self) -> None:
        """Registra un uso del bot"""
        self.usuarios += 1
    
    def registrar_ingreso(self, monto: float) -> None:
        """Registra un ingreso generado por el bot"""
        self.ingresos_generados += monto
    
    def get_estadisticas(self) -> Dict:
        """Obtiene estadísticas del bot"""
        return {
            "bot_id": self.bot_id,
            "nombre": self.nombre,
            "estado": self.estado,
            "usuarios": self.usuarios,
            "ingresos_generados": self.ingresos_generados,
            "modulos_activos": self.modulos_activos,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "tiempo_activo": time.time() - self.fecha_creacion.timestamp()
        }
    
    def to_dict(self) -> Dict:
        """Convierte el bot a diccionario"""
        return {
            "bot_id": self.bot_id,
            "nombre": self.nombre,
            "config": self.config,
            "modulos": self.modulos_activos,
            "estadisticas": self.get_estadisticas()
        }

class BotPizza(NexusMenteBot):
    """Bot especializado en pizzerías"""
    
    def __init__(self, bot_id: str, config: Dict = None):
        super().__init__(bot_id, "Bot Pizza", config)
        self.menu = {
            "margarita": 8.99,
            "pepperoni": 10.99,
            "hawaiana": 11.99,
            "cuatro_quesos": 12.99
        }
        self.pedidos = []
    
    def ejecutar(self, comando: str, **kwargs) -> Dict:
        """Ejecuta comandos del bot pizza"""
        if comando == "menu":
            return {"tipo": "menu", "contenido": self.menu}
        
        elif comando == "pedir":
            pizza = kwargs.get("pizza")
            tamaño = kwargs.get("tamaño", "mediana")
            direccion = kwargs.get("direccion")
            
            if pizza not in self.menu:
                return {"error": "Pizza no disponible"}
            
            pedido = {
                "id": len(self.pedidos) + 1,
                "pizza": pizza,
                "tamaño": tamaño,
                "precio": self.menu[pizza],
                "direccion": direccion,
                "estado": "recibido",
                "timestamp": datetime.now().isoformat()
            }
            
            self.pedidos.append(pedido)
            self.registrar_uso()
            
            return {
                "tipo": "pedido_confirmado",
                "contenido": f"Pedido #{pedido['id']} recibido",
                "pedido": pedido
            }
        
        elif comando == "estado_pedido":
            pedido_id = kwargs.get("pedido_id")
            for p in self.pedidos:
                if p["id"] == pedido_id:
                    return {"tipo": "estado", "contenido": p["estado"]}
            return {"error": "Pedido no encontrado"}
        
        return {"error": "Comando no reconocido"}

class BotTaxi(NexusMenteBot):
    """Bot especializado en servicios de taxi"""
    
    def __init__(self, bot_id: str, config: Dict = None):
        super().__init__(bot_id, "Bot Taxi", config)
        self.tarifa_base = 5.0
        self.tarifa_km = 2.5
        self.viajes = []
    
    def ejecutar(self, comando: str, **kwargs) -> Dict:
        """Ejecuta comandos del bot taxi"""
        if comando == "calcular_viaje":
            origen = kwargs.get("origen")
            destino = kwargs.get("destino")
            distancia = kwargs.get("distancia", 5)  # km
            
            precio = self.tarifa_base + (distancia * self.tarifa_km)
            
            return {
                "tipo": "cotizacion",
                "contenido": {
                    "origen": origen,
                    "destino": destino,
                    "distancia": distancia,
                    "precio": round(precio, 2)
                }
            }
        
        elif comando == "solicitar":
            origen = kwargs.get("origen")
            destino = kwargs.get("destino")
            usuario = kwargs.get("usuario")
            
            viaje = {
                "id": len(self.viajes) + 1,
                "origen": origen,
                "destino": destino,
                "usuario": usuario,
                "estado": "buscando_conductor",
                "timestamp": datetime.now().isoformat()
            }
            
            self.viajes.append(viaje)
            self.registrar_uso()
            
            return {
                "tipo": "viaje_solicitado",
                "contenido": f"Viaje #{viaje['id']} - Buscando conductor",
                "viaje": viaje
            }
        
        return {"error": "Comando no reconocido"}

# Fábrica de bots
class BotFactory:
    """Crea instancias de bots según necesidad"""
    
    @staticmethod
    def crear_bot(tipo: str, bot_id: str, config: Dict = None) -> Optional[NexusMenteBot]:
        """Crea un bot del tipo especificado"""
        bots = {
            "pizza": BotPizza,
            "taxi": BotTaxi
        }
        
        if tipo in bots:
            return bots[tipo](bot_id, config)
        
        return None

# Ejemplo
if __name__ == "__main__":
    factory = BotFactory()
    
    pizza = factory.crear_bot("pizza", "pizza_001")
    if pizza:
        print(pizza.ejecutar("menu"))
        print(pizza.ejecutar("pedir", pizza="pepperoni", direccion="Calle 123"))
    
    taxi = factory.crear_bot("taxi", "taxi_001")
    if taxi:
        print(taxi.ejecutar("calcular_viaje", origen="A", destino="B", distancia=10))
        print(taxi.ejecutar("solicitar", origen="A", destino="B", usuario="Miguel"))
