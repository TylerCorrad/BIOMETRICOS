import openpyxl
import pandas as pd
from controller.reglas import validar_salida

def exportar_df(ruta, df):
    ruta = validar_salida(ruta)
    with pd.ExcelWriter(ruta, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")

        workbook = writer.book
        worksheet = writer.sheets["Data"]

        # FORMATOS
        formato_fecha = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        formato_hora = workbook.add_format({'num_format': 'hh:mm:ss'})
        formato_horas = workbook.add_format({'num_format': 'hh:mm'})

        # APLICA SEGÚN COLUMNAS
        worksheet.set_column('F:F', 12, formato_fecha)   # FECHA
        worksheet.set_column('G:H', 15, formato_hora)    # INGRESO / SALIDA
        worksheet.set_column('I:I', 15, formato_horas)   # HORAS_LABORADAS

