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
    for i in range(nParejas):
        for j in range(nCromosomas):
            padre[i][j] = hijo1[i][j]
            madre[i][j] = hijo2[nParejas - 1 - i][j]
    return padre, madre


# Verificar si todos los cromosomas de los hijos son 9
def todos_nueve(hijos):
    return all(cromosoma == 9 for individuo in hijos for cromosoma in individuo)


if __name__ == "__main__":
    padre, madre = generar_padres()
    print(f"Padre original: {padre}")
    print(f"Madre original: {madre}")
    hijo_1, hijo_2 = herencia(padre, madre)
    hijo_1 = mutacion(hijo_1)
    hijo_2 = mutacion(hijo_2)

    generacion = 1
    while not (todos_nueve(hijo_1) and todos_nueve(hijo_2)):
        padre, madre = actualizar_padres(hijo_1, hijo_2)
        hijo_1, hijo_2 = herencia(padre, madre)
        hijo_1 = mutacion(hijo_1)
        hijo_2 = mutacion(hijo_2)
        generacion += 1

    print(f"Se alcanzó la meta en la generación {generacion}")
    print(f"Hijo 1 ultima generacion: {hijo_1}")
    print(f"Hijo 2 ultima generacion: {hijo_2}")
