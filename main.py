#!/usr/bin/env python3
"""
Juego de Triqui (Tic-Tac-Toe) con MCTS
Juega contra la computadora que usa Monte Carlo Tree Search
"""

from triqui import TicTacToeBoard, Player
from mcts import MCTS

class TriquiGame:
    def __init__(self):
        self.board = TicTacToeBoard()
        self.mcts = MCTS(self.board, Player.MACHINE)
        self.game_over = False

    def print_instructions(self):
        print("="*50)
        print("     ¡BIENVENIDO AL TRIQUI CON MCTS!")
        print("="*50)
        print("\nInstrucciones:")
        print("- Tú eres X, MCTS es O")
        print("- Ingresa el número de la posición donde quieres jugar (0-8)")
        print("- Las posiciones están numeradas así:")
        print("\n 0 | 1 | 2 ")
        print("___|___|___")
        print(" 3 | 4 | 5 ")
        print("___|___|___")
        print(" 6 | 7 | 8 ")
        print("   |   |   ")
        
        while True:
            ready = input("\n¿Estás listo para jugar? (s/n): ").lower().strip()
            if ready in ['s', 'si', 'sí', 'y', 'yes']:
                break
            elif ready in ['n', 'no']:
                print("¡Está bien! Presiona Enter cuando estés listo...")
                input()
                continue
            else:
                print("Por favor responde 's' para sí o 'n' para no.")

        print("\n¡Empecemos!\n")

    def get_human_move(self):
        while True:
            try:
                self.board.print_board()
                print(f"\nPosiciones disponibles: {self.board.get_legal_positions()}")
                move = input("Ingresa tu movimiento (0-8) o 'q' para salir: ").strip()
                
                if move.lower() == 'q':
                    return None
                
                move = int(move)
                if 0 <= move <= 8:                    
                    if self.board.human_make_move(move):
                        return move
                    else:
                        print("¡Esa posición ya está ocupada!")
                else:
                    print("¡Por favor ingresa un número entre 0 y 8!")
            except ValueError:
                print("¡Por favor ingresa un número válido!")

    def make_machine_move(self, show_analysis=False, show_tree=False):
        # print("\nLa máquina está pensando...")
        
        # MCTS para el estado actual
        current_mcts = MCTS(self.board.copy(), Player.MACHINE)
        result = current_mcts.run_search(iterations=1000, show_progress=show_analysis)
        
        # Mostrar estructura del árbol si se solicita
        if show_tree:
            current_mcts.print_tree_structure(max_depth=3)
        
        if result and result["move"]:
            move = result["move"]
            print(f"La máquina juega en la posición {move.position}")
            self.board.make_move(move)
            return True
        
        return False

    def check_game_over(self):
        winner = self.board.check_win()
        
        if winner == "h":
            self.board.print_board()
            print("\n¡FELICIDADES! ¡Le has ganado a MCTS!")
            return True
        elif winner == "m":
            self.board.print_board()
            print("\nMCTS ha ganado. ¡Mejor suerte la próxima vez!")
            return True
        elif winner == "v":
            self.board.print_board()
            print("\n¡Es un empate! Buen juego.")
            return True
        
        return False

    def play(self):
        self.print_instructions()
          # Pregunta si quiere ver el análisis de MCTS
        while True:
            analysis = input("¿Quieres ver el análisis detallado de MCTS en cada jugada? (s/n): ").lower().strip()
            if analysis in ['s', 'si', 'sí', 'y', 'yes']:
                show_analysis = True
                break
            elif analysis in ['n', 'no']:
                show_analysis = False
                break
            else:
                print("Por favor responde 's' para sí o 'n' para no.")
        
        # Pregunta si quiere ver la estructura del árbol de MCTS
        show_tree = False
        if show_analysis:
            while True:
                tree = input("¿También quieres ver la estructura del árbol de búsqueda MCTS? (s/n): ").lower().strip()
                if tree in ['s', 'si', 'sí', 'y', 'yes']:
                    show_tree = True
                    break
                elif tree in ['n', 'no']:
                    show_tree = False
                    break
                else:
                    print("Por favor responde 's' para sí o 'n' para no.")
        
        while not self.game_over:
            # Turno del humano
            human_move = self.get_human_move()
            if human_move is None:
                print("¡Gracias por jugar!")
                return
            
            # Verificar si el juego terminó después del movimiento humano
            if self.check_game_over():
                break
              # Turno de la máquina
            if not self.make_machine_move(show_analysis, show_tree):
                print("Error: La máquina no pudo hacer un movimiento.")
                break
            
            # Verificar si el juego terminó después del movimiento de la máquina
            if self.check_game_over():
                break

    def play_again(self):
        while True:
            choice = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
            if choice in ['s', 'si', 'sí', 'y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Por favor responde 's' para sí o 'n' para no.")

def main():
    print("Iniciando el juego de Triqui con MCTS...")
    
    while True:
        game = TriquiGame()
        game.play()
        
        if not game.play_again():
            print("\n¡Gracias por jugar Triqui con MCTS!")
            break

if __name__ == "__main__":
    main()
