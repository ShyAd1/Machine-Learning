# --- Juego 20Q usando árbol de decisiones en JSON ---
# El árbol se guarda y carga automáticamente para permitir aprendizaje.

import json
import os


# Guarda el árbol de decisiones en un archivo JSON
def guardar_arbol(arbol, archivo="arbol_20q.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(arbol, f, ensure_ascii=False, indent=2)


# Carga el árbol de decisiones desde un archivo JSON, si existe
def cargar_arbol(archivo="arbol_20q.json"):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


# Función principal del juego: recorre el árbol según las respuestas del usuario
# Si llega a una hoja y falla, aprende una nueva pregunta y respuesta
def jugar20Q(nodo, padre=None, rama=None):
    # Si es una hoja (no tiene ramas "si" ni "no")
    if "si" not in nodo and "no" not in nodo:
        respuesta = input(f"{nodo['pregunta']} (sí/no): ").strip().lower()
        if respuesta.startswith("s"):
            print("¡Genial, adiviné!")
        else:
            print("¡Oh no! No lo adiviné.")
            # Aprendizaje: pide la respuesta correcta y una pregunta para distinguir
            nueva_respuesta = input("¿Qué era lo que pensabas?: ").strip()
            nueva_pregunta = input(
                f"Escribe una pregunta para distinguir '{nueva_respuesta}' de '{nodo['pregunta']}': "
            ).strip()
            respuesta_si = (
                input(
                    f"Para '{nueva_respuesta}', ¿la respuesta a la pregunta sería sí?: (sí/no): "
                )
                .strip()
                .lower()
            )
            # Inserta el nuevo conocimiento en el árbol
            if respuesta_si.startswith("s"):
                nuevo_nodo = {
                    "pregunta": nueva_pregunta,
                    "si": {"pregunta": nueva_respuesta},
                    "no": nodo,
                }
            else:
                nuevo_nodo = {
                    "pregunta": nueva_pregunta,
                    "si": nodo,
                    "no": {"pregunta": nueva_respuesta},
                }
            if padre and rama:
                padre[rama] = nuevo_nodo
            else:
                global arbol
                arbol = nuevo_nodo
            guardar_arbol(arbol)
        return

    # Si no es hoja, sigue preguntando según la respuesta
    respuesta = input(f"{nodo['pregunta']} (sí/no): ").strip().lower()
    if respuesta.startswith("s"):
        jugar20Q(nodo["si"], nodo, "si")
    else:
        jugar20Q(nodo["no"], nodo, "no")


# Carga el árbol desde archivo, o usa un árbol de ejemplo si no existe
arbol = cargar_arbol()
if not arbol:
    arbol = {
        "pregunta": "¿Es un objeto físico?",
        "si": {
            "pregunta": "¿Está vivo?",
            "si": {
                "pregunta": "¿Es un animal?",
                "si": {"pregunta": "Estas pensando en un animal."},
                "no": {"pregunta": "Estas pensando en una planta."},
            },
            "no": {"pregunta": "Estas pensando en un objeto inanimado."},
        },
        "no": {
            "pregunta": "¿Es una emoción?",
            "si": {"pregunta": "Estas pensando en una emoción."},
            "no": {"pregunta": "Estas pensando en una idea o concepto abstracto."},
        },
    }


# --- Ejecución principal del juego ---
if __name__ == "__main__":
    print("Piensa en algo y yo intentaré adivinarlo con preguntas de sí/no.")
    jugar20Q(arbol)
