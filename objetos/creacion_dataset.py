import csv
import random

# Configuración para cada tipo de objeto
objetos_config = {
    "cana_basica": {
        "rareza": (1, 2),
        "nivel_requerido": (1, 15),
        "precio_venta": 4,
        "porcentaje_completado": (0, 1),
        "valor_estrategico": (1, 2),
    },
    "cana_rara": {
        "rareza": (2, 3),
        "nivel_requerido": (10, 40),
        "precio_venta": 16,
        "porcentaje_completado": (1, 2),
        "valor_estrategico": (2, 4),
    },
    "cana_epica": {
        "rareza": (3, 4),
        "nivel_requerido": (30, 60),
        "precio_venta": 64,
        "porcentaje_completado": (2, 3),
        "valor_estrategico": (4, 8),
    },
    "cana_legendaria": {
        "rareza": (4, 5),
        "nivel_requerido": (50, 100),
        "precio_venta": 256,
        "porcentaje_completado": 3,  # Valor fijo
        "valor_estrategico": (8, 8),
    },
    "anillas_sixpack": {
        "rareza": (1, 2),
        "nivel_requerido": (1, 100),
        "precio_venta": 0,
        "porcentaje_completado": (0, 1),
        "valor_estrategico": (-1, 0),
    },
    "botella": {
        "rareza": (2, 3),
        "nivel_requerido": (1, 100),
        "precio_venta": 0,
        "porcentaje_completado": (0, 1),
        "valor_estrategico": (-2, -1),
    },
    "lata": {
        "rareza": (3, 4),
        "nivel_requerido": (1, 100),
        "precio_venta": 0,
        "porcentaje_completado": (0, 1),
        "valor_estrategico": (-3, -2),
    },
    "llanta": {
        "rareza": (4, 5),
        "nivel_requerido": (1, 100),
        "precio_venta": 0,
        "porcentaje_completado": (0, 1),
        "valor_estrategico": (-4, -3),
    },
    "tesoro": {
        "rareza": (5, 5),
        "nivel_requerido": (1, 100),
        "precio_venta": 170,
        "porcentaje_completado": (2, 3),
        "valor_estrategico": (10, 10),
    },
}

# Número de registros por cada tipo de objeto
NUM_REGISTROS_POR_TIPO = 500

# Generar el dataset
datos = []

for tipo_objeto, config in objetos_config.items():
    for _ in range(NUM_REGISTROS_POR_TIPO):
        # Generar rareza
        if isinstance(config["rareza"], tuple):
            rareza_min, rareza_max = config["rareza"]
            rareza = random.randint(rareza_min, rareza_max)
        else:
            rareza = config["rareza"]

        # Generar nivel_requerido
        nivel_min, nivel_max = config["nivel_requerido"]
        nivel_requerido = random.randint(nivel_min, nivel_max)

        # Generar porcentaje_completado
        if isinstance(config["porcentaje_completado"], tuple):
            pc_min, pc_max = config["porcentaje_completado"]
            porcentaje_completado = random.randint(pc_min, pc_max)
        else:
            porcentaje_completado = config["porcentaje_completado"]

        # Generar valor_estrategico
        if isinstance(config["valor_estrategico"], tuple):
            ve_min, ve_max = config["valor_estrategico"]
            valor_estrategico = random.randint(ve_min, ve_max)
        else:
            valor_estrategico = config["valor_estrategico"]

        # Crear el registro
        registro = {
            "tipo_objeto": tipo_objeto,
            "rareza": rareza,
            "nivel_requerido": nivel_requerido,
            "precio_venta": config["precio_venta"],
            "porcentaje_completado": porcentaje_completado,
            "valor_estrategico": valor_estrategico,
        }

        datos.append(registro)

# Mezclar los datos para que no estén ordenados por tipo
random.shuffle(datos)

# Guardar en CSV
with open("dataset.csv", "w", newline="", encoding="utf-8") as archivo:
    campos = [
        "tipo_objeto",
        "rareza",
        "nivel_requerido",
        "precio_venta",
        "porcentaje_completado",
        "valor_estrategico",
    ]
    escritor = csv.DictWriter(archivo, fieldnames=campos)

    escritor.writeheader()
    escritor.writerows(datos)

print(f"Dataset generado exitosamente con {len(datos)} registros")
print(f"Registros por tipo de objeto: {NUM_REGISTROS_POR_TIPO}")
