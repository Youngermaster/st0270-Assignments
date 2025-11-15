"""
Grammar class:  • parses the raw input
                • exposes FIRST / FOLLOW
                • keeps productions in canonical internal form
"""

from collections import defaultdict  # Para crear diccionarios con valores por defecto
from typing import Dict, List, Set, Tuple  # Importamos tipos para anotaciones

from .first_follow import compute_first_sets, compute_follow_sets  # Importamos algoritmos de cálculo
from .utils import is_terminal, is_nonterminal  # Importamos funciones auxiliares

# Definiciones de tipos para mejorar la legibilidad y comprensión
Symbol = str  # Un símbolo de la gramática (terminal o no terminal)
ProdRHS = List[Symbol]  # Lado derecho de una producción, lista de símbolos
Prod = Tuple[Symbol, ProdRHS]  # Una producción completa (lado izquierdo, lado derecho)
ProdDict = Dict[Symbol, List[ProdRHS]]  # Diccionario de producciones: NT -> lista de RHS


class Grammar:
    def __init__(self, raw_lines: List[str]) -> None:
        """
        Build grammar from the *n* production lines read by cli.py.
        Each line has the format  `A -> alpha beta | gamma`
        """
        # Inicializar el diccionario de producciones: no terminal -> lista de producciones del lado derecho
        self.productions: ProdDict = defaultdict(list)

        # Procesar cada línea de la gramática
        for line in raw_lines:
            # Dividir la línea en lado izquierdo y lado derecho
            lhs, rhs_part = [t.strip() for t in line.split("->")]
            alts = rhs_part.split()  # Dividir las alternativas (separadas por espacios)
            for alt in alts:
                rhs = list(alt)  # Convertir cada carácter como un símbolo individual
                self.productions[lhs].append(rhs)  # Añadir producción

        # Construir conjunto de no terminales (símbolos del lado izquierdo)
        self.nonterminals: Set[Symbol] = set(self.productions)
        
        # Construir conjunto de terminales (todos los símbolos del lado derecho que no son no terminales)
        self.terminals: Set[Symbol] = {
            s
            for rhs in self.productions.values()
            for prod in rhs
            for s in prod
            if is_terminal(s)
        } | {
            "$"  # Añadir el símbolo de fin de cadena ($) a los terminales
        }

        # Calcular y almacenar en caché los conjuntos FIRST y FOLLOW
        self.first: Dict[Symbol, Set[Symbol]] = compute_first_sets(self)
        self.follow: Dict[Symbol, Set[Symbol]] = compute_follow_sets(self)

    # ------------------------------------------------------------------ #
    # Convenience helpers
    def first_of_string(self, symbols: List[Symbol]) -> Set[Symbol]:
        """
        FIRST(αβ…) with ε-propagation
        Calcula el conjunto FIRST para una secuencia de símbolos
        """
        result: Set[Symbol] = set()
        # Iterar por cada símbolo en la secuencia
        for sym in symbols:
            # Añadir FIRST(sym) - {ε} al resultado
            result |= self.first[sym] - {"e"}
            # Si el símbolo no puede derivar ε, terminar
            if "e" not in self.first[sym]:
                break
        else:  # Si se procesaron todos los símbolos (no hubo break), añadir ε
            result.add("e")
        return result
