import pandas as pd
from controller.transformaciones import normalizar_fechas


def cruce_NITs_fechas(df_empleados, df_huelleros):
    print(f"Columnas empleados: {df_empleados.columns.tolist()}, Columnas huelleros: {df_huelleros.columns.tolist()}")
    df_huelleros["FECHA"] = pd.to_datetime(df_huelleros["FECHA Y HORA"]).dt.date
    df_fechas = df_huelleros[["FECHA"]].drop_duplicates()
    df_NITs_fechas = df_empleados[["NIT"]].merge(df_fechas, how="cross")
    return df_NITs_fechas

def cruce_dataframes(df_huelleros, df_NITs_fechas, df_empleados):
    df_huelleros = normalizar_fechas(df_huelleros)
    df_NITs_fechas = normalizar_fechas(df_NITs_fechas)

    print(F"fechas huelleros: {df_huelleros["FECHA"].dtypes}, fechas NITs_fechas: {df_NITs_fechas["FECHA"].dtypes}, NITS huelleros: {df_huelleros["NIT"].dtypes}, NITS NITs_fechas: {df_NITs_fechas["NIT"].dtypes}, NITS empleados: {df_empleados["NIT"].dtypes}")
    print(list(df_huelleros))
    df_all = df_NITs_fechas.merge(df_huelleros, on=["NIT", "FECHA"], how="left")
    df_all = df_all.merge(df_empleados, on="NIT", how="left")
    return df_all

def obtener_ingreso_salida(df_huelleros):
    df_ingreso = df_huelleros.loc[df_huelleros.groupby(['NIT', 'FECHA'])['FECHA Y HORA'].idxmin()]
    df_salida = df_huelleros.loc[df_huelleros.groupby(['NIT', 'FECHA'])['FECHA Y HORA'].idxmax()]

    df_ingreso = df_ingreso.rename(columns={'FECHA Y HORA': 'HORA_INGRESO', "HUELLERO": 'HUELLERO_INGRESO'})
    df_salida = df_salida.rename(columns={'FECHA Y HORA': 'HORA_SALIDA', "HUELLERO": 'HUELLERO_SALIDA'})
    df_ingreso = df_ingreso[['NIT', 'FECHA', 'HORA_INGRESO', 'HUELLERO_INGRESO']]
    df_salida = df_salida[['NIT', 'FECHA', 'HORA_SALIDA', 'HUELLERO_SALIDA']]
    return df_ingreso, df_salida

def merge_ingreso_salida(df_all, df_ingreso, df_salida):
    df_all = df_all.drop_duplicates(subset=["NIT", "FECHA"])
    df_all = pd.merge(df_all,df_ingreso,on =["NIT","FECHA"], how="left")
    df_all = pd.merge(df_all,df_salida,on =["NIT","FECHA"], how="left")
    return df_all

