import random

nCromosomas = 20
nParejas = 50


# Generar padres aleatorios
def generar_padres():
    padre = [[0 for _ in range(nCromosomas)] for _ in range(nParejas)]
    madre = [[0 for _ in range(nCromosomas)] for _ in range(nParejas)]
    for i in range(nParejas):  # Numero de padres
        for j in range(nCromosomas):  # Numero de cromosomas
            padre[i][j] = random.randint(1, 9)  # valores de cromosoma
            madre[i][j] = random.randint(1, 9)
    return padre, madre


# Herencia genetica
def herencia(padre, madre):
    # Cruza los cromosomas de los padres para crear dos hijos con promedios
    hijo_1 = [
        [(padre[i][j] + madre[i][j]) // 2 for j in range(nCromosomas)]
        for i in range(nParejas)
    ]
    hijo_2 = [
        [((padre[i][j] + madre[i][j]) + 1) // 2 for j in range(nCromosomas)]
        for i in range(nParejas)
    ]
    return hijo_1, hijo_2


# Mutación aleatoria en un cromosoma de cada hijo
def mutacion(hijos):
    for i in range(nParejas):  # Iterar hijos
        if random.random() < 0.10:  # 25% probabilidad de mutación por hijo
            j = random.randint(0, nCromosomas - 1)  # Elegir cromosoma aleatorio
            hijos[i][j] = random.randint(1, 9)  # Mutar cromosoma
    return hijos


# Función de torneo para seleccionar un individuo
def torneo(hijos, k=2):
    return max(
        random.sample(hijos, k), key=lambda x: sum(x)
    )  # Selección del mejor individuo, tomados de 2 en 2 al azar en base a la suma de cromosomas


# Actualizar padres con los hijos generados
def actualizar_padres(hijo1, hijo2):
    # Función de torneo para seleccionar un individuo
    nuevos_padres = [torneo(hijo1) for _ in range(nParejas)]
    nuevas_madres = [torneo(hijo2) for _ in range(nParejas)]
    return nuevos_padres, nuevas_madres


# Verificar si al menos un hijo tiene todos los cromosomas en 9
def algun_hijo_nueve(hijos):
    return any(all(cromosoma == 9 for cromosoma in individuo) for individuo in hijos)


# Buscar el hijo y la generación que logró todos los cromosomas en 9
def encontrar_hijo_exitoso(hijos):
    for idx, individuo in enumerate(hijos):
        if all(cromosoma == 9 for cromosoma in individuo):
            return idx, individuo
    return None, None


if __name__ == "__main__":
    padre, madre = generar_padres()
    print(f"Padre original: {padre}")
    print(f"Madre original: {madre}")
    hijo_1, hijo_2 = herencia(padre, madre)
    hijo_1 = mutacion(hijo_1)
    hijo_2 = mutacion(hijo_2)

    generacion = 0
    while not (algun_hijo_nueve(hijo_1) or algun_hijo_nueve(hijo_2)):
        padre, madre = actualizar_padres(hijo_1, hijo_2)
        hijo_1, hijo_2 = herencia(padre, madre)
        hijo_1 = mutacion(hijo_1)
        hijo_2 = mutacion(hijo_2)
        print(f"Generacion: {generacion}")
        generacion += 1

    print(f"Ultimos hijos: {hijo_1}, {hijo_2}")

    idx1, hijo_exitoso1 = encontrar_hijo_exitoso(hijo_1)
    idx2, hijo_exitoso2 = encontrar_hijo_exitoso(hijo_2)

    if hijo_exitoso1 is not None:
        print(
            f"El hijo exitoso está en hijo_1, índice {idx1}, generación {generacion}: {hijo_exitoso1}"
        )
    elif hijo_exitoso2 is not None:
        print(
            f"El hijo exitoso está en hijo_2, índice {idx2}, generación {generacion}: {hijo_exitoso2}"
        )
    else:
        print("No se encontró un hijo exitoso.")
