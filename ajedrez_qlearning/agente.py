import random
import numpy as np

class AgenteQLearning:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.3):
        self.Q = {}  # Q-table: (estado, accion) -> valor
        self.alpha = alpha      # Tasa de aprendizaje
        self.gamma = gamma      # Factor de descuento
        self.epsilon = epsilon  # Exploración
    
    def obtener_Q(self, estado, accion):
        """Obtiene el valor Q para (estado, acción)"""
        # Convertir acción a tupla para usarla como key
        accion_key = (accion[0], accion[1])
        key = (estado, accion_key)
        return self.Q.get(key, 0.0)
    
    def elegir_accion(self, estado, acciones_legales):
        """Elige acción usando epsilon-greedy"""
        if not acciones_legales:
            return None
        
        # Exploración: acción aleatoria
        if random.random() < self.epsilon:
            return random.choice(acciones_legales)
        
        # Explotación: mejor acción conocida
        valores_Q = [self.obtener_Q(estado, a) for a in acciones_legales]
        max_Q = max(valores_Q)
        
        # Si hay empate, elegir aleatoria entre las mejores
        mejores = [a for a, q in zip(acciones_legales, valores_Q) if q == max_Q]
        return random.choice(mejores)
    
    def actualizar(self, estado, accion, recompensa, siguiente_estado, siguientes_acciones):
        """Actualiza Q-table usando la fórmula de Q-learning"""
        # Q actual
        Q_actual = self.obtener_Q(estado, accion)
        
        # Mejor Q en el siguiente estado
        if siguientes_acciones:
            Q_siguiente_max = max([self.obtener_Q(siguiente_estado, a) 
                                   for a in siguientes_acciones])
        else:
            Q_siguiente_max = 0
        
        # Fórmula de Q-learning
        Q_nuevo = Q_actual + self.alpha * (
            recompensa + self.gamma * Q_siguiente_max - Q_actual
        )
        
        # Guardar
        accion_key = (accion[0], accion[1])
        self.Q[(estado, accion_key)] = Q_nuevo
    
    def guardar(self, filename):
        """Guarda la Q-table en un archivo"""
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.Q, f)
        print(f"Q-table guardada en {filename}")
    
    def cargar(self, filename):
        """Carga la Q-table desde un archivo"""
        import pickle
        with open(filename, 'rb') as f:
            self.Q = pickle.load(f)
        print(f"Q-table cargada desde {filename}")

class AgenteSARSA:
    """
    Agente SARSA (State-Action-Reward-State-Action)
    Diferencia clave: aprende de la acción que REALMENTE tomará (on-policy)
    """
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.3):
        self.Q = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
    
    def obtener_Q(self, estado, accion):
        accion_key = (accion[0], accion[1])
        key = (estado, accion_key)
        return self.Q.get(key, 0.0)
    
    def elegir_accion(self, estado, acciones_legales):
        if not acciones_legales:
            return None
        
        if random.random() < self.epsilon:
            return random.choice(acciones_legales)
        
        valores_Q = [self.obtener_Q(estado, a) for a in acciones_legales]
        max_Q = max(valores_Q)
        mejores = [a for a, q in zip(acciones_legales, valores_Q) if q == max_Q]
        return random.choice(mejores)
    
    def actualizar(self, estado, accion, recompensa, siguiente_estado, siguiente_accion):
        """
        DIFERENCIA CLAVE: recibe siguiente_accion en lugar de siguientes_acciones
        """
        Q_actual = self.obtener_Q(estado, accion)
        
        # SARSA: usa la acción que REALMENTE tomará
        if siguiente_accion is not None:
            Q_siguiente = self.obtener_Q(siguiente_estado, siguiente_accion)
        else:
            Q_siguiente = 0
        
        Q_nuevo = Q_actual + self.alpha * (
            recompensa + self.gamma * Q_siguiente - Q_actual
        )
        
        accion_key = (accion[0], accion[1])
        self.Q[(estado, accion_key)] = Q_nuevo
    
    def guardar(self, filename):
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.Q, f)
        print(f"Q-table guardada en {filename}")
    
    def cargar(self, filename):
        import pickle
        with open(filename, 'rb') as f:
            self.Q = pickle.load(f)
        print(f"Q-table cargada desde {filename}")