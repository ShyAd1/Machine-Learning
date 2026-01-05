"""
Generador de Gráficas - Módulo de Visualización
================================================
Genera todas las gráficas del proyecto de forma modular.
Puede usarse independientemente del sistema de entrenamiento.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class GeneradorGraficas:
    """Clase para generar todas las gráficas del proyecto"""

    def __init__(self, carpeta_salida="graficas", dpi=300):
        """
        Inicializa el generador de gráficas

        Args:
            carpeta_salida: Carpeta donde se guardarán las gráficas
            dpi: Resolución de las imágenes (default: 300)
        """
        self.carpeta = carpeta_salida
        self.dpi = dpi

        # Crear carpeta si no existe
        os.makedirs(self.carpeta, exist_ok=True)
        print(f" Carpeta de gráficas: {self.carpeta}/")

    def _guardar(self, nombre_archivo):
        """Guarda la figura actual y cierra"""
        ruta = os.path.join(self.carpeta, nombre_archivo)
        plt.savefig(ruta, dpi=self.dpi, bbox_inches="tight")
        plt.close()
        print(f"{nombre_archivo}")

    def grafica_tasa_victoria(self, resultados_A, resultados_B):
        """Gráfica 1: Comparación tasa de victoria"""
        plt.figure(figsize=(8, 6))

        casos = ["Caso A\n(4x4)", "Caso B\n(5x5)"]
        vic_ale = [
            resultados_A["aleatorio"]["victorias"],
            resultados_B["aleatorio"]["victorias"],
        ]
        vic_gre = [
            resultados_A["greedy"]["victorias"],
            resultados_B["greedy"]["victorias"],
        ]

        x = np.arange(len(casos))
        width = 0.35

        bars1 = plt.bar(
            x - width / 2,
            vic_ale,
            width,
            label="vs Aleatorio",
            color="#4CAF50",
            edgecolor="black",
        )
        bars2 = plt.bar(
            x + width / 2,
            vic_gre,
            width,
            label="vs Greedy",
            color="#F44336",
            edgecolor="black",
        )

        plt.ylabel("Tasa de Victoria (%)", fontsize=12, fontweight="bold")
        plt.title("Comparación: Tasa de Victoria", fontsize=14, fontweight="bold")
        plt.xticks(x, casos, fontsize=11)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, axis="y")
        plt.ylim(0, 105)

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 1,
                    f"{int(height)}%",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=11,
                )

        plt.tight_layout()
        self._guardar("1_tasa_victoria.png")

    def grafica_velocidad_victoria(self, resultados_A, resultados_B):
        """Gráfica 2: Velocidad de victoria (turnos promedio)"""
        plt.figure(figsize=(8, 6))

        turnos_A_ale = (
            np.mean(resultados_A["aleatorio"]["turnos_victoria"])
            if resultados_A["aleatorio"]["turnos_victoria"]
            else 0
        )
        turnos_A_gre = (
            np.mean(resultados_A["greedy"]["turnos_victoria"])
            if resultados_A["greedy"]["turnos_victoria"]
            else 0
        )
        turnos_B_ale = (
            np.mean(resultados_B["aleatorio"]["turnos_victoria"])
            if resultados_B["aleatorio"]["turnos_victoria"]
            else 0
        )
        turnos_B_gre = (
            np.mean(resultados_B["greedy"]["turnos_victoria"])
            if resultados_B["greedy"]["turnos_victoria"]
            else 0
        )

        data = [turnos_A_ale, turnos_A_gre, turnos_B_ale, turnos_B_gre]
        labels = ["A vs Ale", "A vs Gre", "B vs Ale", "B vs Gre"]
        colors = ["#4CAF50", "#F44336", "#2196F3", "#FF9800"]

        bars = plt.bar(labels, data, color=colors, edgecolor="black")
        plt.ylabel("Turnos promedio", fontsize=12, fontweight="bold")
        plt.title("Velocidad de Victoria", fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3, axis="y")
        plt.ylim(0, max(data) * 1.2)

        for bar, val in zip(bars, data):
            if val > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    bar.get_height() + 0.1,
                    f"{val:.1f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=11,
                )

        plt.tight_layout()
        self._guardar("2_velocidad_victoria.png")

    def grafica_distribucion_markov_A(self, markov_A):
        """Gráfica 3: Distribución Markov Caso A"""
        plt.figure(figsize=(8, 6))

        plt.hist(
            markov_A["longitudes"], bins=30, edgecolor="black", alpha=0.7, color="green"
        )
        plt.axvline(
            markov_A["longitud_promedio"],
            color="red",
            linestyle="--",
            linewidth=2.5,
            label=f"Media: {markov_A['longitud_promedio']:.1f}",
        )

        plt.xlabel("Longitud de partida", fontsize=12, fontweight="bold")
        plt.ylabel("Frecuencia", fontsize=12, fontweight="bold")
        plt.title("Caso A: Distribución Markov", fontsize=14, fontweight="bold")
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        self._guardar("3_distribucion_markov_A.png")

    def grafica_distribucion_markov_B(self, markov_B):
        """Gráfica 4: Distribución Markov Caso B"""
        plt.figure(figsize=(8, 6))

        plt.hist(
            markov_B["longitudes"], bins=30, edgecolor="black", alpha=0.7, color="blue"
        )
        plt.axvline(
            markov_B["longitud_promedio"],
            color="red",
            linestyle="--",
            linewidth=2.5,
            label=f"Media: {markov_B['longitud_promedio']:.1f}",
        )

        plt.xlabel("Longitud de partida", fontsize=12, fontweight="bold")
        plt.ylabel("Frecuencia", fontsize=12, fontweight="bold")
        plt.title("Caso B: Distribución Markov", fontsize=14, fontweight="bold")
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        self._guardar("4_distribucion_markov_B.png")

    def grafica_complejidad_estados(self, markov_A, markov_B):
        """Gráfica 5: Complejidad del espacio de estados"""
        plt.figure(figsize=(8, 6))

        casos = ["Caso A\n(4x4)", "Caso B\n(5x5)"]
        estados = [markov_A["estados_unicos"], markov_B["estados_unicos"]]

        bars = plt.bar(casos, estados, color=["#4CAF50", "#2196F3"], edgecolor="black")
        plt.ylabel("Estados únicos visitados", fontsize=12, fontweight="bold")
        plt.title("Complejidad del Espacio de Estados", fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3, axis="y")
        plt.ylim(0, max(estados) * 1.15)

        for bar, val in zip(bars, estados):
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() + 500,
                f"{val:,}",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=11,
            )

        plt.tight_layout()
        self._guardar("5_complejidad_estados.png")

    def grafica_mejora_rl(self, resultados_A, resultados_B, markov_A, markov_B):
        """Gráfica 6: Mejora de política aleatoria vs RL"""
        plt.figure(figsize=(8, 6))

        casos = ["Caso A\n(4x4)", "Caso B\n(5x5)"]
        markov_probs = [
            markov_A["probabilidades"][0] * 100,
            markov_B["probabilidades"][0] * 100,
        ]
        rl_probs = [
            resultados_A["greedy"]["victorias"],
            resultados_B["greedy"]["victorias"],
        ]

        x = np.arange(len(casos))
        width = 0.35

        bars1 = plt.bar(
            x - width / 2,
            markov_probs,
            width,
            label="Política Aleatoria",
            color="gray",
            alpha=0.7,
            edgecolor="black",
        )
        bars2 = plt.bar(
            x + width / 2,
            rl_probs,
            width,
            label="Agente RL",
            color="gold",
            edgecolor="black",
        )

        plt.ylabel("Tasa de victoria (%)", fontsize=12, fontweight="bold")
        plt.title("Mejora: Aleatorio vs RL (vs Greedy)", fontsize=14, fontweight="bold")
        plt.xticks(x, casos, fontsize=11)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, axis="y")
        plt.ylim(0, 85)

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 1,
                    f"{height:.0f}%",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                )

        plt.tight_layout()
        self._guardar("6_mejora_rl.png")

    def grafica_curva_aprendizaje(self, recompensas_A, recompensas_B, ventana=100):
        """Gráfica 7: Curva de aprendizaje (recompensa vs episodios)"""

        def promedio_movil(datos, ventana):
            """Calcula promedio móvil para suavizar la curva"""
            if len(datos) < ventana:
                return datos
            return np.convolve(datos, np.ones(ventana) / ventana, mode="valid")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # ===== CASO A =====
        episodios_A = range(len(recompensas_A))
        promedio_A = promedio_movil(recompensas_A, ventana)

        ax1.plot(
            episodios_A,
            recompensas_A,
            alpha=0.2,
            color="lightblue",
            linewidth=0.5,
            label="Recompensa por episodio",
        )
        ax1.plot(
            range(ventana - 1, len(recompensas_A)),
            promedio_A,
            color="darkblue",
            linewidth=2.5,
            label=f"Promedio móvil ({ventana} episodios)",
        )
        ax1.axhline(y=0, color="red", linestyle="--", linewidth=1, alpha=0.5)
        ax1.set_xlabel("Episodio", fontsize=12, fontweight="bold")
        ax1.set_ylabel("Recompensa Total", fontsize=12, fontweight="bold")
        ax1.set_title(
            "Caso A (4x4): Curva de Aprendizaje", fontsize=14, fontweight="bold"
        )
        ax1.legend(loc="lower right")
        ax1.grid(True, alpha=0.3)

        promedio_final_A = np.mean(recompensas_A[-1000:])
        ax1.text(
            0.02,
            0.98,
            f"Promedio últimos 1000 ep: {promedio_final_A:.1f}",
            transform=ax1.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

        # ===== CASO B =====
        episodios_B = range(len(recompensas_B))
        promedio_B = promedio_movil(recompensas_B, ventana)

        ax2.plot(
            episodios_B,
            recompensas_B,
            alpha=0.2,
            color="lightgreen",
            linewidth=0.5,
            label="Recompensa por episodio",
        )
        ax2.plot(
            range(ventana - 1, len(recompensas_B)),
            promedio_B,
            color="darkgreen",
            linewidth=2.5,
            label=f"Promedio móvil ({ventana} episodios)",
        )
        ax2.axhline(y=0, color="red", linestyle="--", linewidth=1, alpha=0.5)
        ax2.set_xlabel("Episodio", fontsize=12, fontweight="bold")
        ax2.set_ylabel("Recompensa Total", fontsize=12, fontweight="bold")
        ax2.set_title(
            "Caso B (5x5): Curva de Aprendizaje", fontsize=14, fontweight="bold"
        )
        ax2.legend(loc="lower right")
        ax2.grid(True, alpha=0.3)

        promedio_final_B = np.mean(recompensas_B[-1000:])
        ax2.text(
            0.02,
            0.98,
            f"Promedio últimos 1000 ep: {promedio_final_B:.1f}",
            transform=ax2.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

        plt.tight_layout()
        self._guardar("7_curva_aprendizaje.png")

    def generar_todas(
        self,
        resultados_A,
        resultados_B,
        markov_A,
        markov_B,
        recompensas_A=None,
        recompensas_B=None,
    ):
        """
        Genera todas las gráficas del proyecto

        Args:
            resultados_A: Diccionario con resultados de evaluación caso A
            resultados_B: Diccionario con resultados de evaluación caso B
            markov_A: Diccionario con resultados de análisis Markov caso A
            markov_B: Diccionario con resultados de análisis Markov caso B
            recompensas_A: Lista de recompensas por episodio caso A (opcional)
            recompensas_B: Lista de recompensas por episodio caso B (opcional)
        """
        print("\n" + "=" * 80)
        print("GENERANDO TODAS LAS GRÁFICAS")
        print("=" * 80 + "\n")

        inicio = datetime.now()

        print("1/7 - Tasa de victoria...")
        self.grafica_tasa_victoria(resultados_A, resultados_B)

        print("2/7 - Velocidad de victoria...")
        self.grafica_velocidad_victoria(resultados_A, resultados_B)

        print("3/7 - Distribución Markov A...")
        self.grafica_distribucion_markov_A(markov_A)

        print("4/7 - Distribución Markov B...")
        self.grafica_distribucion_markov_B(markov_B)

        print("5/7 - Complejidad de estados...")
        self.grafica_complejidad_estados(markov_A, markov_B)

        print("6/7 - Mejora RL vs Aleatorio...")
        self.grafica_mejora_rl(resultados_A, resultados_B, markov_A, markov_B)

        if recompensas_A is not None and recompensas_B is not None:
            print("7/7 - Curva de aprendizaje...")
            self.grafica_curva_aprendizaje(recompensas_A, recompensas_B)
        else:
            print("7/7 - Curva de aprendizaje... OMITIDA (sin datos)")

        fin = datetime.now()
        tiempo = (fin - inicio).total_seconds()

        print("\n" + "=" * 80)
        print("GRÁFICAS GENERADAS EXITOSAMENTE")
        print("=" * 80)
        print(f"Carpeta: {self.carpeta}/")
        print(f"Tiempo: {tiempo:.1f} segundos")
        print(f"Resolución: {self.dpi} DPI")
        print("=" * 80 + "\n")


# ============================================================================
# FUNCIÓN DE CONVENIENCIA PARA USO DIRECTO
# ============================================================================


def generar_graficas_proyecto(
    resultados_A,
    resultados_B,
    markov_A,
    markov_B,
    recompensas_A=None,
    recompensas_B=None,
    carpeta="graficas",
    dpi=300,
):
    """
    Función de conveniencia para generar todas las gráficas

    Uso:
        from generador_graficas import generar_graficas_proyecto
        generar_graficas_proyecto(resultados_A, resultados_B, markov_A, markov_B)
    """
    generador = GeneradorGraficas(carpeta_salida=carpeta, dpi=dpi)
    generador.generar_todas(
        resultados_A, resultados_B, markov_A, markov_B, recompensas_A, recompensas_B
    )


# ============================================================================
# SCRIPT EJECUTABLE (para generar con datos de ejemplo)
# ============================================================================

if __name__ == "__main__":
    print("Modo de ejemplo: Generando gráficas con datos simulados...\n")

    # Datos de ejemplo
    resultados_A = {
        "aleatorio": {"victorias": 92, "turnos_victoria": [3.2] * 92},
        "greedy": {"victorias": 75, "turnos_victoria": [3.2] * 75},
    }

    resultados_B = {
        "aleatorio": {"victorias": 99, "turnos_victoria": [4.9] * 99},
        "greedy": {"victorias": 64, "turnos_victoria": [4.7] * 64},
    }

    markov_A = {
        "probabilidades": (0.478, 0.481, 0.041),
        "longitud_promedio": 18.4,
        "longitudes": np.random.normal(18.4, 8, 1000).clip(1, 50),
        "estados_unicos": 9015,
    }

    markov_B = {
        "probabilidades": (0.425, 0.398, 0.177),
        "longitud_promedio": 27.7,
        "longitudes": np.random.normal(27.7, 12, 1000).clip(1, 50),
        "estados_unicos": 22041,
    }

    # Simular recompensas de entrenamiento
    recompensas_A = np.cumsum(np.random.randn(30000) * 2 + 0.1)
    recompensas_B = np.cumsum(np.random.randn(30000) * 2.5 + 0.05)

    # Generar todas las gráficas
    generar_graficas_proyecto(
        resultados_A, resultados_B, markov_A, markov_B, recompensas_A, recompensas_B
    )
