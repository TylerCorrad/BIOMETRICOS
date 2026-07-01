from sqlalchemy import engine, text, create_engine
import pandas as pd
from SQL import query_empleados
from config.config import cargar_config
from data.security import desencriptar


def cargar_empleados_activos():

    try:
        config = cargar_config()
        contraseña = desencriptar(config['PASSWORD'])
        connection_url = (
            f"oracle+oracledb://{config['USER']}:{contraseña}"
            f"@{config['HOST']}:{config['PORT']}/?service_name={config['SID']}"
        )
    except Exception as e:
        raise Exception(f"Error al cargar la configuración:\n{str(e)}")
    
    engine = create_engine(
        connection_url,
        pool_pre_ping=True,
        pool_recycle=1200
        )


    query = query_empleados.query

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            df_emp = pd.DataFrame(result)

    except Exception as e:
        raise Exception(f"Error en la base de datos:\n{str(e)}")

    finally:
        engine.dispose()

    df_emp = df_emp.rename(columns={'nit': 'NIT'})

    return df_emp
