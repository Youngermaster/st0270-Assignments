"""
LL(1) - table construction and predictive parser.
"""

from typing import Dict, List, Tuple  # Importamos tipos para anotaciones

from .grammar import Grammar, Symbol  # Importamos la clase Grammar y el tipo Symbol

# Definición del tipo de la tabla de análisis LL(1):
# No-terminal × Terminal → Producción
# Donde una producción es (No-terminal, Lista de símbolos del lado derecho)
ParseTable = Dict[Symbol, Dict[Symbol, Tuple[Symbol, List[Symbol]]]]  # A,a → prod


class LL1Parser:
    def __init__(self, G: Grammar):
        # Almacenar la gramática
        self.G = G
        # Construir la tabla de análisis predictivo LL(1)
        self.table: ParseTable = self._build_table()

    # ------------------------------------------------------------ #
    def _build_table(self) -> ParseTable:
        # Inicializar la tabla con diccionarios vacíos para cada no terminal
        table: ParseTable = {nt: {} for nt in self.G.nonterminals}

        # Para cada producción A -> α en la gramática
        for A, rhs_list in self.G.productions.items():
            for rhs in rhs_list:
                # Calcular FIRST(α)
                first = self.G.first_of_string(rhs)
                
                # Para cada terminal 'a' en FIRST(α) (excepto ε)
                for a in first - {"e"}:
                    # Comprobar conflictos (si ya existe una entrada para A,a)
                    if a in table[A]:
                        raise ValueError("LL(1) conflict")
                    # Establecer M[A,a] = A -> α
                    table[A][a] = (A, rhs)

                # Si ε está en FIRST(α), añadir A -> α a M[A,b] para cada b en FOLLOW(A)
                if "e" in first:
                    for b in self.G.follow[A]:
                        # Comprobar conflictos
                        if b in table[A]:
                            raise ValueError("LL(1) conflict (ε)")
                        # Establecer M[A,b] = A -> α
                        table[A][b] = (A, rhs)
        return table

    # ------------------------------------------------------------ #
    def parse(self, w: str) -> bool:
        # Asegurarse de que la cadena termina con $
        if not w.endswith("$"):
            w += "$"

        # Inicializar la pila con $ y el símbolo inicial S
        stack = ["$", "S"]
        idx = 0  # Índice para recorrer la cadena de entrada
        
        # Algoritmo de análisis predictivo LL(1)
        while stack:
            X = stack.pop()  # Obtener el símbolo de la cima de la pila
            a = w[idx]       # Obtener el símbolo actual de entrada
            
            # Si ambos son $, la cadena ha sido aceptada
            if X == a == "$":
                return True
                
            # Si X es terminal o $, debe coincidir con el símbolo de entrada
            if X in self.G.terminals | {"$"}:
                if X == a:
                    idx += 1  # Avanzar al siguiente símbolo de entrada
                else:
                    return False  # Error: no coinciden
            else:  # X es no terminal
                # Buscar la producción en la tabla para X y a
                entry = self.table.get(X, {}).get(a)
                if not entry:
                    return False  # Error: entrada vacía en la tabla
                    
                # Obtener el lado derecho de la producción
                _, rhs = entry
                
                # Si no es la producción épsilon, añadir los símbolos a la pila (en orden inverso)
                if rhs != ["e"]:
                    stack.extend(reversed(rhs))
        
        return False  # Si la pila queda vacía antes de procesar toda la entrada
