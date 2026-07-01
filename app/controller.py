from tkinter import messagebox
from controller.procesamiento import Procesar_archivos
from controller.reglas import verificar_oracle_client
import logging


class AppController:

    def __init__(self, root):
        self.root = root

    def ejecutar_proceso(self, archivos, fecha_inicio, fecha_fin):

        try:
            verificar_oracle_client()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error con el cliente de Oracle:\n{str(e)}"
            )
            return

        try:
            logging.info("Iniciando proceso")
            resultado = Procesar_archivos(archivos, fecha_inicio, fecha_fin)
            logging.info("Proceso completado")

            messagebox.showinfo(
                "Éxito",
                "El proceso se ejecutó correctamente."
            )

            return resultado        
                
        except BaseException as e: 
            print("ERROR CAPTADO GLOBAL:", e)

            messagebox.showerror(
                "Error",
                f"Ocurrió un error:\n{str(e)}"
            )

            logging.error(f"Error en controller: {str(e)}")

            return None
