import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score

print("=" * 80)
print("GENERADOR DE MODELOS PICKLE")
print("=" * 80)

# Cargar el dataset
print("\nCargando dataset...")
df = pd.read_csv("dataset_proyecto_objetos.csv")
print(f"Dataset cargado: {df.shape[0]} registros")

# Separar características (X) y etiquetas (y)
X = df.drop("tipo_objeto", axis=1)
y = df["tipo_objeto"]

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Conjunto de entrenamiento: {X_train.shape[0]} registros")
print(f"Conjunto de prueba: {X_test.shape[0]} registros")

# ============================================================================
# MODELO 1: KNN (K-Nearest Neighbors)
# ============================================================================
print("\n" + "=" * 80)
print("ENTRENANDO MODELO KNN")
print("=" * 80)

modelo_knn = KNeighborsClassifier(n_neighbors=5)
modelo_knn.fit(X_train, y_train)
print("Modelo KNN entrenado")

# Evaluar el modelo KNN
y_pred_knn = modelo_knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
f1_knn = f1_score(y_test, y_pred_knn, average="weighted")

print(f"\nMétricas del modelo KNN:")
print(f"  Accuracy:  {accuracy_knn:.4f}")
print(f"  F1-Score:  {f1_knn:.4f}")

# Guardar el modelo KNN en archivo pickle
with open("modelo_knn.pkl", "wb") as archivo:
    pickle.dump(modelo_knn, archivo)
print("\nModelo KNN guardado como 'modelo_knn.pkl'")

# ============================================================================
# MODELO 2: Árbol de Decisión
# ============================================================================
print("\n" + "=" * 80)
print("ENTRENANDO MODELO ÁRBOL DE DECISIÓN")
print("=" * 80)

modelo_arbol = DecisionTreeClassifier(random_state=42)
modelo_arbol.fit(X_train, y_train)
print("Modelo Árbol de Decisión entrenado")

# Evaluar el modelo de Árbol de Decisión
y_pred_arbol = modelo_arbol.predict(X_test)
accuracy_arbol = accuracy_score(y_test, y_pred_arbol)
f1_arbol = f1_score(y_test, y_pred_arbol, average="weighted")

print(f"\nMétricas del modelo Árbol de Decisión:")
print(f"  Accuracy:  {accuracy_arbol:.4f}")
print(f"  F1-Score:  {f1_arbol:.4f}")

# Guardar el modelo de Árbol de Decisión en archivo pickle
with open("modelo_arbol_decision.pkl", "wb") as archivo:
    pickle.dump(modelo_arbol, archivo)
print("\nModelo Árbol de Decisión guardado como 'modelo_arbol_decision.pkl'")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 80)
print("RESUMEN DE MODELOS GENERADOS")
print("=" * 80)
print("\nArchivos pickle generados:")
print("  1. modelo_knn.pkl")
print(f"     - Accuracy:  {accuracy_knn:.4f}")
print(f"     - F1-Score:  {f1_knn:.4f}")
print("\n  2. modelo_arbol_decision.pkl")
print(f"     - Accuracy:  {accuracy_arbol:.4f}")
print(f"     - F1-Score:  {f1_arbol:.4f}")

print("\n" + "=" * 80)
print("PROCESO COMPLETADO")
print("=" * 80)
print("\nUso de los modelos:")
print("   import pickle")
print("   with open('modelo_knn.pkl', 'rb') as f:")
print("       modelo = pickle.load(f)")
print("   prediccion = modelo.predict([[rareza, nivel, precio, porcentaje, valor]])")
