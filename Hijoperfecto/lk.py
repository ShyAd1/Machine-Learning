import random

#Genera la primera generacion
def gen_1 ():
    hombre=[[ 0 for _ in range(20)] for i in range(50)]
    mujer=[[ 0 for _ in range(20)] for i in range(50)]
    for i in range(50):
        for j in range(20):
            hombre[i][j] = random.randint(1,9)
            mujer[i][j] = random.randint(1,9)
    return  hombre, mujer


#Crea la siguiente generacion
def sig_gen (hombre, mujer):
    new_hombre=[[ 0 for _ in range(20)] for i in range(50)]
    new_mujer=[[ 0 for _ in range(20)] for i in range(50)]
    orden_h, orden_m = restriccion()
    for i in range(50):
        for j in range(20):
        #============================Crossover binario====================================
        #   if random.random() < 0.5:
        #       new_hombre[i][j] = hombre[i][j]
        #    else:
        #        new_hombre[i][j] = mujer[i][j]
        #   if random.random() < 0.5:
        #        new_mujer[i][j] = hombre[i][j]
        #    else:
        #        new_mujer[i][j] = mujer[i][j]
        #================================Promedio========================================
            new_hombre[i][j] = (hombre[orden_h[i]][j]+mujer[orden_m[i]][j])//2 # (//)siempre redondea hacia abajo
            new_mujer[i][j] = (hombre[orden_h[i]][j]+mujer[orden_m[i]][j])//2
            if (hombre[orden_h[i]][j]+mujer[orden_m[i]][j]) % 2 != 0:
                if random.random() < 0.5:
                    new_hombre[i][j] += 1
                else:
                    new_mujer[i][j] += 1
        #=================================Evolucion escalonada===========================
            #else:
            #   if new_hombre[i][j] == new_mujer[i][j] and new_hombre[i][j] < 9 and new_mujer[i][j] < 9:
            #       new_hombre[i][j] +=1
            #      new_mujer[i][j] +=1

    return new_hombre, new_mujer

#Garantiza que no se crucen con sus propios genes
def restriccion ():
    a_h = list(range(50))
    a_m = list(range(50))
    bro = True
    while bro:
        random.shuffle(a_m)
        random.shuffle(a_h)
        bro = False
        for i in range(50):
            if a_h[i] == a_m[i]:
                bro = True
    return a_h, a_m

#Aplica mutacion a los individuos
def mutacion (hombre, mujer):
    for i in range(50):
        if random.random() < 0.25:
            j = random.randint(0,19)
            hombre[i][j] = random.randint(1,9)
        if random.random() < 0.25:
            j = random.randint(0,19)
            mujer[i][j] = random.randint(1,9)
    return hombre, mujer

#Verifica si existe un individuo perfecto
def individuo_perfecto(individuos):
    return any(all(c == 9 for c in individuo) for individuo in individuos)

def main ():
    hombre, mujer = gen_1()
    gen = 0
    not_perfect = True
    while not_perfect:
        gen += 1
        print(f"Generacion: {gen}")
        hombre, mujer = sig_gen(hombre, mujer)
        hombre, mujer = mutacion(hombre, mujer)
        if individuo_perfecto(hombre) or individuo_perfecto(mujer):
            print(f"Se alcanzó un individuo perfecto en la generación {gen}")
            break

if __name__ == "__main__":
    main()