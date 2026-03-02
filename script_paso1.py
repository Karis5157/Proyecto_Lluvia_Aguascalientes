import pandas as pd
from bs4 import BeautifulSoup
import os

def cargar_kml(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe en esta carpeta.")
        return None

    print(f"Leyendo estaciones desde {ruta_archivo}...")
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    
    estaciones_datos = []
    for marcador in soup.find_all('Placemark'):
        datos_estacion = {sd.get('name'): sd.text for sd in marcador.find_all('SimpleData')}
        estaciones_datos.append(datos_estacion)
    
    df = pd.DataFrame(estaciones_datos)
    return df

# EJECUCIÓN
df_catalogo = cargar_kml('doc.kml')

if df_catalogo is not None:
    print(f"\n¡ÉXITO! Se encontraron {len(df_catalogo)} estaciones.")
    print("\nAquí tienes las primeras 5:")
    print(df_catalogo[['NOMBRE', 'ESTADO', 'SITUACION']].head())
    
    # Esto crea el archivo para tu Excel
    df_catalogo.to_csv('catalogo_estaciones.csv', index=False)
    print("\nArchivo 'catalogo_estaciones.csv' creado con éxito.")