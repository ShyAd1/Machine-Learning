def ordenar_individuos_por_suma(lista):
    """Ordena una lista de individuos de mayor a menor según la suma de sus atributos."""
    return sorted(lista, key=lambda ind: sum(ind), reverse=True)


import random


# Genera la primera generacion
def gen_1():
    hombre = [[0 for _ in range(20)] for i in range(50)]
    mujer = [[0 for _ in range(20)] for i in range(50)]
    for i in range(50):
        for j in range(20):
            hombre[i][j] = random.randint(1, 9)
            mujer[i][j] = random.randint(1, 9)
    return hombre, mujer


def ordenar_individuos_por_suma(lista):
    """Ordena una lista de individuos de mayor a menor según la suma de sus atributos."""
    return sorted(lista, key=lambda ind: sum(ind), reverse=True)


def clas(hombre, mujer):
    new_hombre = [[0 for _ in range(20)] for i in range(50)]
    new_mujer = [[0 for _ in range(20)] for i in range(50)]
    for i in range(50):
        if random.random() < 0.50:
            k = 0
            for j in range(20):
                new_hombre[i][j] = (hombre[i][j] + mujer[k][j]) // 2
                new_mujer[i][j] = (hombre[i][j] + mujer[k][j]) // 2
                if (hombre[i][j] + mujer[k][j]) % 2 != 0:
                    if random.random() < 0.5:
                        new_hombre[i][j] += 1
                    else:
                        new_mujer[i][j] += 1
        else:
            k = random.randint(0, len(mujer) - 1)
            for j in range(20):
                new_hombre[i][j] = (hombre[i][j] + mujer[k][j]) // 2
                new_mujer[i][j] = (hombre[i][j] + mujer[k][j]) // 2
                if (hombre[i][j] + mujer[k][j]) % 2 != 0:
                    if random.random() < 0.5:
                        new_hombre[i][j] += 1
                    else:
                        new_mujer[i][j] += 1
        mujer.pop(k)

    return new_hombre, new_mujer


def mutacion(hombre, mujer):
    for i in range(50):
        if random.random() < 0.25:
            j = random.randint(0, 19)
            hombre[i][j] = random.randint(1, 9)
        if random.random() < 0.25:
            j = random.randint(0, 19)
            mujer[i][j] = random.randint(1, 9)
    return hombre, mujer


# Verifica si existe un individuo perfecto
def individuo_perfecto(individuos):
    return any(all(c == 9 for c in individuo) for individuo in individuos)


def main():
    hombre, mujer = gen_1()
    gen = 0
    hombre = ordenar_individuos_por_suma(hombre)
    mujer = ordenar_individuos_por_suma(mujer)
    hombre, mujer = clas(hombre, mujer)
    while True:
        gen += 1
        hombre = ordenar_individuos_por_suma(hombre)
        mujer = ordenar_individuos_por_suma(mujer)
        hombre, mujer = clas(hombre, mujer)
        hombre, mujer = mutacion(hombre, mujer)
        print(f"Generación {gen}:")
        print(f"Hombre mejor: {hombre[0]} Suma: {sum(hombre[0])}")
        print(f"Mujer mejor: {mujer[0]} Suma: {sum(mujer[0])}")
        if individuo_perfecto(hombre) or individuo_perfecto(mujer):
            print("¡Individuo perfecto encontrado!")
            break


if __name__ == "__main__":
    main()
