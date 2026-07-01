
import tempfile
import shutil
from datetime import time
import pandas as pd
import os
import logging

from controller.reglas import validar_archivo_no_vacio, validar_columnas

logger = logging.getLogger(__name__)

def copiar_seguro(ruta_original, intentos=5):

    nombre = os.path.basename(ruta_original)
    ruta_temp = os.path.join(tempfile.gettempdir(), nombre)

    for i in range(intentos):
        try:
            shutil.copy2(ruta_original, ruta_temp)

            # validar que NO esté vacío
            if os.path.exists(ruta_temp) and os.path.getsize(ruta_temp) > 0:
                return ruta_temp

        except Exception:
            pass

        time.sleep(1)

    raise Exception(f"No se pudo copiar correctamente el archivo:\n{ruta_original}")


def leer_archivos_temporales(archivos):

    dfs = []

    for archivo in archivos:
        try:
            validar_archivo_no_vacio(archivo)
            
            temp_path = copiar_seguro(archivo)
            xls = pd.ExcelFile(temp_path)
            
            if "Validacion" not in xls.sheet_names:
                raise Exception("El documento debe contar con la hoja ""Validación""")

            # ---------
            # Leer Excel
            # ---------
            df_temp = pd.read_excel(
                temp_path,
                engine="openpyxl",
                sheet_name="Validacion",
                header=0,
            )
            df_temp = normalizar_columnas(df_temp)
            if validar_columnas(df_temp):         
                df_temp["HUELLERO"] = os.path.basename(archivo).split("_")[-1].split(".")[0]
                df_temp = df_temp[["DOCUMENTO","FECHA Y HORA","HUELLERO"]]
                dfs.append(df_temp)
            else:
                return None
                
        except ValueError as e:
            if "Worksheet named" in str(e):
                raise Exception(
                    f"El archivo no contiene la hoja 'Validacion':\n{archivo}"
                )
            else:
                raise

        except Exception as e:
            raise Exception(
                f"Error con archivo:\n{archivo}\n\n{str(e)}"
            )


    return pd.concat(dfs, ignore_index=True)

def convertir_a_fecha(col):

    if pd.api.types.is_datetime64_any_dtype(col):
        return col
    else:
        # si ya parece número (Excel), convertir diferente
        if pd.api.types.is_numeric_dtype(col):
            try:
                dt = pd.to_datetime(col, unit="d", origin="1899-12-30", errors="coerce")
            except Exception as e:
                raise Exception(f"Hay un error con el formato de la columna {col.name}: {str(e)}")
        else:
            # si es otro tipo, intentar convertir directamente
            dt = pd.to_datetime(col, errors="coerce")
    return dt

def normalizar_columnas(df):
    df.columns = df.columns.astype(str).str.strip().str.replace("\n", " ").str.replace("\r", " ").str.upper()
    return df

def filtrar_por_fecha(df, fecha_inicio, fecha_fin):

    df["FECHA Y HORA"] = convertir_a_fecha(df["FECHA Y HORA"])
    df_filtrado = df[(df["FECHA Y HORA"] >= fecha_inicio) & (df["FECHA Y HORA"] <= pd.to_datetime(fecha_fin)+ pd.Timedelta(days=1)-pd.Timedelta(seconds=1))]  # Incluye todo el día final
    return df_filtrado

def preparacion_huelleros(df_huelleros):
    df_huelleros["FECHA"] = convertir_a_fecha(df_huelleros["FECHA"])
    doc_map = {col: "NIT" for col in df_huelleros.columns if str(col).strip() == "DOCUMENTO"}
    if doc_map:
        df_huelleros = df_huelleros.rename(columns=doc_map)
    df_huelleros["NIT"] = df_huelleros["NIT"].astype(str)
    return df_huelleros

def preparacion_NITs_fechas(df_NITs_fechas):
    df_NITs_fechas["NIT"] = df_NITs_fechas["NIT"].astype(str)
    return df_NITs_fechas

def normalizar_fechas(df):
    df["FECHA"] = convertir_a_fecha(df["FECHA"])
    return df

