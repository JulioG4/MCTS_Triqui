import math
import random
from tree import Tree, Node
from triqui import GameMove, Player, get_other_player

class GameNode:
    def __init__(self, move):
        self.move = move
        self.value = 0
        self.simulations = 0

    def copy(self):
        new_game_node = GameNode(self.move.copy() if self.move else None)
        new_game_node.value = self.value
        new_game_node.simulations = self.simulations
        return new_game_node

def ucb1(node, parent):
    if node.data.simulations == 0:
        return float('inf')
    
    exploitation = node.data.value / node.data.simulations
    exploration = math.sqrt(2 * math.log(parent.data.simulations) / node.data.simulations)
    return exploitation + exploration

class MCTS:
    def __init__(self, model, player=Player.MACHINE):
        self.model = model
        root = Node(GameNode(GameMove(get_other_player(player), None)))
        self.tree = Tree(root)

    def run_search(self, iterations=50, show_progress=False):
        if show_progress:
            print(f"\n🔍 MCTS está pensando... ({iterations} simulaciones)")
            print("=" * 50)

        for i in range(iterations):
            self.run_search_iteration()
            
            # Mostrar progreso cada 200 iteraciones
            if show_progress and (i + 1) % 200 == 0:
                progress = (i + 1) / iterations * 100
                print(f"Progreso: {progress:.0f}% ({i + 1}/{iterations})")

        children = self.tree.get_children(self.tree.get(0))
        if not children:
            # If there are not children, make a random move
            legal_moves = self.model.get_legal_positions()
            if legal_moves:
                best_move = GameMove(Player.MACHINE, random.choice(legal_moves))
                return {"move": best_move}
            return None

        best_move_node = max(children, key=lambda x: x.data.simulations)
        
        if show_progress:
            self.print_search_results()
        
        return {"move": best_move_node.data.move}

    def run_search_iteration(self):
        select_res = self.select(self.model.copy())
        select_leaf = select_res["node"]
        select_model = select_res["model"]

        expand_res = self.expand(select_leaf, select_model)
        expand_leaf = expand_res["node"]
        expand_model = expand_res["model"]

        simulation = self.simulate(expand_leaf, expand_model)

        self.backpropagate(expand_leaf, simulation["winner_icon"])

    def get_best_child_ucb1(self, node):
        children = self.tree.get_children(node)
        if not children:
            return None
        
        node_scores = [(child, ucb1(child, node)) for child in children]
        return max(node_scores, key=lambda x: x[1])[0]

    def select(self, model):
        node = self.tree.get(0)

        while not node.is_leaf() and self.is_fully_explored(node, model):
            node = self.get_best_child_ucb1(node)
            if node is None:
                break
            model.make_move(node.data.move)

        return {"node": node, "model": model}

    def expand(self, node, model):
        expanded_node = None

        if model.check_win() == "":
            legal_positions = self.get_available_plays(node, model)
            if legal_positions:
                random_pos = random.choice(legal_positions)
                other_player = get_other_player(node.data.move.player)
                
                random_move = GameMove(other_player, random_pos)
                model.make_move(random_move)

                expanded_node = Node(GameNode(random_move))
                self.tree.insert(expanded_node, node)
            else:
                expanded_node = node
        else:
            expanded_node = node

        return {"node": expanded_node, "model": model}

    def simulate(self, node, model): # Rollout
        current_player = node.data.move.player

        while model.check_win() == "":
            current_player = get_other_player(current_player)
            model.make_random_move(current_player)

        winner_icon = model.check_win()

        return {
            "winner_icon": winner_icon
        }

    def backpropagate(self, node, winner):
        node.data.simulations += 1
        if not node.is_root():
            if ((node.data.move.player == Player.MACHINE and winner == "m") or
                (node.data.move.player == Player.HUMAN and winner == "h")):
                node.data.value += 1
            if ((node.data.move.player == Player.MACHINE and winner == "h") or
                (node.data.move.player == Player.HUMAN and winner == "m")):
                node.data.value -= 1
        
            self.backpropagate(self.tree.get_parent(node), winner)

    def is_fully_explored(self, node, model):
        return len(self.get_available_plays(node, model)) == 0

    def get_available_plays(self, node, model):
        children = self.tree.get_children(node)
        legal_positions = model.get_legal_positions()
        
        explored_positions = [child.data.move.position for child in children if child.data.move]
        return [pos for pos in legal_positions if pos not in explored_positions]

    def print_search_results(self):
        """Muestra un resumen visual de la búsqueda MCTS"""
        print("\n📊 RESULTADOS DE LA BÚSQUEDA MCTS")
        print("=" * 50)
        
        root = self.tree.get(0)
        children = self.tree.get_children(root)
        
        if not children:
            print("❌ No se encontraron movimientos posibles")
            return
        
        print(f"🌳 Total de simulaciones: {root.data.simulations}")
        print(f"🔢 Movimientos evaluados: {len(children)}")
        print()
        
        # Ordenar hijos por número de simulaciones (descendente)
        sorted_children = sorted(children, key=lambda x: x.data.simulations, reverse=True)
        
        print("🎯 ANÁLISIS DE MOVIMIENTOS:")
        print("-" * 50)
        print("Pos | Sims | Victorias | Tasa Win | UCB1  | Eval")
        print("-" * 50)
        
        for i, child in enumerate(sorted_children):
            pos = child.data.move.position
            sims = child.data.simulations
            wins = child.data.value
            win_rate = (wins / sims * 100) if sims > 0 else 0
            ucb1_val = ucb1(child, root) if sims > 0 else 0
            
            # Indicador visual
            if i == 0:
                indicator = "👑 MEJOR"
            elif win_rate >= 50:
                indicator = "✅ Bueno"
            elif win_rate >= 25:
                indicator = "⚠️  Regular"
            else:
                indicator = "❌ Malo"
            
            print(f" {pos}  | {sims:4d} | {wins:8.1f} | {win_rate:7.1f}% | {ucb1_val:5.2f} | {indicator}")
        
        best_child = sorted_children[0]
        print("-" * 50)
        print(f"🎯 DECISIÓN: Jugar en posición {best_child.data.move.position}")
        print(f"💪 Confianza: {best_child.data.simulations} simulaciones")
        print(f"🏆 Tasa de victoria: {(best_child.data.value / best_child.data.simulations * 100):.1f}%")
        print()

    def print_tree_structure(self, max_depth=2):
        """Muestra la estructura del árbol de búsqueda"""
        print("\n🌳 ESTRUCTURA DEL ÁRBOL DE BÚSQUEDA")
        print("=" * 40)
        
        def print_node(node, depth=0):
            if depth > max_depth:
                return
            
            indent = "  " * depth
            
            if node.is_root():
                print(f"{indent}🌱 RAÍZ (sims: {node.data.simulations})")
            else:
                pos = node.data.move.position
                player = "🤖" if node.data.move.player == Player.MACHINE else "👤"
                sims = node.data.simulations
                value = node.data.value
                win_rate = (value / sims * 100) if sims > 0 else 0
                
                print(f"{indent}├─ {player} Pos:{pos} | Sims:{sims} | Win:{win_rate:.1f}%")
            
            # Imprimir hijos ordenados por simulaciones
            children = self.tree.get_children(node)
            sorted_children = sorted(children, key=lambda x: x.data.simulations, reverse=True)
            
            for child in sorted_children:
                print_node(child, depth + 1)
        
        root = self.tree.get(0)
        print_node(root)
        print()

    def print_simple_analysis(self):
        """Muestra un análisis simple y rápido"""
        root = self.tree.get(0)
        children = self.tree.get_children(root)
        
        if not children:
            return
        
        print(f"\n🔍 MCTS analizó {len(children)} movimientos con {root.data.simulations} simulaciones totales")
        
        # Los 3 mejores movimientos
        sorted_children = sorted(children, key=lambda x: x.data.simulations, reverse=True)[:3]
        
        print("🏆 Top 3 movimientos:")
        for i, child in enumerate(sorted_children, 1):
            pos = child.data.move.position
            sims = child.data.simulations
            win_rate = (child.data.value / sims * 100) if sims > 0 else 0
            
            medal = ["🥇", "🥈", "🥉"][i-1]
            print(f"   {medal} Posición {pos}: {win_rate:.1f}% de victoria ({sims} sims)")
        print()
