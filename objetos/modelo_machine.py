import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import warnings

warnings.filterwarnings("ignore")

# Cargar el dataset
print("=" * 80)
print("CARGANDO DATASET")
print("=" * 80)
df = pd.read_csv("dataset.csv")
print(f"\nDataset cargado: {df.shape[0]} registros, {df.shape[1]} columnas")
print(f"\nDistribución de clases:")
print(df["tipo_objeto"].value_counts())
print(f"\nPrimeras filas del dataset:")
print(df.head())

# Separar características (X) y etiquetas (y)
X = df.drop("tipo_objeto", axis=1)
y = df["tipo_objeto"]

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nConjunto de entrenamiento: {X_train.shape[0]} registros")
print(f"Conjunto de prueba: {X_test.shape[0]} registros")

# Crear gráfica de dispersión del dataset
print("\n" + "=" * 80)
print("GENERANDO GRÁFICAS DE DISPERSIÓN")
print("=" * 80)

# Crear carpeta para gráficas si no existe
if not os.path.exists("graficas"):
    os.makedirs("graficas")
    print("Carpeta 'graficas' creada")

# Configurar el estilo
sns.set_style("whitegrid")

# Crear figura con subplots
fig = plt.figure(figsize=(20, 12))

# Lista de características numéricas
caracteristicas = [
    "rareza",
    "nivel_requerido",
    "precio_venta",
    "porcentaje_completado",
    "valor_estrategico",
]

# Crear gráficas de dispersión para combinaciones de características
combinaciones = [
    ("rareza", "nivel_requerido"),
    ("rareza", "precio_venta"),
    ("nivel_requerido", "porcentaje_completado"),
    ("precio_venta", "valor_estrategico"),
    ("porcentaje_completado", "valor_estrategico"),
    ("rareza", "porcentaje_completado"),
]

for idx, (feat1, feat2) in enumerate(combinaciones, 1):
    ax = plt.subplot(2, 3, idx)

    # Crear gráfica de dispersión coloreada por tipo de objeto
    for tipo in sorted(df["tipo_objeto"].unique()):
        datos_tipo = df[df["tipo_objeto"] == tipo]
        ax.scatter(
            datos_tipo[feat1],
            datos_tipo[feat2],
            label=tipo,
            alpha=0.6,
            s=50,
            edgecolors="black",
            linewidth=0.5,
        )

    ax.set_xlabel(feat1.replace("_", " ").title(), fontsize=11, fontweight="bold")
    ax.set_ylabel(feat2.replace("_", " ").title(), fontsize=11, fontweight="bold")
    ax.set_title(
        f"{feat1.replace('_', ' ').title()} vs {feat2.replace('_', ' ').title()}",
        fontsize=12,
        fontweight="bold",
    )
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("graficas/dispersion_dataset.png", dpi=300, bbox_inches="tight")
print("Gráfica de dispersión guardada como 'graficas/dispersion_dataset.png'")
plt.close()

# Crear una gráfica de dispersión 3D adicional
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection="3d")

# Crear un mapa de colores para cada tipo de objeto
tipos_unicos = sorted(df["tipo_objeto"].unique())
colores_map = plt.cm.tab10(np.linspace(0, 1, len(tipos_unicos)))

for idx, tipo in enumerate(tipos_unicos):
    datos_tipo = df[df["tipo_objeto"] == tipo]
    ax.scatter(
        datos_tipo["rareza"],
        datos_tipo["nivel_requerido"],
        datos_tipo["precio_venta"],
        c=[colores_map[idx]],
        label=tipo,
        alpha=0.6,
        s=50,
        edgecolors="black",
        linewidth=0.5,
    )