def horas_laboradas(df):
    # reafirmar formato
    df["HORA_INGRESO"] = convertir_a_fecha(df["HORA_INGRESO"])
    df["HORA_SALIDA"]  = convertir_a_fecha(df["HORA_SALIDA"])

#horas laboradas
    df["HORAS_LABORADAS"] = df["HORA_SALIDA"] - df["HORA_INGRESO"]
    df["CANTIDAD_HORAS_LABORADAS"] = (df["HORAS_LABORADAS"].dt.total_seconds()/3600)
    return df

    
def llenar_nulos(df):
    df.loc[
        df["HORA_INGRESO"].isna(),
        ["HUELLERO_INGRESO"]
        ] = "NO REGISTRA"
    df.loc[
        df["HORA_SALIDA"].isna(),
        ["HUELLERO_SALIDA"]
        ] = "NO REGISTRA"
    df.loc[
        df["CANTIDAD_HORAS_LABORADAS"].isna(),
        ["CANTIDAD_HORAS_LABORADAS"]
        ] = 0
    df["HORAS_LABORADAS"] = pd.to_timedelta(df["HORAS_LABORADAS"], errors='coerce')
    df["HORAS_LABORADAS"] = df["HORAS_LABORADAS"].fillna(pd.Timedelta(0))
    df["HORAS_LABORADAS"] = df["HORAS_LABORADAS"].dt.total_seconds() / 86400
    return df

def reorganizar_columnas(df):
    df = df.reindex(columns = ["NIT","empresa","Nombre", "Cargo", "Dependencia", "FECHA", "HORA_INGRESO", "HORA_SALIDA", "HORAS_LABORADAS","CANTIDAD_HORAS_LABORADAS","HUELLERO_INGRESO", "HUELLERO_SALIDA"])
    df = df.rename(columns={
        "NIT": "DOCUMENTO",
        "empresa": "EMPRESA",
        "Nombre" : "NOMBRE",
        "Cargo" : "NOMBRE_CARGO",
        "Dependencia" : "NOMBRE_DEPENDENCIA",
        "HUELLERO_INGRESO" : "H_INGRESO",
        "HUELLERO_SALIDA" : "H_SALIDA"
        })
    return df
    
def formatos_finales(df):
    df = df.astype({
        "DOCUMENTO": "int64",
        "EMPRESA": "string",
        "NOMBRE": "string",
        "NOMBRE_CARGO": "string",
        "NOMBRE_DEPENDENCIA": "string"
        })
    df["FECHA"] = pd.to_datetime(df["FECHA"]).dt.normalize()

    df["HORA_INGRESO"] = pd.to_datetime(df["HORA_INGRESO"], errors="coerce").dt.time
    df["HORA_SALIDA"] = pd.to_datetime(df["HORA_SALIDA"], errors="coerce").dt.time
    
    df["HORA_INGRESO"] = df["HORA_INGRESO"].fillna(time(0, 0, 0))
    df["HORA_SALIDA"] = df["HORA_SALIDA"].fillna(time(0, 0, 0))
    
    df["HORA_INGRESO"] = (
        pd.to_datetime(df["HORA_INGRESO"].astype(str)).dt.hour / 24
        + pd.to_datetime(df["HORA_INGRESO"].astype(str)).dt.minute / (24*60)
        + pd.to_datetime(df["HORA_INGRESO"].astype(str)).dt.second / (24*3600)
    )
    df["HORA_SALIDA"] = (
        pd.to_datetime(df["HORA_SALIDA"].astype(str)).dt.hour / 24
        + pd.to_datetime(df["HORA_SALIDA"].astype(str)).dt.minute / (24*60)
        + pd.to_datetime(df["HORA_SALIDA"].astype(str)).dt.second / (24*3600)
    )
    df["CANTIDAD_HORAS_LABORADAS"] = df["CANTIDAD_HORAS_LABORADAS"].round(2)
    return(df)




def limpieza_final(df):
    df = llenar_nulos(df)
    df = reorganizar_columnas(df)
    df = formatos_finales(df)
    df = df.drop_duplicates()
    return df