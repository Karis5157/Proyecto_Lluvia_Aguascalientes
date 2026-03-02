import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

print("--- INICIANDO PASO 5: RED NEURONAL (MLP) ---")

# 1. Cargar datos
df = pd.read_csv('dataset_final_para_modelos.csv')
df['FECHA'] = pd.to_datetime(df['FECHA'])

# 2. Split Temporal (Igual que los anteriores)
train = df[df['FECHA'].dt.year <= 2019]
test = df[df['FECHA'].dt.year >= 2020]

X_cols = ['lluvia_ayer', 'tmax_ayer', 'pm_media_estado', 'radiacion_lag1']
y_col = 'target_lluvia'

X_train, y_train = train[X_cols], train[y_col]
X_test, y_test = test[X_cols], test[y_col]

# 3. Escalar los datos (Las Redes Neuronales lo necesitan para converger)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Crear y Entrenar la Red Neuronal (MLP)
print("Entrenando Red Neuronal (Multi-layer Perceptron)...")
# Definimos una red con 2 capas ocultas de 50 y 25 neuronas
mlp = MLPClassifier(hidden_layer_sizes=(50, 25), 
                    max_iter=500, 
                    activation='relu', 
                    solver='adam', 
                    random_state=42,
                    verbose=True)

mlp.fit(X_train_scaled, y_train)

# 5. Evaluación
pred_mlp = mlp.predict(X_test_scaled)
print("\n--- RESULTADOS RED NEURONAL ---")
print(classification_report(y_test, pred_mlp))

# 6. Gráfica de la Curva de Pérdida (Cómo aprendió la red)
plt.figure(figsize=(10, 6))
plt.plot(mlp.loss_curve_)
plt.title('Curva de Aprendizaje - Red Neuronal')
plt.xlabel('Iteraciones')
plt.ylabel('Costo (Loss)')
plt.grid(True)
plt.savefig('aprendizaje_red_neuronal.png')

print("\n¡PASO 5 COMPLETADO!")
print("Se generó la gráfica 'aprendizaje_red_neuronal.png'.")