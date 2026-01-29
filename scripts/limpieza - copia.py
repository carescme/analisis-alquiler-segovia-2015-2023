import pandas as pd
import os

def limpiar_datos():
    print("--- Iniciando Limpieza de Datos ---")
    
    # 1. PROCESAR ALQUILER (Excel de SERPAVI)
    ruta_alquiler = "../data/raw/2025-09-10_bd_SERPAVI_2011-2023.xlsx"
    df_alq = pd.read_excel(ruta_alquiler, sheet_name='Municipios')
    
    # Filtramos por Segovia (Código Provincia 40)
    df_alq = df_alq[df_alq['CPRO'] == 40].copy()
    
    # Transformamos de formato ancho a largo
    df_long = df_alq.melt(id_vars=['CUMUN', 'NMUN'], var_name='temp', value_name='valor')
    
    # --- ARREGLO PARA EL ERROR NaN ---
    # 1. Extraemos el año pero lo dejamos como texto primero
    df_long['anio_str'] = df_long['temp'].str.extract(r'(\d+)$')
    
    # 2. Eliminamos las filas donde el año sea nulo (columnas que no son de datos anuales)
    df_long = df_long.dropna(subset=['anio_str'])
    
    # 3. Ahora sí, convertimos a entero de forma segura
    df_long['anio'] = df_long['anio_str'].astype(int) + 2000
    df_long['metrica'] = df_long['temp'].str.replace(r'_\d+$', '', regex=True)
    
    # Filtrar 2015-2023 y Pivotar
    df_alq_final = df_long[df_long['anio'] >= 2015].pivot_table(
        index=['CUMUN', 'NMUN', 'anio'], 
        columns='metrica', 
        values='valor',
        aggfunc='first' # Por si hay duplicados
    ).reset_index()

    # 2. PROCESAR RENTA (CSV del INE)
    ruta_renta = "../data/raw/INE-31196.csv"
    
    # Probamos a leer con 'sep=None' para que Pandas detecte si es coma o punto y coma automáticamente
    # Usamos 'encoding_errors="replace"' por si hay caracteres extraños
    df_renta = pd.read_csv(ruta_renta, sep=None, engine='python', encoding='utf-8-sig')
    
    # Limpiamos los nombres de las columnas (quita espacios y el posible carácter BOM)
    df_renta.columns = df_renta.columns.str.strip().str.replace('ï»¿', '').str.replace('\ufeff', '')
    
    print(f"Columnas detectadas en Renta: {df_renta.columns.tolist()}")

    # Extraer CUMUN y limpiar números
    # Usamos el nombre de columna detectado para evitar el KeyError
    col_muni = 'Municipios' 
    
    df_renta['CUMUN'] = df_renta[col_muni].str.extract(r'^(\d{5})').astype(float)
    
    # Limpieza de la columna Total (quitamos puntos de miles y cambiamos coma por punto)
    df_renta['Total'] = df_renta['Total'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    df_renta['Total'] = pd.to_numeric(df_renta['Total'], errors='coerce')
    
    # Filtrar solo Segovia (40xxx) y años desde 2015
    df_renta = df_renta[(df_renta['CUMUN'] >= 40000) & (df_renta['CUMUN'] < 41000) & (df_renta['Periodo'] >= 2015)]
    df_renta = df_renta.dropna(subset=['CUMUN'])

    # 3. GUARDAR RESULTADOS
    if not os.path.exists('../data/cleaned'):
        os.makedirs('../data/cleaned')
        
    df_alq_final.to_csv("../data/cleaned/alquiler_limpio.csv", index=False, encoding='utf-8-sig')
    df_renta.to_csv("../data/cleaned/renta_limpia.csv", index=False, encoding='utf-8-sig')
    print("✅ Archivos guardados con éxito en ../data/cleaned/")

if __name__ == "__main__":
    limpiar_datos()