import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report, f1_score, accuracy_score

print("--- INICIANDO PASO 4: ENTRENAMIENTO DE MODELOS ---")

# 1. Cargar datos
df = pd.read_csv('dataset_final_para_modelos.csv')
df['FECHA'] = pd.to_datetime(df['FECHA'])

# 2. Split Temporal (REQUISITO: Entrenar con pasado, probar con futuro)
# Usaremos datos hasta 2018 para entrenar y 2019-2021 para probar
train = df[df['FECHA'].dt.year <= 2018]
test = df[df['FECHA'].dt.year > 2018]

X_cols = ['lluvia_ayer', 'tmax_ayer', 'pm_media_estado', 'radiacion_lag1']
y_col = 'target_lluvia'

X_train, y_train = train[X_cols], train[y_col]
X_test, y_test = test[X_cols], test[y_col]

# Diccionario para resultados
resultados = {}

# --- MODELO 1: Regresión Logística ---
print("Entrenando Regresión Logística...")
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)
resultados['Reg. Logística'] = f1_score(y_test, pred_lr)

# --- MODELO 2: Random Forest ---
print("Entrenando Random Forest...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
resultados['Random Forest'] = f1_score(y_test, pred_rf)

# --- MODELO 3: XGBoost ---
print("Entrenando XGBoost...")
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)
pred_xgb = xgb.predict(X_test)
resultados['XGBoost'] = f1_score(y_test, pred_xgb)

# 3. Gráfica de Comparativa de Modelos
plt.figure(figsize=(10,6))
sns.barplot(x=list(resultados.keys()), y=list(resultados.values()), palette='viridis')
plt.title('Comparativa de Modelos (F1-Score)')
plt.ylabel('Puntaje F1')
plt.ylim(0, 1)
plt.savefig('comparativa_modelos.png')
print("Gráfica 'comparativa_modelos.png' guardada.")

# 4. Matriz de Confusión (Del mejor modelo: XGBoost)
plt.figure(figsize=(8,6))
cm = confusion_matrix(y_test, pred_xgb)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Confusión - XGBoost')
plt.ylabel('Realidad')
plt.xlabel('Predicción')
plt.savefig('matriz_confusion.png')
print("Gráfica 'matriz_confusion.png' guardada.")

# 5. Importancia de las variables
importancias = pd.DataFrame({'Variable': X_cols, 'Importancia': rf.feature_importances_})
importancias = importancias.sort_values(by='Importancia', ascending=False)
print("\n--- IMPORTANCIA DE LAS VARIABLES ---")
print(importancias)

print("\n¡PASO 4 COMPLETADO EXITOSAMENTE!")