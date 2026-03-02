import pandas as pd
import requests
import io
import time
import urllib3

# Desactivar advertencias de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df_catalogo = pd.read_csv('catalogo_estaciones.csv')
estaciones_objetivo = df_catalogo[df_catalogo['SITUACION'] == 'OPERANDO'].head(20)

def descargar_diarios(nombre, url):
    try:
        print(f"Descargando datos de: {nombre}...")
        # CLAVE: verify=False soluciona tu error de SSL
        respuesta = requests.get(url, timeout=15, verify=False)
        if respuesta.status_code != 200:
            return None
        
        contenido = respuesta.text
        lineas = contenido.split('\n')
        inicio_datos = 0
        for i, linea in enumerate(lineas):
            if 'FECHA' in linea.upper():
                inicio_datos = i
                break
        
        df = pd.read_csv(io.StringIO('\n'.join(lineas[inicio_datos:])), 
                         sep=r'\s+', engine='python', skiprows=[1])
        return df
    except Exception as e:
        print(f"Error con {nombre}: {e}")
        return None

lista_dfs = []
for i, fila in estaciones_objetivo.iterrows():
    df_temp = descargar_diarios(fila['NOMBRE'], fila['DIARIOS'])
    if df_temp is not None:
        df_temp['ESTADO'] = fila['ESTADO']
        df_temp['NOMBRE_ESTACION'] = fila['NOMBRE']
        lista_dfs.append(df_temp)
    time.sleep(0.5)

if lista_dfs:
    df_nacional = pd.concat(lista_dfs, ignore_index=True)
    df_nacional['FECHA'] = pd.to_datetime(df_nacional['FECHA'], dayfirst=True, errors='coerce')
    df_nacional['PRECIP'] = pd.to_numeric(df_nacional['PRECIP'], errors='coerce').fillna(0)
    df_nacional.to_csv('dataset_lluvia_nacional.csv', index=False)
    print(f"\n¡ÉXITO! Se creó 'dataset_lluvia_nacional.csv' con {len(df_nacional)} filas.")
else:
    print("Sigue sin poder descargarse nada. Revisa tu conexión a internet.")