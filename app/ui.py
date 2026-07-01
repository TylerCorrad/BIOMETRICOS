import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import re
from pathlib import Path
import json

from data.security import encriptar, desencriptar

class AppUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.archivos = []

        self.build_ui()

    def build_ui(self):
        # -------------------------
        # Título
        # -------------------------
        titulo = tk.Label(self.root, text="Sistema procesamiento Biométricos", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        # -------------------------
        # Botón cargar archivos
        # -------------------------
        btn_archivos = tk.Button(
            self.root,
            text="Seleccionar archivos huelleros",
            command=self.seleccionar_archivos,
            width=30,
            height=2
        )
        btn_archivos.pack(pady=5)

        # Label archivos
        self.label_archivos = tk.Label(self.root, text="No se han seleccionado archivos")
        self.label_archivos.pack(pady=5)
        
        btn_config = tk.Button(
        self.root,
        text="⚙ Conexión BD",
        command=self.abrir_configuracion,
        width=30,
        height=2)
        btn_config.pack(pady=5)
        

        # -------------------------
        # Fechas
        # -------------------------
        frame_fechas = tk.Frame(self.root)
        frame_fechas.pack(pady=10)

        tk.Label(frame_fechas, text="Fecha inicio (YYYY-MM-DD)").grid(row=0, column=0)
        tk.Label(frame_fechas, text="Fecha fin (YYYY-MM-DD)").grid(row=1, column=0)

        self.entry_inicio = tk.Entry(frame_fechas)
        self.entry_inicio.grid(row=0, column=1, padx=5)

        self.entry_fin = tk.Entry(frame_fechas)
        self.entry_fin.grid(row=1, column=1, padx=5)

        # -------------------------
        # Botón ejecutar
        # -------------------------
        btn_ejecutar = tk.Button(
            self.root,
            text="Generar reporte",
            command=self.generar_reporte,
            bg="#4CAF50",
            fg="white",
            width=30,
            height=2
        )
        btn_ejecutar.pack(pady=15)

    # -------------------------
    # FUNCIONES UI
    # -------------------------

    def seleccionar_archivos(self):
        archivos = filedialog.askopenfilenames(
            title="Selecciona los archivos de huelleros",
            filetypes=[("Excel", "*.xlsx *.xlsm")]
        )

        if len(archivos) == 0:
            return

        self.archivos = list(archivos)

        self.label_archivos.config(
            text=f"{len(self.archivos)} archivos seleccionados"
        )

    def generar_reporte(self):
        # Validar archivos
        if len(self.archivos) < 1:
            messagebox.showerror("Error", "Debes seleccionar al menos un archivo")
            return

        fecha_inicio = self.entry_inicio.get()
        fecha_fin = self.entry_fin.get()
        patron = r"^\d{4}-\d{2}-\d{2}" 
        
        if not (re.match(patron,fecha_fin) and re.match(patron,fecha_inicio)):
            messagebox.showerror("error en formato de fecha","la fecha de inicio y la fecha de fin tienen que cumplir con el formato indicado (YYYY-MM-DD)")
            return

        try:
            resultado = self.controller.ejecutar_proceso(
                archivos=self.archivos,
                fecha_inicio=datetime.strptime(fecha_inicio, "%Y-%m-%d"),
                fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d")
            )            
            if resultado is None:
                return

            messagebox.showinfo(
                "Éxito",
                f"Reporte generado correctamente en:\n{resultado}"
            )

        except Exception as e:
            messagebox.showerror("Error: ", str(e))
            return
        
    def abrir_configuracion(self):
        config = cargar_config()

        ventana = tk.Toplevel(self.root)
        ventana.title("Configuración de Base de Datos")
        ventana.geometry("400x300")

        tk.Label(ventana, text="Usuario").pack()
        entry_user = tk.Entry(ventana)
        entry_user.insert(0, config.get("USER", ""))
        entry_user.pack()

        tk.Label(ventana, text="Contraseña").pack()
        entry_pass = tk.Entry(ventana, show="*")
        entry_pass.insert(0, desencriptar(config.get("PASSWORD", "")))
        entry_pass.pack()

        tk.Label(ventana, text="Host").pack()
        entry_host = tk.Entry(ventana)
        entry_host.insert(0, config.get("HOST", ""))
        entry_host.pack()

        tk.Label(ventana, text="Puerto").pack()
        entry_port = tk.Entry(ventana)
        entry_port.insert(0, config.get("PORT", "1521"))
        entry_port.pack()

        tk.Label(ventana, text="SID / Service Name").pack()
        entry_sid = tk.Entry(ventana)
        entry_sid.insert(0, config.get("SID", ""))
        entry_sid.pack()

        def guardar():
            nuevo_config = {
                "USER": entry_user.get(),
                "PASSWORD": encriptar(entry_pass.get()),
                "HOST": entry_host.get(),
                "PORT": entry_port.get(),
                "SID": entry_sid.get()
            }

            guardar_config(nuevo_config)

            messagebox.showinfo("Configuración", "Datos guardados correctamente")
            ventana.destroy()

        btn_guardar = tk.Button(
            ventana,
            text="Guardar",
            command=guardar,
            bg="#4CAF50",
            fg="white"
        )
        btn_guardar.pack(pady=10)
            
        def probar_conexion():
            try:
                # intenta conectar
                messagebox.showinfo("OK", "Conexión exitosa")
            except:
                messagebox.showerror("Error", "No se pudo conectar")
       
#=================VENTANA CONFIGURACIÖN BD=================
CONFIG_PATH = Path.cwd() / "config.json"

def cargar_config():
    if not CONFIG_PATH.exists():
        guardar_config({
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "1521",
            "SID": ""
        })

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