ax.set_xlabel("Rareza", fontsize=12, fontweight="bold")
ax.set_ylabel("Nivel Requerido", fontsize=12, fontweight="bold")
ax.set_zlabel("Precio Venta", fontsize=12, fontweight="bold")
ax.set_title(
    "Dispersión 3D: Rareza vs Nivel Requerido vs Precio Venta",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
ax.legend(loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig("graficas/dispersion_3d_dataset.png", dpi=300, bbox_inches="tight")
print("Gráfica de dispersión 3D guardada como 'graficas/dispersion_3d_dataset.png'")
plt.close()

# Definir los clasificadores
clasificadores = {
    "Regresión Logística": LogisticRegression(max_iter=1000, random_state=42),
    "SVM": SVC(kernel="rbf", random_state=42),
    "Árbol de Decisión": DecisionTreeClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "MLP Básico": MLPClassifier(
        hidden_layer_sizes=(100,), max_iter=1000, random_state=42
    ),
}

# Almacenar resultados
resultados = []

# Entrenar y evaluar cada clasificador
for nombre, clasificador in clasificadores.items():
    print("\n" + "=" * 80)
    print(f"ENTRENANDO: {nombre}")
    print("=" * 80)

    # Entrenar el modelo
    clasificador.fit(X_train, y_train)
    print("Modelo entrenado")

    # Realizar predicciones
    y_pred = clasificador.predict(X_test)

    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    # Guardar resultados
    resultados.append(
        {
            "Clasificador": nombre,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1,
        }
    )

    # Mostrar métricas
    print(f"\nMétricas de {nombre}:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")

    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=sorted(y.unique()),
        yticklabels=sorted(y.unique()),
    )
    plt.title(f"Matriz de Confusión - {nombre}")
    plt.ylabel("Valor Real")
    plt.xlabel("Valor Predicho")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(
        f"graficas/confusion_matrix_{nombre.replace(' ', '_').lower()}.png", dpi=300
    )
    plt.close()
    print(f"Matriz de confusión guardada")

    # Reporte de clasificación detallado
    print(f"\nReporte de clasificación:")
    print(classification_report(y_test, y_pred, zero_division=0))

# Crear DataFrame con resultados
df_resultados = pd.DataFrame(resultados)
df_resultados = df_resultados.sort_values("F1-Score", ascending=False)

# Mostrar tabla comparativa
print("\n" + "=" * 80)
print("COMPARACIÓN DE CLASIFICADORES")
print("=" * 80)
print("\n" + df_resultados.to_string(index=False))

# Identificar el mejor clasificador
mejor_clasificador = df_resultados.iloc[0]
print("\n" + "=" * 80)
print("MEJOR CLASIFICADOR")
print("=" * 80)
print(f"\n{mejor_clasificador['Clasificador']}")
print(f"   Accuracy:  {mejor_clasificador['Accuracy']:.4f}")
print(f"   Precision: {mejor_clasificador['Precision']:.4f}")
print(f"   Recall:    {mejor_clasificador['Recall']:.4f}")
print(f"   F1-Score:  {mejor_clasificador['F1-Score']:.4f}")

# Crear gráfico comparativo
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
metricas = ["Accuracy", "Precision", "Recall", "F1-Score"]
colores = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]

for idx, metrica in enumerate(metricas):
    ax = axes[idx // 2, idx % 2]
    df_resultados_sorted = df_resultados.sort_values(metrica, ascending=True)

    bars = ax.barh(
        df_resultados_sorted["Clasificador"],
        df_resultados_sorted[metrica],
        color=colores[idx],
    )

    # Añadir valores en las barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(
            width,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.4f}",
            ha="left",
            va="center",
            fontweight="bold",
        )

    ax.set_xlabel(metrica, fontsize=12, fontweight="bold")
    ax.set_title(f"Comparación de {metrica}", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 1.1)
    ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig("graficas/comparacion_clasificadores.png", dpi=300, bbox_inches="tight")
print("\nGráfico comparativo guardado como 'graficas/comparacion_clasificadores.png'")


print("\n" + "=" * 80)
print("PROCESO COMPLETADO")
print("=" * 80)
