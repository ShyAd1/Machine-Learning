from dotenv import load_dotenv
from google import genai

load_dotenv()

ALFABETO = list("abcdefghijklmnñopqrstuvwxyz")


def normaliza_si_no(txt: str) -> str:
    t = (txt or "").strip().lower()
    if t in {"si", "sí", "s", "y", "yes"}:
        return "si"
    if t in {"no", "n"}:
        return "no"
    return ""


def pedir_si_no(prompt: str) -> str:
    while True:
        resp = input(prompt).strip()
        v = normaliza_si_no(resp)
        if v:
            return v
        print("Por favor responda 'sí' o 'no'.")


class ContadorPreguntas:
    def __init__(self, max_preguntas: int = 20):
        self.max = max_preguntas
        self.usadas = 0
        self.indice = 1  # numeración en pantalla

    def preguntar(self, prompt: str) -> str:
        if self.usadas >= self.max:
            raise RuntimeError("Se alcanzó el máximo de preguntas permitido.")
        print(self.indice)
        self.indice += 1
        self.usadas += 1
        return pedir_si_no(prompt)

    def restantes(self) -> int:
        return self.max - self.usadas


def busca_letra_binaria(contador: ContadorPreguntas, etiqueta: str) -> str:
    l = 0
    r = len(ALFABETO) - 1
    while l < r:
        mid = l + (r - l) // 2
        letras_izq = "".join(ALFABETO[l : mid + 1])
        resp = contador.preguntar(
            f"¿La {etiqueta} está entre estas letras: {letras_izq}? (sí/no): "
        )
        if resp == "si":
            r = mid
        else:
            l = mid + 1
        if contador.restantes() <= 0:
            break
    return ALFABETO[l]


ARBOL = {
    "q": "¿Es vivo? (sí/no): ",
    "si": {  # Ser vivo
        "q": "¿Pertenece al reino animal? (sí/no): ",
        "si": {
            "q": "¿Vuela? (sí/no): ",
            "si": {"q": "¿Tiene plumas? (sí/no): ", "si": None, "no": None},
            "no": {"q": "¿Vive en el océano? (sí/no): ", "si": None, "no": None},
        },
        "no": {
            "q": "¿Es una planta? (sí/no): ",
            "si": {"q": "¿Produce flores o frutos? (sí/no): ", "si": None, "no": None},
            "no": {"q": "¿Es un hongo? (sí/no): ", "si": None, "no": None},
        },
    },
    "no": {  # No es vivo
        "q": "¿Es abstracto (no se puede tocar)? (sí/no): ",
        "si": {
            "q": "¿Está relacionado con una emoción o estado mental? (sí/no): ",
            "si": {"q": "¿Es positiva? (sí/no): ", "si": None, "no": None},
            "no": {"q": "¿Fue creado por el humano? (sí/no): ", "si": None, "no": None},
        },
        "no": {
            "q": "¿Es comida? (sí/no): ",
            "si": {
                "q": "¿Es dada por la naturaleza? (sí/no): ",
                "si": None,
                "no": None,
            },
            "no": {
                "q": "¿Es más grande que una casa? (sí/no): ",
                "si": None,
                "no": None,
            },
        },
    },
}


def recorre_arbol(
    contador: ContadorPreguntas, nodo: dict, nivel: int = 1, historial=None
):
    """
    Recorre el árbol hasta 4 niveles o hasta llegar a una hoja.
    Devuelve lista de pares (pregunta, respuesta) en orden.
    """
    if historial is None:
        historial = []
    if nodo is None or nivel > 4 or contador.restantes() <= 0:
        return historial

    resp = contador.preguntar(nodo["q"])
    historial.append((nodo["q"].strip().rstrip(":"), resp))

    if nodo.get("si") is None and nodo.get("no") is None:
        return historial

    siguiente = nodo["si"] if resp == "si" else nodo["no"]
    return recorre_arbol(contador, siguiente, nivel + 1, historial)


def juego_20q():
    contador = ContadorPreguntas(max_preguntas=20)

    primera = busca_letra_binaria(contador, "primera letra")
    segunda = busca_letra_binaria(contador, "segunda letra")
    ultima = busca_letra_binaria(contador, "última letra")
    prefijo = primera + segunda

    pares_preg_resp = recorre_arbol(contador, ARBOL, nivel=1)

    return {
        "prefijo": prefijo,
        "ultima": ultima,
        "pares": pares_preg_resp,  # lista de (pregunta, "si"/"no")
        "usadas": contador.usadas,
        "restantes": contador.restantes(),
    }


def formatea_prompt_gemini(datos: dict) -> str:
    lineas = [f"- {p} => {r}" for (p, r) in datos["pares"]]
    return (
        "Actúa como un juego de 20 preguntas (Akinator) y propone UNA sola suposición.\n"
        "Restricciones conocidas de la palabra/ente objetivo:\n"
        f"- Empieza con: {datos['prefijo']}\n"
        f"- Termina con: {datos['ultima']}\n"
        "Respuestas a preguntas binarias del árbol:\n" + "\n".join(lineas) + "\n\n"
        "Devuelve tu suposición más probable en una sola línea."
    )


def main():
    print("Prompt al modelo:\n------------------")

    print("------------------\n")

    try:
        client = genai.Client()
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Eres un experto en 20 preguntas. Hazme 20 preguntas para averiguar qué objeto pienso",
        )
        print("Sugerencia del modelo:", resp.text.strip())
    except Exception as e:
        print("No fue posible invocar al modelo. Detalle:", str(e))
        print("Con base en los filtros anteriores, proponga una palabra candidata.")


if __name__ == "__main__":
    main()
