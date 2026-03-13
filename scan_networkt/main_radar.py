import scapy.all as scapy
import numpy as np
import subprocess
import json
import requests
import asyncio
from supabase import create_client

# === CONFIGURACIÓN ===
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-api-key"
TELEGRAM_TOKEN = "tu-bot-token"
CHAT_ID = "tu-chat-id"

# Coordenadas conocidas de tus routers (x, y) en metros
ROUTER_MAP = {
    "AA:BB:CC:11:22:33": (0, 0),   # Router Principal
    "DD:EE:FF:44:55:66": (10, 0),  # Router Sala
    "11:22:33:44:55:66": (5, 8)    # Router Extensor
}

class OSINStation:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.active_scans = {}

    def get_compass_heading(self):
        """Lee la brújula de Android vía Termux:API"""
        try:
            res = subprocess.check_output(["termux-sensor", "-s", "orientation", "-n", "1"], timeout=2)
            data = json.loads(res)
            return data['orientation']['values'][0] # Azimuth
        except:
            return 0.0 # Fallback si no hay sensor

    def calculate_distance(self, rssi):
        """Convierte potencia de señal a metros aproximados"""
        # n = factor de entorno (2.0 espacio abierto, 3.0 paredes)
        return 10 ** ((-30 - rssi) / (10 * 2.5))

    def trilaterate_position(self, distances_to_routers):
        """Algoritmo de Triangulación"""
        # Simplificado para producción: Retorna (x, y) aproximado
        p = []
        d = []
        for mac, dist in distances_to_routers.items():
            if mac in ROUTER_MAP:
                p.append(ROUTER_MAP[mac])
                d.append(dist)
        
        if len(p) < 3: return (0,0) # Necesitamos al menos 3 puntos

        # Resolución geométrica
        x1, y1 = p[0]; x2, y2 = p[1]; x3, y3 = p[2]
        d1, d2, d3 = d[0], d[1], d[2]
        
        A = 2*x2 - 2*x1
        B = 2*y2 - 2*y1
        C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
        D = 2*x3 - 2*x2
        E = 2*y3 - 2*y2
        F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2
        
        x = (C*E - F*B) / (A*E - D*B)
        y = (A*F - D*C) / (A*E - D*B)
        return x, y

    def process_packet(self, pkt):
        """Callback de Scapy para cada paquete detectado"""
        if pkt.haslayer(scapy.Dot11):
            mac = pkt.addr2
            rssi = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else -100
            dist = self.calculate_distance(rssi)
            
            if mac:
                self.active_scans[mac] = dist

    async def run_radar(self):
        print("📡 Estación OSIN Iniciada...")
        while True:
            # 1. Escaneo de 5 segundos
            scapy.sniff(iface="wlan0", prn=self.process_packet, timeout=5, store=0)
            
            # 2. Obtener orientación y posición propia
            heading = self.get_compass_heading()
            my_x, my_y = self.trilaterate_position(self.active_scans)
            
            # 3. Registrar en Supabase
            data = {
                "entities_count": len(self.active_scans),
                "my_pos_x": float(my_x),
                "my_pos_y": float(my_y),
                "heading": float(heading)
            }
            self.supabase.table("radar_live").insert(data).execute()
            
            # 4. Alerta crítica (ejemplo: objeto a menos de 1m)
            for mac, d in self.active_scans.items():
                if d < 1.0 and mac not in ROUTER_MAP:
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": f"⚠️ Intruso a {d:.2f}m!"})
            
            self.active_scans.clear()
            await asyncio.sleep(1)

if __name__ == "__main__":
    station = OSINStation()
    asyncio.run(station.run_radar())
