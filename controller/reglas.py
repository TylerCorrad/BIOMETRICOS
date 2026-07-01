import pandas as pd
from config import config
import os
import logging
import tkinter as tk


def verificar_oracle_client(r_instantClient=None):
    if r_instantClient is None:
        r_instantClient = config.r_instantClient

    if not r_instantClient or not os.path.exists(r_instantClient):
        logging.error(f"No se encuentra oracle Instant Client")        
        raise FileNotFoundError(f"No se encontró el Oracle Instant Client en la ruta: {r_instantClient} trate instalando la versión 19.30 y ubicandola en la ruta indicada")


def validar_archivo_no_vacio(ruta):
    if not os.path.exists(ruta):
        logging.error(f"archivo no existe: \n{ruta}")
        raise Exception(f"El archivo no existe:\n{ruta}")

    if os.path.getsize(ruta) == 0:
        logging.error(f"archivo vacio: \n{ruta}")
        raise Exception(f"El archivo está vacío:\n{ruta}")

def preguntar_sobre_escritura(ruta_final):

    opcion = {"valor": None}

    def seleccionar(op):
        opcion["valor"] = op
        ventana.destroy()

    ventana = tk.Toplevel()
    ventana.title("Archivo existente")
    ventana.geometry("400x180")
    ventana.resizable(False, False)

    label = tk.Label(
        ventana,
        text=f"El archivo ya existe:\n\n{ruta_final}\n\n¿Qué desea hacer?",
        justify="center"
    )
    label.pack(pady=20)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack()

    btn_sobrescribir = tk.Button(
        frame_botones, text="Sobrescribir",
        width=15, command=lambda: seleccionar("sobrescribir")
    )
    btn_sobrescribir.grid(row=0, column=0, padx=5)

    btn_copia = tk.Button(
        frame_botones, text="Guardar copia",
        width=15, command=lambda: seleccionar("copia")
    )
    btn_copia.grid(row=0, column=1, padx=5)

    btn_cancelar = tk.Button(
        frame_botones, text="Cancelar",
        width=15, command=lambda: seleccionar("cancelar")
    )
    btn_cancelar.grid(row=0, column=2, padx=5)

    ventana.grab_set()   # bloquea interacción con otras ventanas
    ventana.wait_window()

    return opcion["valor"]


def validar_salida(ruta_final):

    if not ruta_final.exists():
        return ruta_final

    logging.warning(f"El archivo ya existe: {ruta_final}")

    opcion = preguntar_sobre_escritura(ruta_final)

    if opcion == "cancelar":
        raise Exception("Proceso cancelado por el usuario.")

    elif opcion == "sobrescribir":
        return ruta_final

    elif opcion == "copia":
        # generar nombre nuevo
        base = ruta_final.stem
        ext = ruta_final.suffix
        carpeta = ruta_final.parent

        i = 1
        while True:
            nueva_ruta = carpeta / f"{base}_{i}{ext}"

            if not nueva_ruta.exists():
                return nueva_ruta

            i += 1
def validar_columnas(df):
    columnas_requeridas = ["DOCUMENTO", "FECHA Y HORA"]

    faltantes = [col for col in columnas_requeridas if col not in df.columns]

    if faltantes:
        raise Exception(
            f"Faltan columnas requeridas:\n{faltantes}\n\n"
            f"Columnas disponibles:\n{df.columns.tolist()}"
        )

    return True
    
    
