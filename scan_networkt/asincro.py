import asyncio
from supabase import create_client

class StationSystem:
    def __init__(self, sb_url, sb_key):
        self.supabase = create_client(sb_url, sb_key)
        self.radar = WiFiRadarModule()
        self.ui = VisualRadar()

    async def run_sync(self):
        while True:
            # 1. Leer Brújula (Simulado o via sensor I2C/Android)
            current_heading = 45.0 # Ejemplo: Noreste
            
            # 2. Escaneo de red
            scapy.sniff(iface=self.radar.interface, 
                        prn=lambda x: self.radar.packet_callback(x, current_heading), 
                        timeout=5)
            
            # 3. Preparar datos para el mapa
            entities = []
            for mac, data in self.radar.devices.items():
                entities.append((data['distance'], data['angle'], 'person'))
                
                # 4. Registro en Supabase
                self.supabase.table("radar_logs").insert({
                    "mac": mac,
                    "distance": data['distance'],
                    "angle": data['angle']
                }).execute()

            # 5. Actualizar Visualización
            self.ui.update_map(current_heading, entities)
            
            # 6. Alerta Telegram si hay alguien a menos de 2 metros
            for dist, _, _ in entities:
                if dist < 2.0:
                    self.send_telegram_alert("¡Persona detectada cerca!")
            
            await asyncio.sleep(1)
