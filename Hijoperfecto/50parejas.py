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


# Mutación aleatoria en un cromosoma de cada hijo
def mutacion(hijos):
    for i in range(nParejas):  # Iterar hijos
        if random.random() < 0.10:  # 10% probabilidad de mutación por hijo
            j = random.randint(0, nCromosomas - 1)  # Elegir cromosoma aleatorio
            hijos[i][j] = random.randint(1, 9)  # Mutar cromosoma
    return hijos


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


# Función de torneo para seleccionar un individuo evitando incesto
def torneo(hijos, idx, k=50, grupo=None):
    """Torneo donde el individuo idx siempre participa, junto con k-1 aleatorios, evitando incesto."""
    participantes = [hijos[idx]]
    indices = list(range(len(hijos)))
    # Si grupo está definido, excluye los índices del grupo (hermanos)
    if grupo is not None:
        indices = [i for i in indices if i not in grupo]
    else:
        indices.remove(idx)
    participantes += random.sample([hijos[i] for i in indices], k - 1)
    return max(participantes, key=lambda x: x.count(9))


# Actualizar padres con los hijos generados evitando incesto
def actualizar_padres(hijo1, hijo2):
    todos_hijos = hijo1 + hijo2
    nuevos_padres = []
    nuevas_madres = []
    for i in range(nParejas):
        # Los hijos generados por el mismo cruce están en posiciones i y i+nParejas
        grupo_hermanos = [i, i + nParejas]
        # Selecciona padre evitando incesto
        nuevos_padres.append(torneo(todos_hijos, i, grupo=grupo_hermanos))
        # Selecciona madre evitando incesto
        nuevas_madres.append(torneo(todos_hijos, i + nParejas, grupo=grupo_hermanos))
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
    # print(f"Padre original: {padre}")
    # print(f"Madre original: {madre}")
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
        print(f"Hijo 1: {hijo_1}")
        print(f"Hijo 2: {hijo_2}")
        generacion += 1

    # print(f"Ultimo hijo 1: {hijo_1}")
    # print(f"Ultimo hijo 2: {hijo_2}")

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
