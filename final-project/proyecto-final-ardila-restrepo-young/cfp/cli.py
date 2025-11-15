"""
Console I/O wrapper.
"""

import sys  # Para salida de errores y terminación del programa

from .grammar import Grammar  # Importamos la clase Grammar
from .ll1 import LL1Parser  # Importamos el analizador LL(1)
from .slr1 import SLR1Parser  # Importamos el analizador SLR(1)


def _read_grammar() -> Grammar:
    """
    Lee la gramática desde la entrada estándar:
    - Primera línea: número de producciones (n)
    - Siguientes n líneas: producciones en formato "A -> abc"
    """
    try:
        n = int(input().strip())  # Leer el número de producciones
    except ValueError:
        sys.exit("First line must be an integer > 0")  # Error si no es un entero válido

    # Leer las n líneas de producciones y construir la gramática
    raw_lines = [input().rstrip() for _ in range(n)]
    return Grammar(raw_lines)


def _feed_strings(parse_cb):
    """
    Lee cadenas para analizar con el parser proporcionado como callback.
    Cada línea no vacía se analiza e imprime "yes" o "no" según sea aceptada o no.
    Una línea vacía termina la entrada.
    """
    while True:
        line = input().strip()  # Leer línea
        if not line:
            break  # Terminar si la línea está vacía
        print("yes" if parse_cb(line) else "no")  # Imprimir resultado del análisis


def main():
    """
    Función principal que maneja la interacción con el usuario:
    1. Lee la gramática
    2. Intenta construir los parsers LL(1) y SLR(1)
    3. Dependiendo de cuál(es) parser(s) se pudo construir:
       - Si ambos: pregunta al usuario cuál usar
       - Si solo uno: usa ese
       - Si ninguno: informa al usuario
    """
    # Leer la gramática
    G = _read_grammar()

    # Intentar construir ambos parsers, capturando conflictos como ValueError
    is_ll1 = is_slr = False
    try:
        ll1_parser = LL1Parser(G)  # Intentar construir el parser LL(1)
        is_ll1 = True  # Si no lanza excepción, la gramática es LL(1)
    except ValueError:
        pass  # Si hay conflictos, no es LL(1)
    try:
        slr_parser = SLR1Parser(G)  # Intentar construir el parser SLR(1)
        is_slr = True  # Si no lanza excepción, la gramática es SLR(1)
    except ValueError:
        pass  # Si hay conflictos, no es SLR(1)

    # ---- Interacción con el usuario según los 4 casos posibles ---- #
    if is_ll1 and is_slr:
        # Caso 1: La gramática es LL(1) y SLR(1)
        prompt = "Select a parser (T: for LL(1), B: for SLR(1), Q: quit):"
        while True:
            print(prompt)
            choice = input().strip().upper()  # Leer y normalizar la elección
            if choice == "Q":
                break  # Salir
            elif choice == "T":
                _feed_strings(ll1_parser.parse)  # Usar parser LL(1)
            elif choice == "B":
                _feed_strings(slr_parser.parse)  # Usar parser SLR(1)
    elif is_ll1:
        # Caso 2: La gramática es solo LL(1)
        print("Grammar is LL(1).")
        _feed_strings(ll1_parser.parse)
    elif is_slr:
        # Caso 3: La gramática es solo SLR(1)
        print("Grammar is SLR(1).")
        _feed_strings(slr_parser.parse)
    else:
        # Caso 4: La gramática no es ni LL(1) ni SLR(1)
        print("Grammar is neither LL(1) nor SLR(1).")


if __name__ == "__main__":
    main()  # Ejecutar solo si se llama directamente al script
