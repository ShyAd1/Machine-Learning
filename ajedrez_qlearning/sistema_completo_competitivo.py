import os
import time
import shutil
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from generador_graficas import GeneradorGraficas

print(
    """
================================================================================
    SISTEMA AUTOMATIZADO COMPETITIVO - AJEDREZ Q-LEARNING
================================================================================
Este script hara TODO automaticamente:
  1. Entrenamiento multiple (10 candidatos por caso)
  2. Entrenamiento optimizado (parametros agresivos)
  3. Evaluacion completa vs Aleatorio y Greedy
  4. Analisis de Markov
  5. Generacion de graficas
  6. Reporte de metrica
  
Algoritmo: Q-Learning
================================================================================
"""
)

# Si llegamos aqui, es opcion 1 (entrenamiento)
respuesta = input("\nIniciar entrenamiento completo? (s/n): ").strip().lower()
if respuesta != "s":
    print("Cancelado.")
    exit()

print("\n" + "=" * 80)
print("INICIANDO PROCESO AUTOMATIZADO Q-LEARNING")
print("=" * 80)
print(f"Inicio: {datetime.now().strftime('%H:%M:%S')}")
print("=" * 80 + "\n")

tiempo_inicio_global = time.time()

from entorno import AjedrezSimple
from agente import AgenteQLearning
from oponentes import OponenteAleatorio, OponenteGreedy


# ============================================================================
# FUNCION DE ENTRENAMIENTO
# ============================================================================


def entrenar_candidato(caso, episodios=30000, candidato_id=0):
    n = 4 if caso == "A" else 5
    con_peon = caso == "B"

    juego = AjedrezSimple(n=n, con_peon=con_peon)
    agente = AgenteQLearning(alpha=0.15, gamma=0.98, epsilon=0.4)

    oponente_aleatorio = OponenteAleatorio()
    oponente_greedy = OponenteGreedy()

    # Parámetros de decay
    epsilon_inicial = 0.4
    epsilon_final = 0.05
    epsilon_decay = (epsilon_inicial - epsilon_final) / (episodios * 0.7)

    victorias = 0
    turnos_victoria = []
    recompensas_por_episodio = []

    for episodio in range(episodios):
        # ===== EPSILON DECAY =====
        if episodio < episodios * 0.7:
            agente.epsilon = max(
                epsilon_final, epsilon_inicial - epsilon_decay * episodio
            )
        else:
            agente.epsilon = epsilon_final

        # ===== CURRICULUM SUAVE =====
        # Primer 70%: solo aleatorio
        # Último 30%: gradualmente introduce Greedy hasta 30%
        progreso = episodio / episodios

        if progreso < 0.7:
            p_greedy = 0.0  # Solo aleatorio los primeros 70% de episodios
        else:
            # En el último 30%, crece de 0% a 30%
            progreso_final = (progreso - 0.7) / 0.3
            p_greedy = min(0.3, progreso_final * 0.3)

        estado = juego.reset()
        turnos_partida = 0
        recompensa_total_episodio = 0

        for paso in range(50):
            turnos_partida += 1

            # ===== TURNO AGENTE =====
            acciones_agente = juego.obtener_acciones_legales()
            if not acciones_agente:
                break

            accion = agente.elegir_accion(estado, acciones_agente)
            siguiente_estado, recompensa, terminado = juego.hacer_movimiento(accion)

            # Ajustar recompensa
            if recompensa == -0.1:
                recompensa = -0.5

            if terminado and recompensa > 50:
                bonus_velocidad = max(0, 10 - turnos_partida)
                recompensa += bonus_velocidad

            recompensa_total_episodio += recompensa

            # Actualizar Q-Learning
            siguientes_acciones = juego.obtener_acciones_legales()
            agente.actualizar(
                estado, accion, recompensa, siguiente_estado, siguientes_acciones
            )

            if terminado:
                if recompensa > 50:
                    victorias += 1
                    turnos_victoria.append(turnos_partida)
                break

            estado = siguiente_estado

            # ===== TURNO OPONENTE (UN SOLO IF) =====
            acciones_oponente = juego.obtener_acciones_legales()
            if acciones_oponente:
                # Curriculum continuo (no escalera)
                if random.random() < p_greedy:
                    accion_oponente = oponente_greedy.elegir_accion(juego)
                else:
                    accion_oponente = oponente_aleatorio.elegir_accion(juego)

                estado, _, terminado = juego.hacer_movimiento(accion_oponente)
                if terminado:
                    break
            else:
                break

        recompensas_por_episodio.append(recompensa_total_episodio)

    return agente, victorias, turnos_victoria, recompensas_por_episodio


