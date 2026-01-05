import random

class OponenteAleatorio:
    """Oponente que elige movimientos al azar"""
    def __init__(self):
        self.nombre = "Aleatorio"
    
    def elegir_accion(self, juego):
        acciones = juego.obtener_acciones_legales()
        if acciones:
            return random.choice(acciones)
        return None

class OponenteGreedy:
    """Oponente que prioriza capturas"""
    def __init__(self):
        self.nombre = "Greedy (captura si puede)"
    
    def elegir_accion(self, juego):
        acciones = juego.obtener_acciones_legales()
        if not acciones:
            return None
        
        # Evaluar cada acción
        mejores_acciones = []
        mejor_valor = -999
        
        for accion in acciones:
            desde, hasta = accion
            fila_hasta, col_hasta = hasta
            pieza_destino = juego.tablero[fila_hasta, col_hasta]
            
            # Calcular valor de la acción
            valor = 0
            
            if pieza_destino != 0:  # Hay captura
                if abs(pieza_destino) == 1:  # Rey
                    valor = 100
                elif abs(pieza_destino) == 4:  # Reina
                    valor = 90
                elif abs(pieza_destino) == 2:  # Torre
                    valor = 50  #20
                elif abs(pieza_destino) == 5:  # Alfil
                    valor = 30
                elif abs(pieza_destino) == 6:  # Caballo
                    valor = 30
                elif abs(pieza_destino) == 3:  # Peón
                    valor = 10
            
            # Guardar mejores acciones
            if valor > mejor_valor:
                mejor_valor = valor
                mejores_acciones = [accion]
            elif valor == mejor_valor:
                mejores_acciones.append(accion)
        
        # Si hay capturas, elegir una al azar
        # Si no hay capturas, todas tienen valor 0, elegir cualquiera
        return random.choice(mejores_acciones)