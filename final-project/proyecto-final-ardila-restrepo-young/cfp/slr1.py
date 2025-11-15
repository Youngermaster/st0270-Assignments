"""
SLR(1) - LR(0) automaton + ACTION/GOTO + driver.
Compact yet faithful to the book (section 4.6, Aho et al.).
"""

from collections import defaultdict  # Para diccionarios con valores por defecto
from typing import Dict, List, Set, Tuple  # Importamos tipos para anotaciones

from .grammar import Grammar  # Importamos la clase Grammar
from .utils import is_terminal, is_nonterminal  # Importamos funciones auxiliares

# Definiciones de tipos para mejorar la legibilidad
Item = Tuple[str, Tuple[str, ...], int]  # (A, rhs, dot): item LR(0) - (No terminal, lado derecho como tupla, posición del punto)
State = Set[Item]  # Un estado es un conjunto de items LR(0)
Action = Tuple[str, int | Tuple[str, int] | None]  # ('shift'|'reduce'|'accept', valor): acción a realizar


class SLR1Parser:
    def __init__(self, G: Grammar):
        # Almacenar la gramática
        self.G = G
        # Inicializar tablas ACTION y GOTO como diccionarios de diccionarios
        self.action: Dict[int, Dict[str, Action]] = defaultdict(dict)
        self.goto: Dict[int, Dict[str, int]] = defaultdict(dict)
        # Construir las tablas
        self._build_tables()

    # -------------------------------------------------------- #
    def _closure(self, I: State) -> State:
        """
        Calcula la clausura de un conjunto de items LR(0)
        Para cada item [A -> α·Bβ] en I, añadir [B -> ·γ] para cada producción B -> γ
        """
        changed, J = True, set(I)  # J es el conjunto resultado, inicialmente igual a I
        while changed:  # Repetir hasta que no haya cambios
            changed = False
            for A, rhs, dot in list(J):  # Para cada item en J
                # Si el punto está antes de un no terminal
                if dot < len(rhs) and is_nonterminal(sym := rhs[dot]):
                    # Añadir todos los items [B -> ·γ] donde B es el no terminal después del punto
                    for prod in self.G.productions[sym]:
                        item = (sym, tuple(prod), 0)  # Crear el nuevo item con el punto al inicio
                        if item not in J:  # Si no está ya en J
                            J.add(item)  # Añadirlo
                            changed = True  # Marcar que hubo cambios
        return J

    def _goto(self, I: State, X: str) -> State:
        """
        Calcula el conjunto GOTO(I,X):
        Todos los items [A -> αX·β] tales que [A -> α·Xβ] está en I
        """
        # Recolectar todos los items donde podemos mover el punto después de X
        moved = {
            (A, rhs, dot + 1) for A, rhs, dot in I if dot < len(rhs) and rhs[dot] == X
        }
        # Calcular la clausura si hay elementos
        return self._closure(moved) if moved else set()

    # -------------------------------------------------------- #
    def _items(self) -> List[State]:
        """
        Construye el autómata LR(0): conjunto de todos los estados alcanzables
        """
        # Comenzar con el item aumentado [S' -> ·S]
        start_item = ("S'", ("S",), 0)
        # Inicializar la colección con la clausura del item inicial
        C = [self._closure({start_item})]
        i = 0
        # Mientras haya estados por procesar
        while i < len(C):
            state = C[i]
            # Para cada símbolo X que aparece después de un punto en el estado
            for X in {
                s for A, rhs, dot in state if dot < len(rhs) for s in (rhs[dot],)
            }:
                # Calcular GOTO(state, X)
                nxt = self._goto(state, X)
                # Si el estado resultante no está vacío y no existe en la colección
                if nxt and nxt not in C:
                    C.append(nxt)  # Añadirlo
            i += 1
        return C

    # -------------------------------------------------------- #
    def _build_tables(self) -> None:
        """
        Construye las tablas ACTION y GOTO para el parser SLR(1)
        """
        # Obtener todos los estados del autómata LR(0)
        C = self._items()
        
        # Crear un índice para las producciones: (A, rhs) -> número de producción
        prod_index = {
            (A, tuple(rhs)): idx
            for A, prods in self.G.productions.items()
            for idx, rhs in enumerate(prods)
        }

        # Para cada estado en el autómata
        for i, I in enumerate(C):
            # Para cada item en el estado
            for A, rhs, dot in I:
                # Caso 1: [A -> α·aβ] (punto antes de terminal)
                if dot < len(rhs):
                    X = rhs[dot]  # Símbolo después del punto
                    j_state = C.index(self._goto(I, X))  # Estado destino
                    
                    if is_terminal(X):  # Si X es terminal
                        # Añadir acción shift a ACTION[i, X]
                        if X in self.action[i]:
                            raise ValueError("shift/reduce conflict")  # Detectar conflicto
                        self.action[i][X] = ("shift", j_state)
                    else:  # Si X es no terminal
                        # Añadir entrada GOTO[i, X] = j
                        self.goto[i][X] = j_state
                        
                # Caso 2: [A -> α·] (punto al final)
                else:
                    # Si es el item aumentado [S' -> S·], añadir acción de aceptación
                    if A == "S'":
                        self.action[i]["$"] = ("accept", None)
                        continue
                        
                    # Para otros items [A -> α·], añadir reducción por A -> α
                    # para cada terminal en FOLLOW(A)
                    for a in self.G.follow[A]:
                        if a in self.action[i]:
                            raise ValueError("conflict")  # Detectar conflicto
                        # Añadir acción reduce a ACTION[i, a]
                        self.action[i][a] = ("reduce", (A, prod_index[(A, rhs)]))

    # -------------------------------------------------------- #
    def parse(self, w: str) -> bool:
        """
        Implementa el algoritmo de análisis sintáctico SLR(1)
        Retorna True si la cadena w es aceptada, False en caso contrario
        """
        # Asegurarse de que la cadena termina con $
        if not w.endswith("$"):
            w += "$"

        # Inicializar la pila con el estado 0
        stack: List[int] = [0]
        idx = 0  # Índice para recorrer la cadena de entrada
        
        # Algoritmo de análisis SLR(1)
        while True:
            state = stack[-1]  # Estado actual (top de la pila)
            a = w[idx]         # Símbolo actual de entrada
            
            # Obtener acción para el estado actual y símbolo de entrada
            act = self.action.get(state, {}).get(a)
            if not act:
                return False  # Error: no hay acción definida
            
            kind, val = act  # Tipo de acción y valor asociado
            
            if kind == "shift":  # Acción shift
                stack.append(val)  # Añadir nuevo estado a la pila
                idx += 1          # Avanzar en la entrada
                
            elif kind == "reduce":  # Acción reduce
                A, prod_no = val    # No terminal y número de producción
                rhs = self.G.productions[A][prod_no]  # Lado derecho de la producción
                
                # Quitar |β| estados de la pila (excepto para ε)
                if rhs != ["e"]:
                    del stack[-len(rhs):]
                    
                state = stack[-1]  # Nuevo estado actual
                # Añadir el estado GOTO[state, A] a la pila
                stack.append(self.goto[state][A])
                
            elif kind == "accept":  # Acción accept
                return True  # La cadena es aceptada
