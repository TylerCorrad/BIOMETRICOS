import tkinter as tk

import oracledb
from app.ui import AppUI
from app.controller import AppController
from controller.reglas import verificar_oracle_client
import logging
import os
import sys
from pathlib import Path
import getpass


def main():
    init_oracle()
    
    configurar_logs()
    # crear ventrana principal
    root = tk.Tk()
    root.title("Procesamiento de biometricos")
    root.geometry("400x300")
    root.resizable(False, False)
    #inicializar controlador
    controller = AppController(root)
    #inicializar interfaz de usuario
    app_ui = AppUI(root, controller)
    #ejecutar app
    root.mainloop()


def configurar_logs():
    ruta_logs = Path.home() / "AppData" / "Local" / "BiometricosApp" / "logs"
    ruta_logs.mkdir(parents=True, exist_ok=True)
    archivo_log = ruta_logs / "app.log"

    logging.basicConfig(
        filename=str(archivo_log),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def init_oracle():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

    client_path = os.path.join(base_path, "instantclient")

    print("Ruta Oracle:", client_path)
    print("Existe:", os.path.exists(client_path))

    if not os.path.exists(client_path):
        raise Exception(f"No se encontró instantclient:\n{client_path}")

    oracledb.init_oracle_client(lib_dir=client_path)




if __name__ == "__main__":
    main()
    
