# lluvia_clasificacion.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    RocCurveDisplay,
    accuracy_score,
)
import seaborn as sns
import matplotlib.pyplot as plt

# ===============================
# 1. Cargar dataset
# ===============================
df = pd.read_csv("clima_cdmx_dataset_copia.csv")

# ===============================
# 2. Limpieza y preparación
# ===============================
# Convertir fecha a datetime
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], dayfirst=True)

# Features de la fecha
df["hora"] = df["fecha_hora"].dt.hour
df["mes"] = df["fecha_hora"].dt.month
df["dia_semana"] = df["fecha_hora"].dt.dayofweek

# Eliminar columnas que no sirven directamente
df = df.drop(columns=["fecha_hora", "direccion_viento", "clima"])

# Reemplazar comas decimales por puntos
df = df.replace(",", ".", regex=True)

# Intentar convertir todo a número
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Rellenar NaN con la media
df = df.fillna(df.mean(numeric_only=True))

# ===============================
# 3. Crear variable binaria "lluvia"
# ===============================
# lluvia = 1 si la precipitación > 0, sino 0
df["lluvia"] = (df["precipitaciones"] > 0).astype(int)

# ===============================
# 4. Separar features y target
# ===============================
X = df.drop(columns=["lluvia"])
y = df["lluvia"]

# Dividir en train y test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Escalar (recomendado para LogisticRegression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ===============================
# 5. Modelos de clasificación
# ===============================
modelos = {
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
}

# ===============================
# 6. Entrenamiento y evaluación
# ===============================
resultados_modelos = []

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    # Métricas básicas
    report = classification_report(
        y_test, y_pred, target_names=["No Lluvia", "Lluvia"], output_dict=True
    )
    acc = accuracy_score(y_test, y_pred)
    precision = report["Lluvia"]["precision"]
    recall = report["Lluvia"]["recall"]
    f1 = report["Lluvia"]["f1-score"]

    # Probabilidades para ROC-AUC (si el modelo las ofrece)
    roc_auc = None
    if hasattr(modelo, "predict_proba"):
        y_prob = modelo.predict_proba(X_test)[:, 1]
        try:
            roc_auc = roc_auc_score(y_test, y_prob)
        except ValueError:
            roc_auc = None
    else:
        y_prob = None

    print(f"\nModelo: {nombre}")
    print(
        classification_report(
            y_test, y_pred, target_names=["No Lluvia", "Lluvia"], zero_division=0
        )
    )

    # Matriz de confusión numérica
    cm = confusion_matrix(y_test, y_pred)
    print("Matriz de confusión:\n", cm)

    # Matriz de confusión visual (heatmap)
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["No Lluvia", "Lluvia"],
        yticklabels=["No Lluvia", "Lluvia"],
    )
    plt.title(f"Matriz de Confusión - {nombre}")
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.show()

    # Barras de métricas por clase (precision, recall, f1 de clase 'Lluvia')
    plt.figure(figsize=(6, 4))
    plt.bar(
        ["Precision", "Recall", "F1"],
        [precision, recall, f1],
        color=["#1f77b4", "#ff7f0e", "#2ca02c"],
    )
    plt.ylim(0, 1)
    plt.title(f"Métricas clase 'Lluvia' - {nombre}")
    for i, v in enumerate([precision, recall, f1]):
        plt.text(i, v + 0.02, f"{v:.2f}", ha="center")
    plt.tight_layout()
    plt.show()

    # Curva ROC si hay probabilidades
    if y_prob is not None:
        RocCurveDisplay.from_predictions(y_test, y_prob)
        plt.title(f"Curva ROC - {nombre} (AUC={roc_auc:.3f})")
        plt.tight_layout()
        plt.show()

    resultados_modelos.append(
        {
            "modelo": nombre,
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "roc_auc": roc_auc,
        }
    )

# Resumen comparativo de modelos
if resultados_modelos:
    resumen_df = pd.DataFrame(resultados_modelos)
    print("\n=== RESUMEN COMPARATIVO ===")
    print(resumen_df)

    # Gráfico comparativo F1
    plt.figure(figsize=(6, 4))
    plt.bar(resumen_df["modelo"], resumen_df["f1"], color="#4c72b0")
    plt.ylim(0, 1)
    plt.ylabel("F1 (clase Lluvia)")
    plt.title("Comparación F1 por Modelo")
    for x, v in zip(resumen_df["modelo"], resumen_df["f1"]):
        plt.text(x, v + 0.02, f"{v:.2f}", ha="center")
    plt.tight_layout()
    plt.show()

    # Curva ROC múltiple si ambos tienen probas
    modelos_con_prob = [m for m in modelos if hasattr(modelos[m], "predict_proba")]
    if len(modelos_con_prob) > 1:
        plt.figure(figsize=(6, 5))
        for m in modelos_con_prob:
            probs = modelos[m].predict_proba(X_test)[:, 1]
            RocCurveDisplay.from_predictions(y_test, probs, name=m)
        plt.plot([0, 1], [0, 1], "k--")
        plt.title("Curvas ROC Comparativas")
        plt.tight_layout()
        plt.show()

# ===============================
# 7. Ejemplo de predicción
# ===============================
# print(df.columns)
# Crear un nuevo ejemplo (usa el mismo orden de columnas que X)
nuevo_dato = pd.DataFrame(
    [
        {
            "temperatura": 22.0,
            "precipitaciones": 0.0,
            "humedad_relativa": 0.58,
            "velocidad_viento": 4.0,
            "rafaga_viento": 4.0,
            "angulo_viento": 124,
            "nubosidad": 0.54,
            "visibilidad": 10,
            "hora": 15,
            "mes": 9,
            "dia_semana": 0,
        }
    ]
)

# Asegurar que tenga las mismas columnas
nuevo_dato = nuevo_dato[X.columns]

# Escalar y predecir
nuevo_dato_scaled = scaler.transform(nuevo_dato)
prediccion = modelos["Random Forest"].predict(nuevo_dato_scaled)
print("\n¿Lloverá?:", "Sí" if prediccion[0] == 1 else "No")
