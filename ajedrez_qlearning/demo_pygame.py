"""
DEMO INTERACTIVO CON PYGAME - AJEDREZ Q-LEARNING
Visualiza partidas del agente entrenado contra diferentes oponentes
"""

import pygame
import sys
import os
from entorno import AjedrezSimple
from agente import AgenteQLearning
from oponentes import OponenteAleatorio, OponenteGreedy

# Inicializar Pygame
pygame.init()

# Colores mejorados para mejor visibilidad
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CREMA = (255, 248, 220)  # Casillas claras del tablero
MARRON = (139, 90, 43)  # Casillas oscuras del tablero
VERDE_BRILLANTE = (50, 205, 50)  # Resaltar destino
AZUL_CLARO = (135, 206, 250)  # Resaltar origen
ROJO_BRILLANTE = (220, 20, 60)  # Mensajes importantes
AZUL_OSCURO = (25, 25, 112)  # Texto principal
AMARILLO_ORO = (255, 215, 0)  # Resaltar victorias
GRIS_FONDO = (245, 245, 245)  # Fondo general

# Configuración de ventana (más grande)
ANCHO_VENTANA = 1000
ALTO_VENTANA = 900  # Mayor altura para Caso B
TAMANO_CELDA = 75  # Celdas más grandes


class VisualizadorPygame:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("♔ Ajedrez Q-Learning - Demo Interactivo ♔")
        self.reloj = pygame.time.Clock()
        # Fuentes más grandes y legibles
        self.fuente_titulo = pygame.font.Font(None, 56)
        self.fuente_grande = pygame.font.Font(None, 72)  # Para piezas
        self.fuente_mediana = pygame.font.Font(None, 42)
        self.fuente_pequena = pygame.font.Font(None, 28)
        self.fuente_mini = pygame.font.Font(None, 22)

        # Estado
        self.caso = "A"
        self.oponente_tipo = "aleatorio"
        self.velocidad = 1.0
        self.agente = None
        self.juego = None
        self.en_pausa = False
        self.partida_terminada = False
        self.estado_juego = None
        self.ultimo_movimiento = None
        self.turnos = 0
        self.resultado = None
        self.delay_movimiento = 0  # Contador para ralentizar movimientos
        self.frames_por_movimiento = 90  # ~1.5 segundos entre movimientos (60 FPS)

        # Cargar agente
        self.cargar_agente()

    def cargar_agente(self):
        """Carga el agente entrenado"""
        archivo = f"agente_caso_{self.caso}_QLEARNING.pkl"
        if not os.path.exists(archivo):
            print(f"Error: No se encontró {archivo}")
            print("Ejecuta primero el entrenamiento con opción 1")
            pygame.quit()
            sys.exit()

        self.agente = AgenteQLearning()
        self.agente.cargar(archivo)
        self.agente.epsilon = 0  # Sin exploración

    def cambiar_caso(self, caso):
        """Cambia entre Caso A y Caso B"""
        self.caso = caso
        self.cargar_agente()
        self.iniciar_partida()

    def cambiar_oponente(self, tipo):
        """Cambia el tipo de oponente"""
        self.oponente_tipo = tipo
        self.iniciar_partida()

    def iniciar_partida(self):
        """Inicia una nueva partida"""
        n = 4 if self.caso == "A" else 5
        con_peon = self.caso == "B"

        self.juego = AjedrezSimple(n=n, con_peon=con_peon)
        self.estado_juego = self.juego.reset()

        if self.oponente_tipo == "aleatorio":
            self.oponente = OponenteAleatorio()
        else:
            self.oponente = OponenteGreedy()

        self.en_pausa = False
        self.partida_terminada = False
        self.ultimo_movimiento = None
        self.turnos = 0
        self.resultado = None

    def dibujar_tablero(self):
        """Dibuja el tablero de ajedrez"""
        if self.juego is None:
            return

        n = self.juego.n
        offset_x = (ANCHO_VENTANA - n * TAMANO_CELDA) // 2
        offset_y = 150

        for i in range(n):
            for j in range(n):
                color = CREMA if (i + j) % 2 == 0 else MARRON
                rect = pygame.Rect(
                    offset_x + j * TAMANO_CELDA,
                    offset_y + i * TAMANO_CELDA,
                    TAMANO_CELDA,
                    TAMANO_CELDA,
                )
                pygame.draw.rect(self.pantalla, color, rect)

                # Dibujar piezas
                pieza = self.juego.tablero[i, j]
                if pieza != 0:
                    self.dibujar_pieza(pieza, rect.centerx, rect.centery)

        # Resaltar último movimiento
        if self.ultimo_movimiento:
            (fi, fj), (ti, tj) = self.ultimo_movimiento
            # Origen en azul claro
            rect_origen = pygame.Rect(
                offset_x + fj * TAMANO_CELDA + 5,
                offset_y + fi * TAMANO_CELDA + 5,
                TAMANO_CELDA - 10,
                TAMANO_CELDA - 10,
            )
            pygame.draw.rect(self.pantalla, AZUL_CLARO, rect_origen, 6)

            # Destino en verde brillante
            rect_destino = pygame.Rect(
                offset_x + tj * TAMANO_CELDA + 5,
                offset_y + ti * TAMANO_CELDA + 5,
                TAMANO_CELDA - 10,
                TAMANO_CELDA - 10,
            )
            pygame.draw.rect(self.pantalla, VERDE_BRILLANTE, rect_destino, 6)

    def dibujar_pieza(self, pieza, x, y):
        """Dibuja una pieza usando texto claro (R=Rey, T=Torre, P=Peon) con colores muy visibles"""
        # Usar letras en lugar de símbolos Unicode
        if abs(pieza) == 1:
            nombre = "R"  # Rey
        elif abs(pieza) == 2:
            nombre = "T"  # Torre
        elif abs(pieza) == 3:
            nombre = "P"  # Peón
        else:
            return

        if pieza > 0:  # Piezas AGENTE (Blancas)
            # Sombra oscura para profundidad
            sombra = self.fuente_grande.render(nombre, True, (100, 100, 100))
            rect_sombra = sombra.get_rect(center=(x + 3, y + 3))
            self.pantalla.blit(sombra, rect_sombra)

            # Borde negro grueso para contraste
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx != 0 or dy != 0:
                        borde = self.fuente_grande.render(nombre, True, NEGRO)
                        rect_borde = borde.get_rect(center=(x + dx, y + dy))
                        self.pantalla.blit(borde, rect_borde)

            # Pieza principal en BLANCO
            color_pieza = (255, 255, 255)  # Blanco puro
            texto = self.fuente_grande.render(nombre, True, color_pieza)

        else:  # Piezas OPONENTE (Negras)
            # Sombra clara para profundidad
            sombra = self.fuente_grande.render(nombre, True, (100, 100, 100))
            rect_sombra = sombra.get_rect(center=(x + 3, y + 3))
            self.pantalla.blit(sombra, rect_sombra)

            # Borde blanco grueso para contraste
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx != 0 or dy != 0:
                        borde = self.fuente_grande.render(nombre, True, BLANCO)
                        rect_borde = borde.get_rect(center=(x + dx, y + dy))
                        self.pantalla.blit(borde, rect_borde)

            # Pieza principal en NEGRO
            color_pieza = (30, 30, 30)  # Negro (casi puro para mejor visibilidad)
            texto = self.fuente_grande.render(nombre, True, color_pieza)

        # Dibujar pieza principal
        rect = texto.get_rect(center=(x, y))
        self.pantalla.blit(texto, rect)

    def dibujar_interfaz(self):
        """Dibuja la interfaz de usuario mejorada"""
        # Fondo con gradiente simulado
        self.pantalla.fill(GRIS_FONDO)

        # Barra superior con título
        pygame.draw.rect(self.pantalla, AZUL_OSCURO, (0, 0, ANCHO_VENTANA, 120))

        # Título principal
        titulo = f"Caso {self.caso} ({'4x4' if self.caso == 'A' else '5x5'})"
        texto_titulo = self.fuente_titulo.render(titulo, True, AMARILLO_ORO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, 35))
        self.pantalla.blit(texto_titulo, rect_titulo)

        # Subtítulo con oponente
        subtitulo = f"Q-Learning vs {self.oponente_tipo.capitalize()}"
        texto_sub = self.fuente_mediana.render(subtitulo, True, BLANCO)
        rect_sub = texto_sub.get_rect(center=(ANCHO_VENTANA // 2, 80))
        self.pantalla.blit(texto_sub, rect_sub)

        # Panel izquierdo - Info del juego
        panel_izq = pygame.Rect(20, 140, 200, 250)
        pygame.draw.rect(self.pantalla, BLANCO, panel_izq, border_radius=10)
        pygame.draw.rect(self.pantalla, AZUL_OSCURO, panel_izq, 3, border_radius=10)

        # Turno actual
        turno_texto = f"Turno: {self.turnos}"
        texto = self.fuente_mediana.render(turno_texto, True, AZUL_OSCURO)
        self.pantalla.blit(texto, (40, 160))

        # Jugador actual
        if not self.partida_terminada:
            jugador = "AGENTE" if self.juego.turno == 1 else "OPONENTE"
            color_jugador = VERDE_BRILLANTE if self.juego.turno == 1 else ROJO_BRILLANTE
            texto_jugador = self.fuente_pequena.render("Jugando:", True, NEGRO)
            self.pantalla.blit(texto_jugador, (40, 210))
            texto_jug = self.fuente_mediana.render(jugador, True, color_jugador)
            self.pantalla.blit(texto_jug, (40, 240))

        # Leyenda de piezas debajo del panel izquierdo
        # Calcular altura dinámica basada en el caso
        if self.caso == "B":
            altura_leyenda = 265  # Más espacio para 3+3 piezas (agente + oponente)
        else:
            altura_leyenda = 200  # Espacio para 2+2 piezas

        panel_leyenda = pygame.Rect(20, 410, 225, altura_leyenda)
        pygame.draw.rect(self.pantalla, BLANCO, panel_leyenda, border_radius=10)
        pygame.draw.rect(self.pantalla, AZUL_OSCURO, panel_leyenda, 3, border_radius=10)

        # Título
        titulo_leyenda = self.fuente_mediana.render("PIEZAS", True, AZUL_OSCURO)
        self.pantalla.blit(titulo_leyenda, (70, 420))

        # AGENTE (Amarillo dorado) - Piezas Blancas
        y_base = 450
        texto_agente = self.fuente_pequena.render(
            "AGENTE (Blancas):", True, AZUL_OSCURO
        )
        self.pantalla.blit(texto_agente, (30, y_base))

        # Rey
        y_base += 30
        pygame.draw.circle(self.pantalla, (255, 255, 255), (45, y_base), 8)
        pygame.draw.circle(self.pantalla, NEGRO, (45, y_base), 8, 2)
        rey_texto = self.fuente_pequena.render("= Rey", True, NEGRO)
        self.pantalla.blit(rey_texto, (60, y_base - 7))

        # Torre
        y_base += 25
        pygame.draw.circle(self.pantalla, (255, 255, 255), (45, y_base), 8)
        pygame.draw.circle(self.pantalla, NEGRO, (45, y_base), 8, 2)
        torre_texto = self.fuente_pequena.render("= Torre", True, NEGRO)
        self.pantalla.blit(torre_texto, (60, y_base - 7))

        # Peón (solo Caso B)
        if self.caso == "B":
            y_base += 25
            pygame.draw.circle(self.pantalla, (255, 255, 255), (45, y_base), 8)
            pygame.draw.circle(self.pantalla, NEGRO, (45, y_base), 8, 2)
            peon_texto = self.fuente_pequena.render("= Peon", True, NEGRO)
            self.pantalla.blit(peon_texto, (60, y_base - 7))

        # OPONENTE (Rojo oscuro) - Piezas Negras
        y_base += 35
        texto_oponente = self.fuente_pequena.render(
            "OPONENTE (Negras):", True, AZUL_OSCURO
        )
        self.pantalla.blit(texto_oponente, (30, y_base))

        # Rey oponente
        y_base += 30
        pygame.draw.circle(self.pantalla, (30, 30, 30), (45, y_base), 8)
        pygame.draw.circle(self.pantalla, BLANCO, (45, y_base), 8, 2)
        rey_negro_texto = self.fuente_pequena.render("= Rey", True, NEGRO)
        self.pantalla.blit(rey_negro_texto, (60, y_base - 7))

        # Torre oponente
        y_base += 25
        pygame.draw.circle(self.pantalla, (30, 30, 30), (45, y_base), 8)
        pygame.draw.circle(self.pantalla, BLANCO, (45, y_base), 8, 2)
        torre_negra_texto = self.fuente_pequena.render("= Torre", True, NEGRO)
        self.pantalla.blit(torre_negra_texto, (60, y_base - 7))

        # Peón oponente (solo Caso B)
        if self.caso == "B":
            y_base += 25
            pygame.draw.circle(self.pantalla, (30, 30, 30), (45, y_base), 8)
            pygame.draw.circle(self.pantalla, BLANCO, (45, y_base), 8, 2)
            peon_negro_texto = self.fuente_pequena.render("= Peon", True, NEGRO)
            self.pantalla.blit(peon_negro_texto, (60, y_base - 7))

        # Panel derecho - Controles
        panel_der = pygame.Rect(ANCHO_VENTANA - 250, 140, 230, 360)
        pygame.draw.rect(self.pantalla, BLANCO, panel_der, border_radius=10)
        pygame.draw.rect(self.pantalla, AZUL_OSCURO, panel_der, 3, border_radius=10)

        # Título de controles
        titulo_ctrl = self.fuente_mediana.render("CONTROLES", True, AZUL_OSCURO)
        self.pantalla.blit(titulo_ctrl, (ANCHO_VENTANA - 235, 155))

        # Lista de controles con mejor formato
        controles = [
            ("ESPACIO", "Pausar"),
            ("R", "Reiniciar"),
            ("A", "Caso A (4x4)"),
            ("B", "Caso B (5x5)"),
            ("O", "Cambiar rival"),
            ("Q", "Salir"),
        ]

        y_pos = 205
        for tecla, accion in controles:
            # Dibujar tecla
            texto_tecla = self.fuente_pequena.render(tecla, True, BLANCO)
            rect_tecla = pygame.Rect(ANCHO_VENTANA - 235, y_pos, 60, 30)
            pygame.draw.rect(self.pantalla, AZUL_OSCURO, rect_tecla, border_radius=5)
            rect_texto = texto_tecla.get_rect(center=rect_tecla.center)
            self.pantalla.blit(texto_tecla, rect_texto)

            # Dibujar acción
            texto_accion = self.fuente_mini.render(accion, True, NEGRO)
            self.pantalla.blit(texto_accion, (ANCHO_VENTANA - 165, y_pos + 5))
            y_pos += 50

        # Dibujar tablero
        self.dibujar_tablero()

        # Estado de la partida
        if self.partida_terminada:
            self.dibujar_resultado()
        elif self.en_pausa:
            # Panel de pausa grande y visible
            n = self.juego.n
            offset_y = 180 + n * TAMANO_CELDA // 2
            panel_pausa = pygame.Rect(ANCHO_VENTANA // 2 - 150, offset_y - 50, 300, 100)
            pygame.draw.rect(self.pantalla, AMARILLO_ORO, panel_pausa, border_radius=15)
            pygame.draw.rect(
                self.pantalla, AZUL_OSCURO, panel_pausa, 5, border_radius=15
            )

            texto = self.fuente_titulo.render("PAUSA", True, AZUL_OSCURO)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, offset_y))
            self.pantalla.blit(texto, rect)

    def dibujar_resultado(self):
        """Dibuja el resultado de la partida con estilo mejorado"""
        if self.resultado:
            # Panel de resultado grande - posición fija en la parte inferior
            # para que siempre sea visible sin importar el tamaño del tablero
            offset_y = ALTO_VENTANA - 180

            panel_resultado = pygame.Rect(150, offset_y, ANCHO_VENTANA - 300, 140)
            pygame.draw.rect(self.pantalla, BLANCO, panel_resultado, border_radius=15)

            # Color según resultado
            if "GANA" in self.resultado:
                color_borde = VERDE_BRILLANTE
                color_texto = VERDE_BRILLANTE
            else:
                color_borde = ROJO_BRILLANTE
                color_texto = ROJO_BRILLANTE

            pygame.draw.rect(
                self.pantalla, color_borde, panel_resultado, 5, border_radius=15
            )

            # Texto del resultado
            texto = self.fuente_titulo.render(self.resultado, True, color_texto)
            rect = texto.get_rect(center=(ANCHO_VENTANA // 2, offset_y + 45))
            self.pantalla.blit(texto, rect)

            # Mensaje para reiniciar con ícono
            msg = "Presiona R para nueva partida"
            texto2 = self.fuente_mediana.render(msg, True, AZUL_OSCURO)
            rect2 = texto2.get_rect(center=(ANCHO_VENTANA // 2, offset_y + 95))
            self.pantalla.blit(texto2, rect2)

    def actualizar_juego(self):
        """Actualiza el estado del juego con delay para visualización"""
        if self.partida_terminada or self.en_pausa:
            return

        # Control de velocidad - esperar entre movimientos
        if self.delay_movimiento > 0:
            self.delay_movimiento -= 1
            return

        # Resetear delay después de cada movimiento
        self.delay_movimiento = self.frames_por_movimiento

        # Turno del agente (blanco)
        if self.juego.turno == 1:
            acciones = self.juego.obtener_acciones_legales()
            if not acciones:
                self.resultado = "Empate - Sin movimientos"
                self.partida_terminada = True
                return

            accion = self.agente.elegir_accion(self.estado_juego, acciones)
            self.ultimo_movimiento = accion
            self.estado_juego, recompensa, terminado = self.juego.hacer_movimiento(
                accion
            )
            self.turnos += 1

            if terminado:
                if recompensa > 50:
                    self.resultado = f"¡Agente GANA en {self.turnos} turnos!"
                else:
                    self.resultado = "Oponente gana"
                self.partida_terminada = True
                return

        # Turno del oponente (negro)
        else:
            acciones = self.juego.obtener_acciones_legales()
            if not acciones:
                self.resultado = "Empate - Sin movimientos"
                self.partida_terminada = True
                return

            accion = self.oponente.elegir_accion(self.juego)
            if accion:
                self.ultimo_movimiento = accion
                self.estado_juego, _, terminado = self.juego.hacer_movimiento(accion)

                if terminado:
                    self.resultado = "Oponente gana"
                    self.partida_terminada = True
                    return

    def manejar_eventos(self):
        """Maneja eventos de teclado"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    return False
                elif evento.key == pygame.K_SPACE:
                    self.en_pausa = not self.en_pausa
                elif evento.key == pygame.K_r:
                    self.iniciar_partida()
                elif evento.key == pygame.K_a:
                    self.cambiar_caso("A")
                elif evento.key == pygame.K_b:
                    self.cambiar_caso("B")
                elif evento.key == pygame.K_o:
                    nuevo_oponente = (
                        "greedy" if self.oponente_tipo == "aleatorio" else "aleatorio"
                    )
                    self.cambiar_oponente(nuevo_oponente)

        return True

    def ejecutar(self):
        """Bucle principal"""
        self.iniciar_partida()
        ejecutando = True

        while ejecutando:
            ejecutando = self.manejar_eventos()

            # Actualizar juego
            self.actualizar_juego()

            # Dibujar
            self.dibujar_interfaz()
            pygame.display.flip()

            # Control de velocidad (60 FPS para suavidad, delay controla velocidad de juego)
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()


# ============================================================================
# EJECUCION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("DEMO INTERACTIVO - AJEDREZ Q-LEARNING")
    print("=" * 80)
    print("\nCargando interfaz gráfica...")

    visualizador = VisualizadorPygame()
    visualizador.ejecutar()
