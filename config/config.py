import os
from datetime import datetime
import json
from pathlib import Path
import sys
from data.security import encriptar, desencriptar


###### RUTAS DE LOS ARCHIVOS ######
ruta_raiz = os.path.dirname(os.path.dirname(__file__))

r_instantClient = os.path.join(ruta_raiz,"instantclient")

def temp_path(file_path):
    return os.path.join("temp", "temp_" + os.path.basename(file_path)) if file_path else None

CONFIG_PATH = Path.cwd() / "config.json"


def cargar_config():
    # Si no existe, crea uno vacío por defecto
    if not CONFIG_PATH.exists():
        config_default = {
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "1521",
            "SID": ""
        }

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_default, f, indent=4)

        return config_default

    # Leer archivo existente
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        
        return json.load(f)


def guardar_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


