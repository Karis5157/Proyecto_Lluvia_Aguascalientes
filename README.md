# Proyecto_Lluvia_Aguascalientes
Este proyecto tiene como objetivo desarrollar un modelo de Inteligencia de Negocios y Machine Learning para predecir la precipitación pluvial en el estado de Aguascalientes, México. Utilizando datos históricos de CONAGUA, el modelo ayuda a optimizar la toma de decisiones en infraestructura y gestión de riesgos.

📋 Descripción del Proyecto
El proyecto se divide en las siguientes etapas técnicas:

Extracción de Datos: Procesamiento de archivos KML de CONAGUA para identificar estaciones climatológicas operadas por el SMN.

Limpieza y Preprocesamiento: Manejo de valores nulos y conversión de fechas al formato datetime.

Ingeniería de Variables: Creación de variables temporales y variables de tendencia como medias móviles de 7 y 30 días (PRECIP_30D, PRECIP_7D).

Modelado: Entrenamiento y comparativa de clasificadores binarios (Regresión Logística, Random Forest, XGBoost).

📊 Resultados y Visualizaciones
Al ejecutar los scripts, se generarán las siguientes imágenes clave para el análisis:

comparativa_modelos_f1.png: Gráfica que muestra el rendimiento de los modelos, donde Random Forest destaca como el mejor predictor.

importancia_variables.png: Gráfica que revela que la radiación solar y la lluvia acumulada de los últimos 30 días son los factores más influyentes.

matrices_confusion.png: Evaluación detallada de aciertos y errores de los modelos.

🧠 Insights de Negocio

Memoria Climática: Se descubrió que la radiación solar del día anterior tiene un impacto del 86% en las predicciones, lo que facilita la creación de modelos simplificados pero efectivos.

Decisiones Estratégicas: El modelo permite transformar casi 200,000 registros en información accionable para inversiones agrícolas o logísticas.
