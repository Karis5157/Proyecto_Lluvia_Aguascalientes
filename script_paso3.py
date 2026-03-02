import pandas as pd
import numpy as np

print("--- INICIANDO PASO 3: INGENIERÍA DE VARIABLES ---")

# 1. Cargar el dataset generado en el paso anterior
print("Cargando datos...")
try:
    df = pd.read_csv('dataset_lluvia_nacional.csv')
except FileNotFoundError:
    print("ERROR: No se encontró 'dataset_lluvia_nacional.csv'. Ejecuta el Paso 2 primero.")
    exit()

# --- NUEVO: ELIMINAR PALABRA "NULO" DE TODO EL DATAFRAME ---
print("Buscando y eliminando etiquetas 'NULO' del dataset original...")
df = df.replace('NULO', np.nan)

# --- SOLUCIÓN AL ERROR DE TIPO DE DATOS ---
print("Limpiando y convirtiendo columnas a números...")
cols_numericas = ['PRECIP', 'TMAX', 'TMIN']
for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Rellenamos nulos iniciales para cálculos
df['TMAX'] = df['TMAX'].fillna(df['TMAX'].mean())
df['TMIN'] = df['TMIN'].fillna(df['TMIN'].mean())
df['PRECIP'] = df['PRECIP'].fillna(0)

df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
df = df.dropna(subset=['FECHA'])
df = df.sort_values(['NOMBRE_ESTACION', 'FECHA'])

# 2. Crear el TARGET (Lluvia binaria: 1 si llovió, 0 si no)
df['target_lluvia'] = (df['PRECIP'] > 0).astype(int)

# 3. Crear los LAGS
print("Creando variables de 'ayer' (Lags)...")
df['lluvia_ayer'] = df.groupby('NOMBRE_ESTACION')['PRECIP'].shift(1)
df['tmax_ayer'] = df.groupby('NOMBRE_ESTACION')['TMAX'].shift(1)

# 4. INTEGRACIÓN DE CONTAMINANTES Y RADIACIÓN
print("Integrando contaminantes y radiación simulada...")
df['pm25'] = df['TMAX'] * 0.8 + np.random.normal(0, 2, len(df))
df['radiacion'] = df['TMAX'] * 30 + np.random.normal(0, 10, len(df))

df['pm_media_estado'] = df.groupby('ESTADO')['pm25'].transform('mean')
df['radiacion_lag1'] = df.groupby('NOMBRE_ESTACION')['radiacion'].shift(1)

# --- MEJORA DE LIMPIEZA TOTAL ---
print("Eliminando filas con datos incompletos y nulos residuales...")
# Ahora dropna() borrará tanto los Lags vacíos como los antiguos "NULOS" de CONAGUA
df = df.dropna() 

# 5. Guardar el dataset con manejo de error de permisos
try:
    df.to_csv('dataset_final_para_modelos.csv', index=False)
    print("\n¡PASO 3 COMPLETADO EXITOSAMENTE!")
    print(f"Dataset generado: 'dataset_final_para_modelos.csv' con {len(df)} filas.")
    print(f"Nulos encontrados: {df.isnull().sum().sum()}") 
except PermissionError:
    print("\n¡ERROR DE PERMISO!")
    print("No se pudo guardar el archivo porque 'dataset_final_para_modelos.csv' está abierto en Excel.")
    print("POR FAVOR, CIERRA EL EXCEL Y VUELVE A EJECUTAR EL SCRIPT.")