import random

# random.seed(42)  # Fijar semilla para reproducibilidad

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


def herencia(padre, madre):
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
        if random.random() < 0.10:  # 10% probabilidad de mutación por hijo
            j = random.randint(0, nCromosomas - 1)  # Elegir cromosoma aleatorio
            hijos[i][j] = random.randint(1, 9)  # Mutar cromosoma
    return hijos


# Actualizar padres con los hijos generados
def actualizar_padres(hijo1, hijo2):
    # Suponiendo que todos_hijos está ordenado por alguna "calidad" descendente
    todos_hijos = hijo1 + hijo2

    # Ordenar hijos por suma de cromosomas (mayor es mejor)
    todos_hijos.sort(key=lambda x: sum(x), reverse=True)

    # Dividir en rangos
    top_180_140 = todos_hijos[0:25]  # 180-140 (25 mejores)
    top_140_100 = todos_hijos[25:50]  # 140-100 (siguientes 25)
    top_100_60 = todos_hijos[50:75]  # 100-60 (siguientes 25)
    top_60_20 = todos_hijos[75:100]  # 60-20 (últimos 25)

    # Juntar según lo que pides
    nuevos_padres = top_180_140 + top_100_60
    nuevas_madres = top_140_100 + top_60_20

    return nuevos_padres, nuevas_madres


# Actualizar padres con los hijos generados
# def actualizar_padres(hijo1, hijo2):
#     todos_hijos = hijo1 + hijo2
#     random.shuffle(todos_hijos)

#     # Asignar la primera mitad como padres y la segunda como madres
#     nuevos_padres = todos_hijos[:nParejas]
#     nuevas_madres = todos_hijos[nParejas : 2 * nParejas]
#     return nuevos_padres, nuevas_madres


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

    generacion = 1
    # for i in range(3):
    #     padre, madre = actualizar_padres(hijo_1, hijo_2)
    #     hijo_1, hijo_2 = herencia(padre, madre)
    #     hijo_1 = mutacion(hijo_1)
    #     hijo_2 = mutacion(hijo_2)
    #     print(f"Hijo 1: {hijo_1}")
    #     print(f"Hijo 2: {hijo_2}")

    while not (algun_hijo_nueve(hijo_1) or algun_hijo_nueve(hijo_2)):
        padre, madre = actualizar_padres(hijo_1, hijo_2)
        hijo_1, hijo_2 = herencia(padre, madre)
        hijo_1 = mutacion(hijo_1)
        hijo_2 = mutacion(hijo_2)
        # print(f"Hijo 1: {hijo_1}")
        # print(f"Hijo 2: {hijo_2}")
        print(f"Generacion: {generacion}")
        generacion += 1

    # print(f"Hijo 1 ultima generacion: {hijo_1}")
    # print(f"Hijo 2 ultima generacion: {hijo_2}")

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
