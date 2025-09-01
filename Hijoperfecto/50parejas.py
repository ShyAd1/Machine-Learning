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


# Se utiliza Función escalonada
# Si ambos padres tienen un cromosoma alto, el hijo sube más rápido
def herencia(padre, madre):
    hijo_1 = [
        [
            min(
                (
                    padre[i][j] + 1
                    if padre[i][j] == madre[i][j]
                    else (padre[i][j] + madre[i][j]) // 2
                ),
                9,
            )
            for j in range(nCromosomas)
        ]
        for i in range(nParejas)
    ]
    hijo_2 = [
        [
            min(
                (
                    madre[i][j] + 1
                    if padre[i][j] == madre[i][j]
                    else (padre[i][j] + madre[i][j]) // 2
                ),
                9,
            )
            for j in range(nCromosomas)
        ]
        for i in range(nParejas)
    ]
    return hijo_1, hijo_2


# Mutación aleatoria en un cromosoma de un hijo
def mutacion(hijo):
    if random.random() < 0.1:  # 10% probabilidad de mutación
        i = random.randint(0, nParejas - 1)  # Seleccionar hijo
        j = random.randint(0, nCromosomas - 1)  # Seleccionar cromosoma
        hijo[i][j] = random.randint(1, 9)  # Mutar cromosoma
    return hijo


# Actualizar padres con los hijos generados
def actualizar_padres(hijo1, hijo2):
    todos_hijos = hijo1 + hijo2
    random.shuffle(todos_hijos)

    # Asignar la primera mitad como padres y la segunda como madres
    nuevos_padres = todos_hijos[:nParejas]
    nuevas_madres = todos_hijos[nParejas : 2 * nParejas]
    return nuevos_padres, nuevas_madres


# Verificar si al menos un hijo tiene todos los cromosomas en 9
def algun_hijo_nueve(hijos):
    return any(all(cromosoma == 9 for cromosoma in individuo) for individuo in hijos)


if __name__ == "__main__":
    padre, madre = generar_padres()
    print(f"Padre original: {padre}")
    print(f"Madre original: {madre}")
    hijo_1, hijo_2 = herencia(padre, madre)
    hijo_1 = mutacion(hijo_1)
    hijo_2 = mutacion(hijo_2)

    generacion = 1
    while not (algun_hijo_nueve(hijo_1) or algun_hijo_nueve(hijo_2)):
        padre, madre = actualizar_padres(hijo_1, hijo_2)
        hijo_1, hijo_2 = herencia(padre, madre)
        hijo_1 = mutacion(hijo_1)
        hijo_2 = mutacion(hijo_2)
        generacion += 1

    print(f"Se alcanzó la meta en la generación {generacion}")
    print(f"Hijo 1 ultima generacion: {hijo_1}")
    print(f"Hijo 2 ultima generacion: {hijo_2}")

    # Buscar el hijo y la generación que logró todos los cromosomas en 9
    def encontrar_hijo_exitoso(hijos):
        for idx, individuo in enumerate(hijos):
            if all(cromosoma == 9 for cromosoma in individuo):
                return idx, individuo
        return None, None

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
