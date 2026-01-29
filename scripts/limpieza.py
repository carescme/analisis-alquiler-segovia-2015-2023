import pandas as pd
import os

def limpiar_datos():
    print("--- 🚀 Iniciando Limpieza de Datos ---")
    
    # 1. RUTAS ABSOLUTAS
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    
    ruta_alquiler = os.path.join(project_root, "data", "raw", "2025-09-10_bd_SERPAVI_2011-2023.xlsx")
    ruta_renta = os.path.join(project_root, "data", "raw", "INE-31196.csv")
    output_dir = os.path.join(project_root, "data", "cleaned")

    # 2. PROCESAR ALQUILER
    if os.path.exists(ruta_alquiler):
        print(f"📂 Leyendo Alquiler: {ruta_alquiler}")
        df_alq = pd.read_excel(ruta_alquiler, sheet_name='Municipios')
        df_alq = df_alq[df_alq['CPRO'] == 40].copy()
        
        # Transformación a formato largo
        df_long = df_alq.melt(id_vars=['CUMUN', 'NMUN'], var_name='temp', value_name='valor')
        df_long['anio'] = df_long['temp'].str.extract(r'(\d+)$').astype(float) + 2000
        df_long['metrica'] = df_long['temp'].str.replace(r'_\d+$', '', regex=True)
        
        df_alq_final = df_long[df_long['anio'] >= 2015].pivot_table(
            index=['CUMUN', 'NMUN', 'anio'], columns='metrica', values='valor', aggfunc='first'
        ).reset_index()
        print(f"✅ Alquiler procesado: {len(df_alq_final)} filas.")
    else:
        print("❌ ERROR: No se encuentra el Excel de Alquiler.")

    # 3. PROCESAR RENTA (El punto crítico)
    if os.path.exists(ruta_renta):
        print(f"📂 Leyendo Renta: {ruta_renta}")
        df_renta = pd.read_csv(ruta_renta, sep=None, engine='python', encoding='utf-8-sig')
        
        # Limpieza de columnas y números
        df_renta.columns = df_renta.columns.str.strip()
        
        # Eliminamos puntos de miles y cambiamos comas por puntos antes de convertir
        df_renta['Total'] = (df_renta['Total'].astype(str)
                             .str.replace('.', '', regex=False)
                             .str.replace(',', '.', regex=False))
        df_renta['Total'] = pd.to_numeric(df_renta['Total'], errors='coerce')
        
        # Extraer CUMUN y filtrar por Segovia (40)
        df_renta['CUMUN'] = df_renta['Municipios'].str.extract(r'^(\d{5})').astype(float)
        df_renta = df_renta[(df_renta['CUMUN'] >= 40000) & (df_renta['CUMUN'] < 41000)]
        
        # IMPORTANTE: No filtramos por indicador aquí para no perder datos, 
        # lo haremos en el Notebook. Solo quitamos nulos en el Total.
        df_renta = df_renta.dropna(subset=['Total'])
        print(f"✅ Renta procesada: {len(df_renta)} filas.")
    else:
        print("❌ ERROR: No se encuentra el CSV de Renta.")

    # 4. GUARDAR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Creada carpeta: {output_dir}")

    df_alq_final.to_csv(os.path.join(output_dir, "alquiler_limpio.csv"), index=False, encoding='utf-8-sig')
    df_renta.to_csv(os.path.join(output_dir, "renta_limpia.csv"), index=False, encoding='utf-8-sig')
    print(f"🎉 ¡PROCESO FINALIZADO! Archivos guardados en {output_dir}")

if __name__ == "__main__":
    limpiar_datos()