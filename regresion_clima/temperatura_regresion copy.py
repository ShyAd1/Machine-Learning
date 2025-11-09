import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import (
    LinearRegression,
    BayesianRidge,
    Ridge,
    Lasso,
    ElasticNet,
    HuberRegressor,
)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
    AdaBoostRegressor,
    HistGradientBoostingRegressor,
)
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
import matplotlib.pyplot as plt

# ===============================
# 1. Cargar dataset
# ===============================
df = pd.read_csv(
    "regresion_clima/dataset_clima.csv", sep=","
)  # usa sep="," si es CSV normal

# ===============================
# 2. Limpieza de datos
# ===============================

# Eliminar columnas que terminan en "_source"
df = df[[col for col in df.columns if not col.endswith("_source")]]

# Rellenar valores faltantes con la media
df = df.fillna(df.mean(numeric_only=True))

# ===============================
# 3. Separar variables
# ===============================
X = df.drop(columns=["temp"])  # características (sin la temperatura)
y = df["temp"]  # variable objetivo

# ===============================
# 4. División de datos (sin mezclar orden temporal)
# ===============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Escalado (solo para modelos sensibles a escala)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===============================
# 5. Modelos
# ===============================
modelos = {
    "LinearRegression": LinearRegression(),
    "BayesianRidge": BayesianRidge(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "ElasticNet": ElasticNet(),
    "Huber": HuberRegressor(max_iter=1000),
    "KNN": KNeighborsRegressor(n_neighbors=15, weights="distance"),
    "DecisionTree": DecisionTreeRegressor(random_state=42),
    "RandomForest": RandomForestRegressor(n_estimators=300, random_state=42),
    "ExtraTrees": ExtraTreesRegressor(n_estimators=400, random_state=42, n_jobs=-1),
    "AdaBoost": AdaBoostRegressor(random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
    "HistGradientBoosting": HistGradientBoostingRegressor(random_state=42),
    "SVR_rbf": SVR(kernel="rbf", C=1.0, epsilon=0.1),
}

resultados = []
# Configuración de gráficos: muestra ventanas por defecto
SAVE_PLOTS = False  # pon True si prefieres guardar a archivos en regresion_clima/plots
PLOTS_DIR = os.path.join("regresion_clima", "plots")
if SAVE_PLOTS:
    os.makedirs(PLOTS_DIR, exist_ok=True)

scaled_models = {
    "LinearRegression",
    "BayesianRidge",
    "Ridge",
    "Lasso",
    "ElasticNet",
    "Huber",
    "KNN",
    "SVR_rbf",
}

for nombre, modelo in modelos.items():
    if nombre in scaled_models:
        Xtr, Xte = X_train_scaled, X_test_scaled
    else:
        Xtr, Xte = X_train, X_test

    modelo.fit(Xtr, y_train)
    y_pred = modelo.predict(Xte)

    # Métricas
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    resultados.append({"modelo": nombre, "MAE": mae, "RMSE": rmse, "R2": r2})

    # Gráfico Real vs Predicho
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(y_test, y_pred, alpha=0.6)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lims, lims, "r--")
    ax.set_title(f"Real vs Predicho - {nombre}")
    ax.set_xlabel("Temperatura Real (°C)")
    ax.set_ylabel("Predicha (°C)")
    fig.tight_layout()
    if SAVE_PLOTS:
        fig.savefig(
            os.path.join(PLOTS_DIR, f"scatter_{nombre}.png"),
            dpi=120,
            bbox_inches="tight",
        )
        plt.close(fig)
    else:
        # Mostrar de forma bloqueante; cierra manualmente la ventana para continuar al siguiente modelo
        plt.show()

# ===============================
# 6. Resultados comparativos
# ===============================
res_df = pd.DataFrame(resultados).sort_values(by="RMSE")
print("\n=== RESULTADOS COMPARATIVOS ===")
print(res_df.to_string(index=False))

# ===============================
# 7. Ejemplo de predicción
# ===============================
mejor_nombre = res_df.iloc[0]["modelo"]
mejor_modelo = modelos[mejor_nombre]
print(f"\nMejor modelo según RMSE: {mejor_nombre}")

nuevo_dato_actual = X.iloc[-1].copy()

# Sobrescribe solo los campos que conozcas (ejemplo CDMX)
nuevo_dato_actual.update(
    pd.Series(
        {
            "year": 2025,
            "month": 11,
            "day": 8,
            "hour": 14,
            "rhum": 16,  # humedad relativa %
            "prcp": 0.0,  # precipitación mm
            "wdir": 16,  # dirección viento grados
            "wspd": 6,  # velocidad viento km/h
            "pres": 1011,  # presión hPa
            "cldc": 4,  # nubosidad 0-8
            "coco": 3,  # código de condición climática
        }
    )
)

# Asegurar formato correcto para predict
df_actual = pd.DataFrame([nuevo_dato_actual.values], columns=X.columns)

if mejor_nombre in scaled_models:
    df_actual_scaled = scaler.transform(df_actual)
    prediccion_actual = mejor_modelo.predict(df_actual_scaled)
else:
    prediccion_actual = mejor_modelo.predict(df_actual)

print(f"Temperatura estimada actual: {prediccion_actual[0]:.2f} °C")

# ===============================
# 8. Variante: modelado solo con fecha/hora
# ===============================
# Creamos variables temporales cíclicas: month_sin/cos, hour_sin/cos y dayofyear_sin/cos (si existe fecha)


def add_time_cyclic_features(df_in):
    df_feat = pd.DataFrame(index=df_in.index)
    # Month
    if "month" in df_in.columns:
        m = df_in["month"].astype(int)
        df_feat["month_sin"] = np.sin(2 * np.pi * m / 12)
        df_feat["month_cos"] = np.cos(2 * np.pi * m / 12)
    # Hour
    if "hour" in df_in.columns:
        h = df_in["hour"].astype(int)
        df_feat["hour_sin"] = np.sin(2 * np.pi * h / 24)
        df_feat["hour_cos"] = np.cos(2 * np.pi * h / 24)
    # Day (si tienes day o dayofyear)
    if "day" in df_in.columns:
        d = df_in["day"].astype(int)
        df_feat["day_sin"] = np.sin(2 * np.pi * d / 31)
        df_feat["day_cos"] = np.cos(2 * np.pi * d / 31)
    if "dayofyear" in df_in.columns:
        doy = df_in["dayofyear"].astype(int)
        df_feat["doy_sin"] = np.sin(2 * np.pi * doy / 366)
        df_feat["doy_cos"] = np.cos(2 * np.pi * doy / 366)
    return df_feat


# Construir dataset solo temporal
X_time = add_time_cyclic_features(X)
Xtr_t, Xte_t, ytr_t, yte_t = train_test_split(X_time, y, test_size=0.2, shuffle=False)

scaler_t = StandardScaler()
Xtr_t_sc = scaler_t.fit_transform(Xtr_t)
Xte_t_sc = scaler_t.transform(Xte_t)

modelos_t = {
    "LinearRegression": LinearRegression(),
    "BayesianRidge": BayesianRidge(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "ElasticNet": ElasticNet(),
    "Huber": HuberRegressor(max_iter=1000),
    "KNN": KNeighborsRegressor(n_neighbors=15, weights="distance"),
    "SVR_rbf": SVR(kernel="rbf", C=1.0, epsilon=0.1),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
    "HistGradientBoosting": HistGradientBoostingRegressor(random_state=42),
}

scaled_models_t = {
    "LinearRegression",
    "BayesianRidge",
    "Ridge",
    "Lasso",
    "ElasticNet",
    "Huber",
    "KNN",
    "SVR_rbf",
}

resultados_t = []
for nombre, modelo in modelos_t.items():
    if nombre in scaled_models_t:
        Xtr_u, Xte_u = Xtr_t_sc, Xte_t_sc
    else:
        Xtr_u, Xte_u = Xtr_t, Xte_t
    modelo.fit(Xtr_u, ytr_t)
    ypred_t = modelo.predict(Xte_u)
    mse = mean_squared_error(yte_t, ypred_t)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(yte_t, ypred_t)
    r2 = r2_score(yte_t, ypred_t)
    resultados_t.append({"modelo": nombre, "MAE": mae, "RMSE": rmse, "R2": r2})

res_time_df = pd.DataFrame(resultados_t).sort_values(by="RMSE")
print("\n=== MODELOS SOLO CON FECHA/HORA (ordenados por RMSE) ===")
print(res_time_df.to_string(index=False))

best_time_name = res_time_df.iloc[0]["modelo"]
best_time_model = modelos_t[best_time_name]
print(f"Mejor modelo (time-only): {best_time_name}")


def predict_with_datetime(year, month, day, hour):
    # Construir fila temporal
    s = pd.Series(dtype=float)
    # Si existen, usa estas columnas crudas para crear las cíclicas
    base = {}
    if "month" in X.columns:
        base["month"] = month
    if "hour" in X.columns:
        base["hour"] = hour
    if "day" in X.columns:
        base["day"] = day
    if "dayofyear" in X.columns:
        # Si tienes dayofyear en X, calcula aquí si lo deseas
        import datetime as _dt

        base["dayofyear"] = int(_dt.date(year, month, day).timetuple().tm_yday)
    df_tmp = pd.DataFrame([base])
    feats = add_time_cyclic_features(df_tmp)
    feats = feats.reindex(columns=X_time.columns, fill_value=0.0)
    # Escalar si corresponde al mejor modelo temporal
    if best_time_name in scaled_models_t:
        feats_sc = scaler_t.transform(feats)
        return best_time_model.predict(feats_sc)
    else:
        return best_time_model.predict(feats)


pred_time_only = predict_with_datetime(2025, 10, 19, 23)
print(f"Predicción SOLO con fecha/hora: {pred_time_only[0]:.2f} °C")