def entrenar_mejor_caso(caso, num_candidatos=10, episodios=30000):
    """Entrena multiples candidatos y elige el mejor"""
    print(f"\n{'='*80}")
    print(f"ENTRENAMIENTO MULTIPLE - CASO {caso} [Q-Learning]")
    print(f"{'='*80}")
    print(f"Candidatos: {num_candidatos} | Episodios: {episodios}")
    print(f"{'='*80}\n")

    mejores = []

    for i in range(num_candidatos):
        print(f"[{i+1}/{num_candidatos}] Entrenando candidato {i+1}...")
        tiempo_inicio = time.time()

        agente, victorias_entrenamiento, turnos, recompensas = entrenar_candidato(
            caso, episodios, i
        )

        print(
            f"    Entrenamiento: {victorias_entrenamiento} victorias en {episodios} episodios"
        )
        print(f"    Evaluando vs Greedy...")

        tasa, turnos_prom, score = evaluar_candidato(agente, caso, 50)

        tiempo_candidato = time.time() - tiempo_inicio

        mejores.append(
            {
                "id": i + 1,
                "agente": agente,
                "tasa_greedy": tasa,
                "turnos": turnos_prom,
                "score": score,
                "tiempo": tiempo_candidato,
                "recompensas": recompensas,
            }
        )

        print(
            f"    Resultado: {tasa:.0f}% victoria | {turnos_prom:.1f} turnos | Score: {score:.1f}"
        )
        print(f"    Tiempo: {tiempo_candidato/60:.1f} min\n")

    mejores.sort(key=lambda x: x["score"], reverse=True)

    print(f"\n{'='*80}")
    print(f"RANKING CASO {caso} [Q-Learning]")
    print(f"{'='*80}")
    for i, candidato in enumerate(mejores[:5], 1):
        print(
            f"{i}. Candidato #{candidato['id']}: "
            f"{candidato['tasa_greedy']:.0f}% | "
            f"{candidato['turnos']:.1f} turnos | "
            f"Score: {candidato['score']:.1f}"
        )
    print(f"{'='*80}\n")

    return mejores[0]["agente"], mejores[0], mejores[0]["recompensas"]


def evaluar_candidato(agente, caso, num_partidas=50):
    """Evalua un agente rapidamente"""
    n = 4 if caso == "A" else 5
    con_peon = caso == "B"

    agente.epsilon = 0
    oponente = OponenteGreedy()

    victorias = 0
    turnos_victoria = []

    for _ in range(num_partidas):
        juego = AjedrezSimple(n=n, con_peon=con_peon)
        estado = juego.reset()

        for turno in range(1, 51):
            acciones = juego.obtener_acciones_legales()
            if not acciones:
                break

            accion = agente.elegir_accion(estado, acciones)
            estado, recompensa, terminado = juego.hacer_movimiento(accion)

            if terminado:
                if recompensa > 50:
                    victorias += 1
                    turnos_victoria.append(turno)
                break

            accion_oponente = oponente.elegir_accion(juego)
            if not accion_oponente:
                break

            estado, _, terminado = juego.hacer_movimiento(accion_oponente)
            if terminado:
                break

    tasa = victorias / num_partidas * 100
    turnos_prom = np.mean(turnos_victoria) if turnos_victoria else 999
    score = tasa * 0.6 - turnos_prom * 2

    return tasa, turnos_prom, score


