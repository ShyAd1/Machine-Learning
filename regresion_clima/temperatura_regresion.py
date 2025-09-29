import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# ===============================
# 1. Cargar dataset
# ===============================
df = pd.read_csv("clima_cdmx_dataset_copia.csv")

# Convertir fecha
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], dayfirst=True)
df["hora"] = df["fecha_hora"].dt.hour
df["mes"] = df["fecha_hora"].dt.month
df["dia_semana"] = df["fecha_hora"].dt.dayofweek

# Eliminar columnas irrelevantes
df = df.drop(columns=["fecha_hora", "direccion_viento", "clima"])

# Convertir decimales con coma a punto y a numérico
df = df.replace(",", ".", regex=True).apply(pd.to_numeric, errors="coerce")
df = df.fillna(df.mean(numeric_only=True))

# ===============================
# 2. Variables X y target y
# ===============================
X = df.drop(columns=["temperatura"])
y = df["temperatura"]

# ===============================
# 3. Train/Test split (sin shuffle para mantener orden temporal si lo hay)
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===============================
# 4. Modelos de regresión
# ===============================
modelos = {
    "LinearRegression": LinearRegression(),
    "BayesianRidge": BayesianRidge(),
    "RandomForest": RandomForestRegressor(
        n_estimators=400, max_depth=18, random_state=42, n_jobs=-1
    ),
    "SVR_rbf": SVR(kernel="rbf", C=1.0, epsilon=0.1),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
}

resultados = []
figuras_scatter = []
figuras_residuos = []

for nombre, modelo in modelos.items():
    # Elegir datos escalados sólo para los modelos lineales / sensibles a escala
    if nombre in ["LinearRegression", "BayesianRidge", "SVR_rbf"]:
        Xtr, Xte = X_train_scaled, X_test_scaled
    else:
        Xtr, Xte = X_train, X_test  # árboles y boosting no necesitan escalado

    modelo.fit(Xtr, y_train)
    y_pred = modelo.predict(Xte)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    resultados.append(
        {
            "modelo": nombre,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        }
    )

    # Scatter Real vs Predicho
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.scatter(y_test, y_pred, alpha=0.6)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax1.plot(lims, lims, "r--")
    ax1.set_title(f"Real vs Predicho - {nombre}")
    ax1.set_xlabel("Real")
    ax1.set_ylabel("Predicho")
    fig1.tight_layout()
    plt.show()

    # Residuos
    resid = y_test - y_pred
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.hist(resid, bins=20, alpha=0.75, color="#1f77b4")
    ax2.set_title(f"Residuos - {nombre}")
    ax2.set_xlabel("Residuo")
    ax2.set_ylabel("Frecuencia")
    fig2.tight_layout()
    plt.show()

# ===============================
# 5. Resumen comparativo
# ===============================
res_df = pd.DataFrame(resultados).sort_values(by="RMSE")
print("\n=== RESULTADOS COMPARATIVOS (ordenados por RMSE) ===")
print(res_df.to_string(index=False))

# Barras comparativas de RMSE / MAE / R2
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
res_df.plot(x="modelo", y="RMSE", kind="bar", ax=axes[0], color="#d62728", legend=False)
axes[0].set_title("RMSE")
axes[0].set_ylabel("RMSE")
res_df.plot(x="modelo", y="MAE", kind="bar", ax=axes[1], color="#ff7f0e", legend=False)
axes[1].set_title("MAE")
res_df.plot(x="modelo", y="R2", kind="bar", ax=axes[2], color="#2ca02c", legend=False)
axes[2].set_title("R2")
axes[2].set_ylim(0, 1)
for ax in axes:
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.2f}",
            (p.get_x() + p.get_width() / 2, p.get_height() + 0.01),
            ha="center",
            fontsize=8,
        )
fig.suptitle("Comparativa de Modelos")
plt.tight_layout()
plt.show()

# ===============================
# 6. Elegir mejor modelo para ejemplo de predicción (menor RMSE)
# ===============================
mejor_nombre = res_df.iloc[0]["modelo"]
mejor_modelo = modelos[mejor_nombre]
print(f"\nMejor modelo según RMSE: {mejor_nombre}")

# Asegurar que esté entrenado (ya lo está, pero por claridad)
if mejor_nombre in ["LinearRegression", "BayesianRidge", "SVR_rbf"]:
    mejor_modelo.fit(X_train_scaled, y_train)
    X_ref = X_train_scaled
else:
    mejor_modelo.fit(X_train, y_train)
    X_ref = X_train

# ===============================
# 7. Predicción ejemplo
# ===============================
# Construir un nuevo ejemplo (usar columnas de X en el mismo orden)
nuevo_dato = pd.DataFrame(
    [{col: X.iloc[-1][col] for col in X.columns}]  # copia última fila como plantilla
)
# Puedes modificar algún valor manualmente aquí si deseas:
# nuevo_dato['hora'] = 7

# Escalar según corresponda
if mejor_nombre in ["LinearRegression", "BayesianRidge", "SVR_rbf"]:
    nuevo_dato_scaled = scaler.transform(nuevo_dato)
    prediccion = mejor_modelo.predict(nuevo_dato_scaled)
else:
    prediccion = mejor_modelo.predict(nuevo_dato)

print(
    "Temperatura predicha (ejemplo basado en última fila modificable):", prediccion[0]
)
