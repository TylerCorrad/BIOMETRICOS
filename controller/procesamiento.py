import pandas as pd
from pathlib import Path
import datetime
from datetime import datetime
from controller.transformaciones import (limpieza_final,
                                   horas_laboradas,
                                   leer_archivos_temporales,
                                    preparacion_huelleros,
                                    filtrar_por_fecha,
                                    preparacion_NITs_fechas)
from controller.agrupaciones import (cruce_NITs_fechas, 
                                     cruce_dataframes, 
                                     obtener_ingreso_salida, 
                                     merge_ingreso_salida)
from data.loader import cargar_empleados_activos
from Excel.exportador import exportar_df



def Procesar_archivos(archivos, fecha_inicio, fecha_fin):
    #leer archivos de huelleros y preparar dataframe
    df_huelleros = leer_archivos_temporales(archivos)
    df_huelleros = filtrar_por_fecha(df_huelleros, fecha_inicio, fecha_fin)
    df_huelleros = df_huelleros.sort_values(by="FECHA Y HORA", ascending=True)
        #conectar a la base de datos y cargar empleados activos
    df_empleados = cargar_empleados_activos()
        #cruce de todos los nits con todas las fechas
    df_NITs_fechas = cruce_NITs_fechas(df_empleados, df_huelleros)
        #preparacion de dataframes para cruzar
    df_huelleros = preparacion_huelleros(df_huelleros)
    df_NITs_fechas = preparacion_NITs_fechas(df_NITs_fechas)
        #merge de dataframes de fechas, empleados y registros de huelleros
    df_all = cruce_dataframes(df_huelleros, df_NITs_fechas, df_empleados)
        #hora y huellero de ingreso y salida
    df_ingreso, df_salida = obtener_ingreso_salida(df_huelleros)
    df_all = merge_ingreso_salida(df_all, df_ingreso, df_salida)
        #limpieza de columnas y filas innecesarias
    df_all = df_all.drop(columns=["FECHA Y HORA", "HUELLERO"])
    df_all = df_all.drop_duplicates()
        # calcular horas laboradas
    df_all = horas_laboradas(df_all)
    df_all = limpieza_final(df_all)
        #exportar dataframe
    r_docs = Path.home() / "Documents"
    r_docs.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"Reporte_Biometricos_{datetime.now().strftime('%Y%m%d')}.xlsx"
    ruta_final = r_docs / nombre_archivo
    exportar_df(ruta_final,df_all)
    return ruta_final





