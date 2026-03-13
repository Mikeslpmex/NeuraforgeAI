import scapy.all as scapy
import subprocess
import re
import numpy as np

class WiFiRadarModule:
    def __init__(self, interface="wlan0"):
        self.interface = interface
        self.devices = {} # MAC: {"rssi": -db, "angle": degrees}

    def set_monitor_mode(self):
        """Configura la antena en modo monitor para 'escuchar' el entorno"""
        subprocess.run(["ip", "link", "set", self.interface, "down"])
        subprocess.run(["iw", self.interface, "set", "type", "monitor"])
        subprocess.run(["ip", "link", "set", self.interface, "up"])

    def get_router_diagnostics(self):
        """Obtiene datos de la conexión actual al router principal"""
        cmd = ["iw", "dev", self.interface, "link"]
        result = subprocess.check_output(cmd).decode()
        signal = re.search(r"signal: (-\d+)", result)
        return int(signal.group(1)) if signal else 0

    def packet_callback(self, pkt, current_compass_heading):
        """Procesa paquetes para triangular dispositivos"""
        if pkt.haslayer(scapy.Dot11):
            if pkt.addr2 and pkt.addr2 not in self.devices:
                # Extraer intensidad de señal (RSSI)
                rssi = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else -100
                
                # Guardamos la ubicación relativa basada en la brújula en ese instante
                self.devices[pkt.addr2] = {
                    "distance": self.calculate_distance(rssi),
                    "angle": current_compass_heading,
                    "last_seen": pkt.time
                }

    def calculate_distance(self, rssi, n=2.0):
        """Fórmula de pérdida de trayecto en el espacio libre"""
        # d = 10 ^ ((MeasuredPower - RSSI) / (10 * n))
        measured_power = -30 # Señal a 1 metro de distancia
        return 10 ** ((measured_power - rssi) / (10 * n))
