import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
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

# Features de la fecha (opcionales pero útiles)
df["hora"] = df["fecha_hora"].dt.hour
df["mes"] = df["fecha_hora"].dt.month
df["dia_semana"] = df["fecha_hora"].dt.dayofweek

# Eliminar columnas que no sirven directamente
df = df.drop(columns=["fecha_hora", "direccion_viento"])

# Reemplazar comas decimales por puntos (muy importante)
df = df.replace(",", ".", regex=True)

# Intentar convertir todo a número (si algo no se puede → NaN)
for col in df.columns:
    if col != "clima":  # excepto el target
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Rellenar posibles NaN con la media de la columna
df = df.fillna(df.mean(numeric_only=True))

# ===============================
# 3. Separar features y target
# ===============================
X = df.drop(columns=["clima"])
y = df["clima"]

# Codificar target a números
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# ===============================
# 4. Dividir en train y test
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Escalado de datos (NO es obligatorio para RandomForest,
# pero sí ayuda en SVM, MLP, LogisticRegression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ===============================
# 5. Definir y entrenar modelos
# ===============================
modelos = {
    "Random Forest": RandomForestClassifier(
        n_estimators=200, max_depth=15, random_state=42
    ),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(kernel="rbf", probability=True),
    "MLP": MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42),
}

# ===============================
# 6. Evaluación de modelos
# ===============================
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    print(f"\nModelo: {nombre}")
    # Reporte textual
    print(
        classification_report(
            y_test,
            y_pred,
            labels=range(len(encoder.classes_)),
            target_names=encoder.classes_,
            zero_division=0,
        )
    )

    # Reporte estructurado para extraer métricas por clase
    report_dict = classification_report(
        y_test,
        y_pred,
        labels=range(len(encoder.classes_)),
        target_names=encoder.classes_,
        zero_division=0,
        output_dict=True,
    )

    # Matriz de confusión (gráfica)
    cm = confusion_matrix(y_test, y_pred, labels=range(len(encoder.classes_)))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=encoder.classes_)
    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(cmap="Blues", ax=ax, colorbar=True)
    plt.title(f"Matriz de Confusión - {nombre}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # F1 por clase (barras)
    class_f1 = {
        cls: report_dict[cls]["f1-score"]
        for cls in encoder.classes_
        if cls in report_dict
    }
    plt.figure(figsize=(8, 4))
    plt.bar(class_f1.keys(), class_f1.values(), color="#1f77b4")
    plt.ylabel("F1-score")
    plt.ylim(0, 1)
    plt.title(f"F1 por Clase - {nombre}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # Macro y weighted F1 destacados
    macro_f1 = report_dict.get("macro avg", {}).get("f1-score", float("nan"))
    weighted_f1 = report_dict.get("weighted avg", {}).get("f1-score", float("nan"))
    print(f"Macro F1: {macro_f1:.4f} | Weighted F1: {weighted_f1:.4f}")

# ===============================
# 7. Importancia de variables (solo Random Forest)
# ===============================
rf = modelos["Random Forest"]
importances = rf.feature_importances_
features = X.columns

plt.figure(figsize=(10, 5))
plt.barh(features, importances)
plt.xlabel("Importancia")
plt.title("Importancia de las variables en la predicción del clima")
plt.show()
