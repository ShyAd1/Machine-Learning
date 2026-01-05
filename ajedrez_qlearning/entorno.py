import numpy as np

class AjedrezSimple:
    def __init__(self, n=4, con_peon=False):
        """
        n: tamaño del tablero (4 o 5)
        con_peon: True para incluir peones (Caso B)
        """
        self.n = n
        self.con_peon = con_peon
        self.reset()
    
    def reset(self):
        """Reinicia el juego a posición inicial"""
        self.tablero = np.zeros((self.n, self.n), dtype=int)
        
        # Piezas:
        # 1 = rey blanco, 2 = torre blanca, 3 = peon blanco
        # 4 = reina blanca, 5 = alfil blanco, 6 = caballo blanco
        # -1 = rey negro, -2 = torre negra, -3 = peon negro
        # -4 = reina negra, -5 = alfil negro, -6 = caballo negro
        if self.n == 4:
            # Caso A: 4x4 con Rey + Torre
            self.tablero[3, 0] = 1   # Rey blanco
            self.tablero[3, 3] = 2   # Torre blanca
            self.tablero[0, 0] = -1  # Rey negro
            self.tablero[0, 3] = -2  # Torre negra
        else:  # 5x5
            # Caso B: 5x5 con Rey + Torre + Peon
            self.tablero[4, 0] = 1   # Rey blanco
            self.tablero[4, 4] = 2   # Torre blanca
            self.tablero[4, 2] = 3   # Peon blanco
            self.tablero[0, 0] = -1  # Rey negro
            self.tablero[0, 4] = -2  # Torre negra
            self.tablero[0, 2] = -3  # Peon negro
        # if self.n == 4:
        #     # Caso A: 4x4 con Rey + Torre
        #     # 1-rey negro, 3-torre negra, 14-torre blanca, 16-rey blanco
            
        #     # Posición 1: (0, 0) -> Rey negro
        #     self.tablero[0, 0] = -1
            
        #     # Posición 3: (0, 2) -> Torre negra
        #     self.tablero[0, 2] = -2
            
        #     # Posición 14: (3, 1) -> Torre blanca
        #     self.tablero[3, 1] = 2
            
        #     # Posición 16: (3, 3) -> Rey blanco
        #     self.tablero[3, 3] = 1
            
        # else:  # 5x5
        #     # Caso B: 5x5 con Rey + Torre + Peon
        #     # 2-torre negra, 3-rey negro, 4-peón negro
        #     # 22-peón blanco, 23-rey blanco, 24-torre blanca
            
        #     # Posición 2: (0, 1) -> Torre negra
        #     self.tablero[0, 1] = -2
            
        #     # Posición 3: (0, 2) -> Rey negro
        #     self.tablero[0, 2] = -1
            
        #     # Posición 4: (0, 3) -> Peón negro
        #     self.tablero[0, 3] = -3
            
        #     # Posición 22: (4, 1) -> Peón blanco
        #     self.tablero[4, 1] = 3
            
        #     # Posición 23: (4, 2) -> Rey blanco
        #     self.tablero[4, 2] = 1
            
        #     # Posición 24: (4, 3) -> Torre blanca
        #     self.tablero[4, 3] = 2
        
        self.turno = 1  # 1 = blanco, -1 = negro
        self.peones_coronados = []
        return self.get_estado()
    
    def get_estado(self):
        """Convierte el tablero a tupla"""
        return tuple(self.tablero.flatten()) + (self.turno,)
    
    def obtener_movimientos_rey(self, fila, col):
        """Movimientos legales del rey (8 direcciones, 1 casilla)"""
        movimientos = []
        
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                
                nueva_fila = fila + df
                nueva_col = col + dc
                
                if 0 <= nueva_fila < self.n and 0 <= nueva_col < self.n:
                    pieza_destino = self.tablero[nueva_fila, nueva_col]
                    
                    if self.turno == 1:  # Blanco
                        if pieza_destino <= 0:
                            movimientos.append((nueva_fila, nueva_col))
                    else:  # Negro
                        if pieza_destino >= 0:
                            movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
    
    def obtener_movimientos_torre(self, fila, col):
        """Movimientos legales de la torre (lineas rectas)"""
        movimientos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila, col
            
            while True:
                nueva_fila += df
                nueva_col += dc
                
                if not (0 <= nueva_fila < self.n and 0 <= nueva_col < self.n):
                    break
                
                pieza_destino = self.tablero[nueva_fila, nueva_col]
                
                if pieza_destino == 0:
                    movimientos.append((nueva_fila, nueva_col))
                elif (self.turno == 1 and pieza_destino < 0) or \
                     (self.turno == -1 and pieza_destino > 0):
                    movimientos.append((nueva_fila, nueva_col))
                    break
                else:
                    break
        
        return movimientos
    
    def obtener_movimientos_peon(self, fila, col):
        """Movimientos legales del peon"""
        movimientos = []
        
        if self.turno == 1:  # Peon blanco (avanza hacia arriba)
            direccion = -1
            fila_inicial = self.n - 2
        else:  # Peon negro (avanza hacia abajo)
            direccion = 1
            fila_inicial = 1
        
        # Movimiento hacia adelante (1 casilla)
        nueva_fila = fila + direccion
        if 0 <= nueva_fila < self.n:
            if self.tablero[nueva_fila, col] == 0:
                movimientos.append((nueva_fila, col))
                
                # Movimiento inicial de 2 casillas
                if fila == fila_inicial:
                    nueva_fila_2 = fila + 2 * direccion
                    if 0 <= nueva_fila_2 < self.n and self.tablero[nueva_fila_2, col] == 0:
                        movimientos.append((nueva_fila_2, col))
        
        # Captura en diagonal
        nueva_fila = fila + direccion
        for nueva_col in [col - 1, col + 1]:
            if 0 <= nueva_fila < self.n and 0 <= nueva_col < self.n:
                pieza_destino = self.tablero[nueva_fila, nueva_col]
                if (self.turno == 1 and pieza_destino < 0) or \
                   (self.turno == -1 and pieza_destino > 0):
                    movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
    
    # ========== NUEVAS PIEZAS ==========
    
    def obtener_movimientos_reina(self, fila, col):
        """Movimientos legales de la reina (torre + alfil)"""
        movimientos = []
        # Reina = 8 direcciones sin límite
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),      # Torre
            (-1, -1), (-1, 1), (1, -1), (1, 1)     # Alfil
        ]
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila, col
            
            while True:
                nueva_fila += df
                nueva_col += dc
                
                if not (0 <= nueva_fila < self.n and 0 <= nueva_col < self.n):
                    break
                
                pieza_destino = self.tablero[nueva_fila, nueva_col]
                
                if pieza_destino == 0:
                    movimientos.append((nueva_fila, nueva_col))
                elif (self.turno == 1 and pieza_destino < 0) or \
                     (self.turno == -1 and pieza_destino > 0):
                    movimientos.append((nueva_fila, nueva_col))
                    break
                else:
                    break
        
        return movimientos
    
    def obtener_movimientos_alfil(self, fila, col):
        """Movimientos legales del alfil (diagonales)"""
        movimientos = []
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila, col
            
            while True:
                nueva_fila += df
                nueva_col += dc
                
                if not (0 <= nueva_fila < self.n and 0 <= nueva_col < self.n):
                    break
                
                pieza_destino = self.tablero[nueva_fila, nueva_col]
                
                if pieza_destino == 0:
                    movimientos.append((nueva_fila, nueva_col))
                elif (self.turno == 1 and pieza_destino < 0) or \
                     (self.turno == -1 and pieza_destino > 0):
                    movimientos.append((nueva_fila, nueva_col))
                    break
                else:
                    break
        
        return movimientos
    
    def obtener_movimientos_caballo(self, fila, col):
        """Movimientos legales del caballo (movimiento en L)"""
        movimientos = []
        saltos = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for df, dc in saltos:
            nueva_fila = fila + df
            nueva_col = col + dc
            
            if 0 <= nueva_fila < self.n and 0 <= nueva_col < self.n:
                pieza_destino = self.tablero[nueva_fila, nueva_col]
                
                if self.turno == 1:  # Blanco
                    if pieza_destino <= 0:
                        movimientos.append((nueva_fila, nueva_col))
                else:  # Negro
                    if pieza_destino >= 0:
                        movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
    
    # ===================================
    
    def obtener_acciones_legales(self):
        """Retorna todas las acciones legales para el jugador actual"""
        acciones = []
        
        for fila in range(self.n):
            for col in range(self.n):
                pieza = self.tablero[fila, col]
                
                if self.turno == 1 and pieza > 0:  # Blanco
                    if pieza == 1:  # Rey
                        movs = self.obtener_movimientos_rey(fila, col)
                    elif pieza == 2:  # Torre
                        movs = self.obtener_movimientos_torre(fila, col)
                    elif pieza == 3:  # Peon
                        movs = self.obtener_movimientos_peon(fila, col)
                    elif pieza == 4:  # Reina
                        movs = self.obtener_movimientos_reina(fila, col)
                    elif pieza == 5:  # Alfil
                        movs = self.obtener_movimientos_alfil(fila, col)
                    elif pieza == 6:  # Caballo
                        movs = self.obtener_movimientos_caballo(fila, col)
                    else:
                        continue
                    
                    for destino in movs:
                        acciones.append(((fila, col), destino))
                
                elif self.turno == -1 and pieza < 0:  # Negro
                    if pieza == -1:  # Rey
                        movs = self.obtener_movimientos_rey(fila, col)
                    elif pieza == -2:  # Torre
                        movs = self.obtener_movimientos_torre(fila, col)
                    elif pieza == -3:  # Peon
                        movs = self.obtener_movimientos_peon(fila, col)
                    elif pieza == -4:  # Reina
                        movs = self.obtener_movimientos_reina(fila, col)
                    elif pieza == -5:  # Alfil
                        movs = self.obtener_movimientos_alfil(fila, col)
                    elif pieza == -6:  # Caballo
                        movs = self.obtener_movimientos_caballo(fila, col)
                    else:
                        continue
                    
                    for destino in movs:
                        acciones.append(((fila, col), destino))
        
        return acciones
    
    def verificar_coronacion(self, fila, col):
        """Verifica si un peon debe coronar - AHORA CORONA A REINA (4)"""
        pieza = self.tablero[fila, col]
        
        if abs(pieza) == 3:  # Es un peon
            if pieza == 3 and fila == 0:  # Peon blanco llego arriba
                self.tablero[fila, col] = 4  # ← CAMBIO: Corona a REINA
                return True
            elif pieza == -3 and fila == self.n - 1:  # Peon negro llego abajo
                self.tablero[fila, col] = -4  # ← CAMBIO: Corona a REINA
                return True
        return False
    
    def hacer_movimiento(self, accion):
        """Ejecuta una accion y retorna (nuevo_estado, recompensa, terminado)"""
        desde, hasta = accion
        fila_desde, col_desde = desde
        fila_hasta, col_hasta = hasta
        
        pieza_capturada = self.tablero[fila_hasta, col_hasta]
        
        # Mover pieza
        self.tablero[fila_hasta, col_hasta] = self.tablero[fila_desde, col_desde]
        self.tablero[fila_desde, col_desde] = 0
        
        # Verificar coronacion
        corono = self.verificar_coronacion(fila_hasta, col_hasta)
        
        # Calcular recompensa
        recompensa = -0.1
        
        if pieza_capturada != 0:
            if abs(pieza_capturada) == 1:  # Rey
                recompensa = 100 if self.turno == 1 else -100
            elif abs(pieza_capturada) == 4:  # Reina (NUEVO)
                recompensa = 90 if self.turno == 1 else -90
            elif abs(pieza_capturada) == 2:  # Torre
                recompensa = 50 if self.turno == 1 else -50
            elif abs(pieza_capturada) == 5:  # Alfil (NUEVO)
                recompensa = 30 if self.turno == 1 else -30
            elif abs(pieza_capturada) == 6:  # Caballo (NUEVO)
                recompensa = 30 if self.turno == 1 else -30
            elif abs(pieza_capturada) == 3:  # Peon
                recompensa = 10 if self.turno == 1 else -10
        
        if corono:
            recompensa += 50 if self.turno == 1 else -50
        
        terminado = self.verificar_fin()
        self.turno *= -1
        
        return self.get_estado(), recompensa, terminado
    
    def verificar_fin(self):
        """Verifica si el juego termino"""
        tiene_rey_blanco = np.any(self.tablero == 1)
        tiene_rey_negro = np.any(self.tablero == -1)
        return not (tiene_rey_blanco and tiene_rey_negro)
    
    # def renderizar(self):
    #     """Muestra el tablero"""
    #     print("\n" + "="*(self.n * 4 + 1))
    #     simbolos = {
    #         0: "·",
    #         1: "♔", 2: "♖", 3: "♙", 4: "♕", 5: "♗", 6: "♘",
    #         -1: "♚", -2: "♜", -3: "♟", -4: "♛", -5: "♝", -6: "♞"
    #     }
        
    #     for fila in range(self.n):
    #         for col in range(self.n):
    #             pieza = self.tablero[fila, col]
    #             print(f" {simbolos[pieza]} ", end="")
    #         print()
    #     print("="*(self.n * 4 + 1))
    def renderizar(self):
        """Muestra el tablero con colores"""
        # Colores ANSI
        BLANCO_FONDO = "\033[47m"  # Fondo blanco
        NEGRO_FONDO = "\033[40m"   # Fondo negro
        TEXTO_NEGRO = "\033[30m"   # Texto negro
        TEXTO_BLANCO = "\033[37m"  # Texto blanco
        RESET = "\033[0m"
        
        simbolos = {
            0: " ",
            1: "♔", 2: "♖", 3: "♙", 4: "♕", 5: "♗", 6: "♘",
            -1: "♚", -2: "♜", -3: "♟", -4: "♛", -5: "♝", -6: "♞"
        }
        
        print("\n" + "="*(self.n * 4 + 1))
        
        for fila in range(self.n):
            for col in range(self.n):
                pieza = self.tablero[fila, col]
                simbolo = simbolos[pieza]
                
                # Alternar colores como tablero de ajedrez
                if (fila + col) % 2 == 0:
                    fondo = BLANCO_FONDO
                    texto = TEXTO_NEGRO
                else:
                    fondo = NEGRO_FONDO
                    texto = TEXTO_BLANCO
                
                # Imprimir celda con color
                print(f"{fondo}{texto} {simbolo} {RESET}", end="")
            print()  # Salto de línea
        
        print("="*(self.n * 4 + 1))