import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import datetime
import time

# import requests

# --- Cargar y preparar datos históricos ---
df = pd.read_csv("regresion_clima/dataset_clima_76680.csv", sep=",")
df = df[[col for col in df.columns if not col.endswith("_source")]]

df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
df["day_of_year"] = df["datetime"].dt.dayofyear
df["year_scaled"] = (df["year"] - df["year"].min()) / (
    df["year"].max() - df["year"].min()
)
df["weekday"] = df["datetime"].dt.weekday
df["sin_week"] = np.sin(2 * np.pi * df["weekday"] / 7)
df["cos_week"] = np.cos(2 * np.pi * df["weekday"] / 7)
df["day_of_month"] = df["datetime"].dt.day
df["sin_day"] = np.sin(2 * np.pi * df["day_of_month"] / 31)
df["cos_day"] = np.cos(2 * np.pi * df["day_of_month"] / 31)
df["sin_year"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
df["cos_year"] = np.cos(2 * np.pi * df["day_of_year"] / 365)
df["sin_hour"] = np.sin(2 * np.pi * df["hour"] / 24)
df["cos_hour"] = np.cos(2 * np.pi * df["hour"] / 24)

X = df[
    [
        "sin_year",
        "cos_year",
        "sin_hour",
        "cos_hour",
        "sin_week",
        "cos_week",
        "sin_day",
        "cos_day",
        "year_scaled",
    ]
]
y = df["temp"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# model = HistGradientBoostingRegressor(
#     learning_rate=0.03, max_iter=800, max_depth=10, min_samples_leaf=5, random_state=42
# )
model = ExtraTreesRegressor(
    n_estimators=200, max_depth=15, min_samples_leaf=3, random_state=42
)
# model = SVR(kernel="rbf", C=1.0, epsilon=0.1)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R²: {r2:.3f}")


# --- Función para preparar fecha/hora como antes ---
def preparar_fecha(year, month, day, hour):
    day_of_year = pd.Timestamp(year=year, month=month, day=day).day_of_year
    sin_year = np.sin(2 * np.pi * day_of_year / 365)
    cos_year = np.cos(2 * np.pi * day_of_year / 365)
    sin_hour = np.sin(2 * np.pi * hour / 24)
    cos_hour = np.cos(2 * np.pi * hour / 24)

    weekday = pd.Timestamp(year=year, month=month, day=day).weekday()
    sin_week = np.sin(2 * np.pi * weekday / 7)
    cos_week = np.cos(2 * np.pi * weekday / 7)
    day_of_month = pd.Timestamp(year=year, month=month, day=day).day
    sin_day = np.sin(2 * np.pi * day_of_month / 31)
    cos_day = np.cos(2 * np.pi * day_of_month / 31)

    year_min = df["year"].min()
    year_max = df["year"].max()
    if year_max > year_min:
        year_scaled = (year - year_min) / (year_max - year_min)
    else:
        year_scaled = 0.0

    row = {
        "sin_year": sin_year,
        "cos_year": cos_year,
        "sin_hour": sin_hour,
        "cos_hour": cos_hour,
        "sin_week": sin_week,
        "cos_week": cos_week,
        "sin_day": sin_day,
        "cos_day": cos_day,
        "year_scaled": year_scaled,
    }
    df_row = pd.DataFrame([row])
    return df_row.reindex(columns=X.columns, fill_value=0.0)


# # --- Función para obtener datos actuales de la API para CDMX ---
# def obtener_datos_api(lat=19.4326, lon=-99.1332):
#     url = (
#         f"https://api.open-meteo.com/v1/forecast?"
#         f"latitude={lat}&longitude={lon}&current_weather=true"
#         f"&hourly=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m"
#     )
#     resp = requests.get(url)
#     data = resp.json()
#     current = data.get("current_weather", {})
#     # algunas versiones de API usan "current" o "current_weather"
#     temp_api = current.get("temperature") or current.get("temperature_2m")
#     rhum_api = None
#     pres_api = None
#     wspd_api = None
#     # No todas las variables estarán en current_weather — tal vez estén en hourly
#     # Aquí hacemos un fallback sencillo:
#     hourly = data.get("hourly", {})
#     if rhum_api is None:
#         rhum_vals = hourly.get("relative_humidity_2m")
#         if rhum_vals:
#             rhum_api = rhum_vals[0]
#     if pres_api is None:
#         pres_vals = hourly.get("pressure_msl")
#         if pres_vals:
#             pres_api = pres_vals[0]
#     if wspd_api is None:
#         wspd_vals = hourly.get("wind_speed_10m")
#         if wspd_vals:
#             wspd_api = wspd_vals[0]

#     return {
#         "temp_api": temp_api,
#         "rhum_api": rhum_api,
#         "pres_api": pres_api,
#         "wspd_api": wspd_api,
#     }


print("\nIniciando actualización automática cada minuto (Ctrl + C para detener)...\n")

while True:
    now = datetime.datetime.now()
    year, month, day, hour = now.year, now.month, now.day, now.hour

    X_live = preparar_fecha(year, month, day, hour)  # Ajuste de zona horaria
    pred_temp = model.predict(X_live)[0]

    # api_data = obtener_datos_api()
    # temp_api = api_data["temp_api"]

    # if temp_api is not None:
    #     # Ajuste: mezcla tu predicción con la medición actual de la API
    #     ajuste = (temp_api - pred_temp) * 0.85  # factor 0.5 = 50% de la diferencia
    #     pred_final = pred_temp + ajuste
    # else:
    #     pred_final = pred_temp

    print(
        f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Predicción de la temperatura: {pred_temp:.2f} °C"
        # f"API actual: {temp_api:.2f} °C"
    )

    time.sleep(60)
