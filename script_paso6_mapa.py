import pandas as pd
import folium

# Cargar el catálogo original que creaste en el paso 1
df_geo = pd.read_csv('catalogo_estaciones.csv')

# Filtrar solo las que usamos (las primeras 20 que estén OPERANDO)
df_mapa = df_geo[df_geo['SITUACION'] == 'OPERANDO'].head(20)

# Crear mapa centrado en México
m = folium.Map(location=[23.6345, -102.5528], zoom_start=5)

for _, fila in df_mapa.iterrows():
    folium.Marker(
        location=[fila['LATITUD'], fila['LONGITUD']],
        popup=f"Estación: {fila['NOMBRE']}<br>Estado: {fila['ESTADO']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

m.save('mapa_estaciones.html')
print("Mapa generado como 'mapa_estaciones.html'. Ábrelo en tu navegador.")