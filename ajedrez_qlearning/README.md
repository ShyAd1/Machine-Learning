# Ajedrez Q-Learning - Sistema Automatizado

Sistema de entrenamiento y visualización de agentes de Q-Learning para ajedrez simplificado.

## Características

- **Interfaz Pygame**: Visualización interactiva de partidas
- **Análisis completo**: Gráficas, métricas y estadísticas
- **Curriculum suave**: Entrenamiento progresivo optimizado
- **Multi-candidato**: Entrena 10 agentes y elige el mejor

## Casos de Juego

- **Caso A (4x4)**: Rey + Torre vs Rey + Torre
- **Caso B (5x5)**: Rey + Torre + Peón vs Rey + Torre

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### 1. Entrenamiento Automatizado

Ejecuta el sistema completo:

```bash
python sistema_completo_competitivo.py
```

**Menú:**

- `1`: Entrenamiento completo (30-40 min)
- `2`: Demo visual con Pygame
- `3`: Salir

### 2. Demo Visual (Pygame)

Después de entrenar, ejecuta:

```bash
python demo_pygame.py
```

**Controles:**

- `ESPACIO`: Pausar/Reanudar
- `R`: Reiniciar partida
- `A`: Caso A (4x4)
- `B`: Caso B (5x5)
- `O`: Cambiar oponente (Aleatorio/Greedy)
- `Q`: Salir

## Archivos Generados

```
agente_caso_A_QLEARNING.pkl   # Agente entrenado 4x4
agente_caso_B_QLEARNING.pkl   # Agente entrenado 5x5
graficas/                      # 7 gráficas de análisis
```

## Resultados Esperados

**Caso A (4x4):**

- vs Aleatorio: ~95-100%
- vs Greedy: ~70-85%
- Turnos promedio: ~8-12

**Caso B (5x5):**

- vs Aleatorio: ~90-95%
- vs Greedy: ~65-80%
- Turnos promedio: ~12-18

## Configuración del Curriculum

El sistema usa un **curriculum suave** para entrenamiento:

```python
# Primeros 70% episodios: Solo oponente aleatorio (aprende lo básico)
# Últimos 30% episodios: Gradualmente 0% → 30% Greedy (desafío progresivo)
```

Esto permite que el agente:

1. Aprenda estrategias básicas sin frustración
2. Se enfrente a desafíos solo cuando está preparado
3. Converja más rápido y mejor

## Métricas de Evaluación

- **Tasa de victoria**: % de partidas ganadas
- **Turnos promedio**: Eficiencia en victorias
- **Score**: `tasa * 0.6 - turnos * 2` (equilibrio velocidad/efectividad)

## Sistema Multi-Candidato

El sistema entrena **10 candidatos** por caso y selecciona automáticamente el mejor basándose en:

1. Tasa de victoria vs Greedy (60%)
2. Velocidad de victoria (40%)

## Interfaz Pygame

La interfaz muestra:

- Tablero visual con piezas
- Último movimiento resaltado
- Información de turno y jugador
- Controles interactivos
- Resultado de la partida

## Notas Técnicas

**Parámetros optimizados:**

- `alpha=0.15`: Tasa de aprendizaje balanceada
- `gamma=0.98`: Prioriza victorias a largo plazo
- `epsilon`: 0.4 → 0.05 (decay progresivo)

**Recompensas ajustadas:**

- Victoria: 100 + bonus velocidad
- Movimiento normal: -0.5 (penaliza lentitud)
- Derrota: -100

## Solución de Problemas

**"No se encontró agente_caso_X_QLEARNING.pkl"**

- Ejecuta primero la opción 1 (entrenamiento)

**"Pygame no está instalado"**

- `pip install pygame`

**Agente no gana nada**

- Verifica que el curriculum esté configurado correctamente
- Asegúrate de que epsilon se restaura después de evaluación

## Autor

Sistema de Q-Learning para ajedrez simplificado con análisis competitivo.
