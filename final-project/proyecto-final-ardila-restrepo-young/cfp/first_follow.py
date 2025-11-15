"""
Pure, unit-test-friendly algorithms for FIRST / FOLLOW.
They do not mutate Grammar - they only *read* it and return dicts.
"""

from typing import Dict, List, Set, TYPE_CHECKING  # Importamos tipos para anotaciones

from .utils import is_terminal, is_nonterminal  # Importamos funciones auxiliares

# Evitar importación circular usando TYPE_CHECKING
if TYPE_CHECKING:
    from .grammar import Grammar  # Solo importa durante verificación de tipos

Symbol = str  # Definición local del tipo Symbol para evitar importación circular


def compute_first_sets(G: "Grammar") -> Dict[Symbol, Set[Symbol]]:
    # Calcula los conjuntos FIRST para cada símbolo de la gramática
    # FIRST(X) = conjunto de terminales que pueden aparecer al inicio de una derivación desde X
    
    # Inicialización: 
    # - Para terminales t: FIRST(t) = {t}
    # - Para épsilon 'e': FIRST(e) = {e}
    # - Para no terminales: FIRST(NT) = conjunto vacío inicialmente
    first: Dict[Symbol, Set[Symbol]] = {t: {t} for t in G.terminals | {"e"}} | {
        nt: set() for nt in G.nonterminals
    }

    changed = True  # Bandera para controlar el ciclo
    while changed:  # Repetir hasta que no haya cambios
        changed = False
        # Recorrer todas las producciones A -> α
        for A, rhs_list in G.productions.items():
            for rhs in rhs_list:
                # Caso 1: Producción épsilon (A -> ε)
                if rhs == ["e"]:
                    if "e" not in first[A]:
                        first[A].add("e")  # Agregar ε a FIRST(A)
                        changed = True
                    continue

                # Caso 2: Producción A -> X₁X₂...Xₙ
                for sym in rhs:  # Recorrer cada símbolo en el lado derecho
                    before = len(first[A])
                    # Agregar FIRST(X) - {ε} a FIRST(A)
                    first[A] |= first[sym] - {"e"}
                    
                    # Actualizamos el flag *antes* de decidir si salimos
                    if len(first[A]) != before:
                        changed = True
                    
                    # Ahora sí probamos si debemos cortar la cadena
                    # Si ε no está en FIRST(X), no podemos continuar al siguiente símbolo
                    if "e" not in first[sym]:
                        break
                else:  # Se ejecuta si no hubo break: todos los símbolos derivan ε
                    if "e" not in first[A]:
                        first[A].add("e")
                        changed = True
    return first


def compute_follow_sets(G: "Grammar") -> Dict[Symbol, Set[Symbol]]:
    # Calcula los conjuntos FOLLOW para cada no terminal de la gramática
    # FOLLOW(A) = conjunto de terminales que pueden aparecer inmediatamente después de A
    
    # Inicialización: todos los FOLLOW comienzan vacíos
    follow: Dict[Symbol, Set[Symbol]] = {nt: set() for nt in G.nonterminals}
    follow["S"].add("$")  # El símbolo inicial siempre tiene $ en su FOLLOW
    
    changed = True  # Bandera para controlar el ciclo
    while changed:  # Repetir hasta que no haya cambios
        changed = False
        # Recorrer todas las producciones A -> α
        for A, rhs_list in G.productions.items():
            for rhs in rhs_list:
                # Para cada no terminal B en la producción
                for i, B in enumerate(rhs):
                    if is_nonterminal(B):
                        # β es todo lo que sigue después de B
                        beta = rhs[i + 1 :]
                        # Calcular FIRST(β)
                        first_beta = G.first_of_string(beta)
                        before = len(follow[B])
                        
                        # Agregar FIRST(β) - {ε} a FOLLOW(B)
                        follow[B] |= first_beta - {"e"}
                        
                        # Si β puede derivar ε o β es vacío, agregar FOLLOW(A) a FOLLOW(B)
                        if "e" in first_beta or not beta:
                            follow[B] |= follow[A]
                            
                        # Actualizar bandera si hubo cambios
                        changed |= before != len(follow[B])
    return follow