def evaluacion_completa(agente, caso, nombre="agente"):
    """Evaluacion completa vs ambos oponentes"""
    print(f"\n{'='*80}")
    print(f"EVALUACION COMPLETA - CASO {caso} ({nombre})")
    print(f"{'='*80}\n")

    n = 4 if caso == "A" else 5
    con_peon = caso == "B"
    agente.epsilon = 0

    resultados = {}

    for oponente_tipo in ["aleatorio", "greedy"]:
        print(f"Evaluando vs {oponente_tipo.capitalize()}...")

        if oponente_tipo == "aleatorio":
            oponente = OponenteAleatorio()
        else:
            oponente = OponenteGreedy()

        victorias = 0
        derrotas = 0
        empates = 0
        turnos_victoria = []

        for i in range(100):
            juego = AjedrezSimple(n=n, con_peon=con_peon)
            estado = juego.reset()

            for turno in range(1, 51):
                acciones = juego.obtener_acciones_legales()
                if not acciones:
                    empates += 1
                    break

                accion = agente.elegir_accion(estado, acciones)
                estado, recompensa, terminado = juego.hacer_movimiento(accion)

                if terminado:
                    if recompensa > 50:
                        victorias += 1
                        turnos_victoria.append(turno)
                    else:
                        derrotas += 1
                    break

                accion_oponente = oponente.elegir_accion(juego)
                if not accion_oponente:
                    empates += 1
                    break

                estado, _, terminado = juego.hacer_movimiento(accion_oponente)

                if terminado:
                    derrotas += 1
                    break
            else:
                empates += 1

            if (i + 1) % 25 == 0:
                print(f"  Progreso: {i+1}/100")

        resultados[oponente_tipo] = {
            "victorias": victorias,
            "derrotas": derrotas,
            "empates": empates,
            "turnos_victoria": turnos_victoria,
        }

        print(
            f"  Victorias: {victorias}% | Turnos promedio: {np.mean(turnos_victoria) if turnos_victoria else 'N/A'}\n"
        )

    return resultados


def analisis_markov(caso, num_partidas=1000):
    """Analisis de Markov con politica aleatoria"""
    print(f"\n{'='*80}")
    print(f"ANALISIS DE MARKOV - CASO {caso}")
    print(f"{'='*80}\n")

    n = 4 if caso == "A" else 5
    con_peon = caso == "B"

    resultados = {"blanco": 0, "negro": 0, "empate": 0}
    longitudes = []
    estados_visitados = set()

    print(f"Simulando {num_partidas} partidas aleatorias...")

    for i in range(num_partidas):
        juego = AjedrezSimple(n=n, con_peon=con_peon)
        juego.reset()

        for paso in range(50):
            estado = juego.get_estado()
            estados_visitados.add(estado)

            acciones = juego.obtener_acciones_legales()
            if not acciones:
                resultados["empate"] += 1
                longitudes.append(paso + 1)
                break

            accion = random.choice(acciones)
            _, recompensa, terminado = juego.hacer_movimiento(accion)

            if terminado:
                if juego.turno == -1:
                    resultados["blanco"] += 1
                else:
                    resultados["negro"] += 1
                longitudes.append(paso + 1)
                break
        else:
            resultados["empate"] += 1
            longitudes.append(50)

        if (i + 1) % 200 == 0:
            print(f"  Progreso: {i+1}/{num_partidas}")

    total = sum(resultados.values())
    prob_blanco = resultados["blanco"] / total
    prob_negro = resultados["negro"] / total
    prob_empate = resultados["empate"] / total

    print(f"\nResultados:")
    print(f"  P(Blanco) = {prob_blanco:.3f} ({prob_blanco*100:.1f}%)")
    print(f"  P(Negro)  = {prob_negro:.3f} ({prob_negro*100:.1f}%)")
    print(f"  P(Empate) = {prob_empate:.3f} ({prob_empate*100:.1f}%)")
    print(f"  Longitud promedio: {np.mean(longitudes):.1f} movimientos")
    print(f"  Estados unicos: {len(estados_visitados):,}")

    return {
        "probabilidades": (prob_blanco, prob_negro, prob_empate),
        "longitud_promedio": np.mean(longitudes),
        "longitudes": longitudes,
        "estados_unicos": len(estados_visitados),
        "resultados": resultados,
    }


