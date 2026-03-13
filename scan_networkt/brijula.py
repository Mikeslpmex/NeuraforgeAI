import subprocess
import json

def get_android_compass():
    # Llama a la API de sensores de Termux
    result = subprocess.check_output(["termux-sensor", "-s", "orientation", "-n", "1"])
    data = json.loads(result)
    return data['orientation']['values'][0] # Azimuth (0-360)
