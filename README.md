# MCTS Triqui

Juego de Triqui (Tic-Tac-Toe) usando Monte Carlo Tree Search.

## Ejecución

```bash
python main.py
```

## Archivos

- `main.py` - Interfaz del juego
- `triqui.py` - Lógica del tablero
- `mcts.py` - Algoritmo MCTS
- `tree.py` - Estructura de árbol

## Funcionamiento

1. El jugador es X, MCTS es O
2. Posiciones numeradas del 0 al 8
3. MCTS ejecuta 1000 simulaciones por jugada
4. Opciones de visualización:
   - Análisis detallado de movimientos
   - Estructura del árbol de búsqueda

## MCTS

- **Selección**: UCB1 para elegir nodos
- **Expansión**: Añade un hijo aleatorio
- **Simulación**: Partidas aleatorias hasta el final
- **Retropropagación**: Actualiza valores hacia la raíz

## Métricas

- **Simulaciones**: Número de veces evaluado el movimiento
- **Victorias**: Valor neto (victorias - derrotas)
- **Tasa Win**: Porcentaje de victorias
- **UCB1**: Valor de confianza superior
