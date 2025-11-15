from typing import Iterable, List  # Importamos tipos para anotaciones


def flatten(seqs: Iterable[Iterable[str]]) -> List[str]:
    """Returns a 1-D list from a nested iterable"""
    # Aplana una lista de listas en una sola lista
    # Utiliza comprensión de listas doble: itera sobre cada secuencia y luego sobre cada elemento
    return [s for seq in seqs for s in seq]


def is_terminal(sym: str) -> bool:
    # Determina si un símbolo es terminal:
    # - No debe estar en mayúsculas (los no terminales son mayúsculas)
    # - No debe ser 'e' (épsilon) ni '$' (fin de cadena)
    return not sym.isupper() and sym not in ("e", "$")


def is_nonterminal(sym: str) -> bool:
    # Determina si un símbolo es no terminal:
    # - Debe estar en mayúsculas (convención para representar no terminales)
    return sym.isupper()