# ============================================================================
# EJECUCION PRINCIPAL
# ============================================================================

# ============================================================================
# EJECUCION PRINCIPAL - SOLO Q-LEARNING
# ============================================================================

print("\n" + "=" * 80)
print("FASE 1: ENTRENAMIENTO CASO A")
print("=" * 80)
agente_A, stats_A, recompensas_A = entrenar_mejor_caso(
    "A", num_candidatos=10, episodios=20000
)
agente_A.guardar("agente_caso_A_QLEARNING.pkl")

print("\n" + "=" * 80)
print("FASE 2: ENTRENAMIENTO CASO B")
print("=" * 80)
agente_B, stats_B, recompensas_B = entrenar_mejor_caso(
    "B", num_candidatos=10, episodios=30000
)
agente_B.guardar("agente_caso_B_QLEARNING.pkl")

print("\n" + "=" * 80)
print("FASE 3: EVALUACION COMPLETA")
print("=" * 80)
resultados_A = evaluacion_completa(agente_A, "A", "Q-Learning")
resultados_B = evaluacion_completa(agente_B, "B", "Q-Learning")

print("\n" + "=" * 80)
print("FASE 4: ANALISIS DE MARKOV")
print("=" * 80)
markov_A = analisis_markov("A", 1000)
markov_B = analisis_markov("B", 1000)

print("\n" + "=" * 80)
print("FASE 5: GENERACION DE TODAS LAS GRAFICAS")
print("=" * 80)
generador = GeneradorGraficas(carpeta_salida="graficas", dpi=300)
generador.generar_todas(
    resultados_A, resultados_B, markov_A, markov_B, recompensas_A, recompensas_B
)

tiempo_total = time.time() - tiempo_inicio_global

print("\n" + "=" * 80)
print("PROCESO COMPLETADO")
print("=" * 80)
print(f"Tiempo total: {tiempo_total/60:.1f} minutos")
print(f"Fin: {datetime.now().strftime('%H:%M:%S')}")
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS FINALES")
print("=" * 80)

print(f"\nCASO A (4x4):")
print(f"  Score entrenamiento: {stats_A['score']:.1f}")
print(f"  vs Aleatorio: {resultados_A['aleatorio']['victorias']}%")
print(f"  vs Greedy:    {resultados_A['greedy']['victorias']}%")
if resultados_A["greedy"]["turnos_victoria"]:
    print(
        f"  Turnos vs Greedy: {np.mean(resultados_A['greedy']['turnos_victoria']):.1f}"
    )

print(f"\nCASO B (5x5):")
print(f"  Score entrenamiento: {stats_B['score']:.1f}")
print(f"  vs Aleatorio: {resultados_B['aleatorio']['victorias']}%")
print(f"  vs Greedy:    {resultados_B['greedy']['victorias']}%")
if resultados_B["greedy"]["turnos_victoria"]:
    print(
        f"  Turnos vs Greedy: {np.mean(resultados_B['greedy']['turnos_victoria']):.1f}"
    )

print(f"\nMEJORA POR RL:")
mejora_A = resultados_A["greedy"]["victorias"] - markov_A["probabilidades"][0] * 100
mejora_B = resultados_B["greedy"]["victorias"] - markov_B["probabilidades"][0] * 100
print(f"  Caso A: {mejora_A:+.1f} puntos vs politica aleatoria")
print(f"  Caso B: {mejora_B:+.1f} puntos vs politica aleatoria")

print(f"\nARCHIVOS GENERADOS:")
print(f"  - agente_caso_A_QLEARNING.pkl")
print(f"  - agente_caso_B_QLEARNING.pkl")
print(f"  - graficas/ (7 imagenes)")

print("\n" + "=" * 80)
print("EJECUTA 'demo_pygame.py' PARA VER TU AGENTE EN ACCION")
print("=" * 80)
