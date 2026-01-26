import pandas as pd
from sqlalchemy import create_engine
import sys
import os

# Esto permite que Python encuentre el archivo config.py en la carpeta superior
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DB_CONFIG

# Creamos el engine usando el diccionario de config.py
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['pass']}@{DB_CONFIG['host']}/{DB_CONFIG['db']}"
)

def cargar_datos_final():
    print("--- Iniciando Carga de Datos en MySQL ---")
    
    # 1. PREPARAR TABLA MAESTRA DE MUNICIPIOS (Unión de ambos archivos)
    print("Sincronizando lista de municipios...")
    df_alq = pd.read_csv("../data/cleaned/alquiler_limpio.csv", encoding='utf-8-sig')
    df_renta = pd.read_csv("../data/cleaned/renta_limpia.csv", encoding='utf-8-sig')

    # Sacamos los códigos y nombres de ambos para que no falte ninguno
    muni_alq = df_alq[['CUMUN', 'NMUN']].drop_duplicates()
    muni_alq.columns = ['cumun', 'nombre']
    
    # El de renta no suele traer el nombre limpio, así que usamos el de alquiler como base
    # pero nos aseguramos de que todos los CUMUN de renta existan en la tabla maestra
    muni_renta_cods = df_renta[['CUMUN']].drop_duplicates()
    muni_renta_cods.columns = ['cumun']
    
    # Unimos todos los códigos únicos
    todos_los_codigos = pd.merge(muni_renta_cods, muni_alq, on='cumun', how='left')
    # Si algún municipio del INE no estaba en el de alquiler, le ponemos un nombre genérico
    todos_los_codigos['nombre'] = todos_los_codigos['nombre'].fillna("Municipio Desconocido")
    
    # 2. CARGAR MUNICIPIOS
    # Usamos if_exists='append' pero la tabla debe estar vacía para evitar duplicados de PK
    todos_los_codigos.to_sql('municipios', con=engine, if_exists='append', index=False)
    print(f"✅ 1/3 Tabla 'municipios' cargada con {len(todos_los_codigos)} registros.")

    # 3. CARGAR ALQUILER
    # Mapeamos las columnas del CSV a las de la BD
    # Nota: He usado los nombres que aparecían en tus capturas (ALQM2_LV_M_VC, etc.)
    df_alq_sql = df_alq[['CUMUN', 'anio', 'ALQM2_LV_M_VC', 'ALQTBID12_M_VC', 'SLVM2_M_VC']].copy()
    df_alq_sql.columns = ['cumun', 'anio', 'precio_m2_mediana', 'alquiler_mensual_mediana', 'superficie_mediana']
    
    df_alq_sql.to_sql('alquiler', con=engine, if_exists='append', index=False)
    print("✅ 2/3 Tabla 'alquiler' cargada.")

    # 4. CARGAR RENTA
    df_renta_sql = df_renta[['CUMUN', 'Periodo', 'Indicadores de renta media y mediana', 'Total']].copy()
    df_renta_sql.columns = ['cumun', 'anio', 'indicador_tipo', 'valor_euros']
    
    # Eliminamos nulos en CUMUN para evitar errores de clave ajena
    df_renta_sql = df_renta_sql.dropna(subset=['cumun'])
    
    # IMPORTANTE: Solo cargamos renta de municipios que ya hemos metido en la tabla municipios
    # (Esto evita el IntegrityError que te salió)
    df_renta_sql = df_renta_sql[df_renta_sql['cumun'].isin(todos_los_codigos['cumun'])]
    
    df_renta_sql.to_sql('renta', con=engine, if_exists='append', index=False)
    print("✅ 3/3 Tabla 'renta' cargada.")

    print("\n🚀 ¡PROCESO COMPLETADO CON ÉXITO!")

if __name__ == "__main__":
    cargar_datos_final()