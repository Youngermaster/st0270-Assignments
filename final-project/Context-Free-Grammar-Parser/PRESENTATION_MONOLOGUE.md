# Monólogo de Presentación: Context-Free Grammar Parser

## Introducción

Buenos días/tardes. Hoy les voy a presentar mi proyecto de **Parser de Gramáticas Libres de Contexto**.

¿Alguna vez se han preguntado cómo una computadora entiende si un código que escribimos es válido o no? ¿Cómo sabe Python que `if x == 5:` está bien escrito pero `if x = 5:` está mal? Bueno, detrás de eso hay algo llamado un **parser**, que es básicamente un programa que lee texto y verifica si cumple con ciertas reglas.

Mi proyecto hace exactamente eso, pero en lugar de analizar código Python o Java, analiza **gramáticas libres de contexto**. Estas son como las reglas del juego que definen qué cadenas de texto son válidas y cuáles no.

Lo interesante es que mi programa no solo analiza UNA gramática, sino que puede usar **DOS métodos diferentes** para hacerlo:
- **LL(1)**: Un método que lee de izquierda a derecha y trabaja de arriba hacia abajo
- **SLR(1)**: Otro método que también lee de izquierda a derecha pero trabaja de abajo hacia arriba

Y lo más cool es que el programa automáticamente te dice qué método funciona para tu gramática, o si ninguno funciona.

---

## Arquitectura General: Los 7 Archivos Principales

Okay, antes de meternos en detalles, déjenme mostrarles cómo está organizado el código. Lo dividí en **7 archivos principales**, cada uno con una responsabilidad específica. Es como una línea de producción en una fábrica: cada estación hace una cosa específica.

### 1. **main.py** - El Punto de Entrada
Este es el archivo más simple. Solo tiene 4 líneas de código real. Su único trabajo es decir "Oye, `cli.py`, ¡empieza a trabajar!". Es como el botón de encendido de toda la máquina.

### 2. **cli.py** - La Interfaz de Línea de Comandos
Este es el **cerebro** del programa. Coordina todo. Lee la entrada del usuario, llama a los otros módulos en el orden correcto, y decide qué hacer según los resultados. Es como el director de orquesta.

### 3. **utils.py** - Los Bloques Básicos (Símbolos)
Aquí definimos qué es un **símbolo**. En nuestro mundo, un símbolo puede ser:
- Una letra minúscula → terminal (como 'a', 'b', '+')
- Una letra MAYÚSCULA → no terminal (como 'S', 'A', 'E')
- La letra 'e' especial → epsilon (cadena vacía)
- El símbolo '$' → fin de entrada

Es como definir los tipos de piezas de Lego con las que vamos a trabajar.

### 4. **grammar.py** - La Gramática
Este archivo sabe cómo leer y entender una gramática. Una gramática es un conjunto de reglas como:
```
S -> aS
S -> b
```
Este módulo las convierte de texto plano a objetos Python que podemos manipular. Es como traducir del español a un lenguaje que la computadora entiende.

### 5. **first_follow.py** - Conjuntos FIRST y FOLLOW
Este es uno de los archivos más importantes. Calcula dos cosas mágicas:
- **FIRST**: ¿Con qué símbolos puede EMPEZAR una producción?
- **FOLLOW**: ¿Qué símbolos pueden venir DESPUÉS de un no terminal?

Estos conjuntos son super importantes porque los parsers los usan para tomar decisiones.

### 6. **ll1.py** - El Parser LL(1)
Aquí está la implementación completa del parser LL(1). Construye una tabla de análisis y luego la usa para verificar si una cadena es válida. Trabaja con una pila y va prediciendo qué producción usar.

### 7. **slr1.py** - El Parser SLR(1)
Y aquí está el parser SLR(1). Es más complejo que LL(1). Construye un autómata (una máquina de estados) y usa tablas ACTION y GOTO para decidir qué hacer en cada momento.

---

Ahora que tienen la visión general, vamos a entrar en detalle a cada uno. Imaginen que vamos a seguir el flujo de ejecución paso a paso, como si estuviéramos haciendo debugging.

---

## El Viaje de una Gramática: Paso a Paso

Voy a usar un ejemplo super simple para explicar todo el flujo. Supongamos que el usuario nos da esta gramática:

```
1
S -> a
```

Que significa: "La única cadena válida es 'a'". Simple, ¿verdad?

Y el usuario también nos da la cadena "a" para verificar si es válida.

Ahora veamos qué pasa internamente...

---

## Paso 1: main.py - Arrancando la Máquina

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from src.cli import run

if __name__ == '__main__':
    run()
```

¿Ven? Super simple. Solo configura el path de Python para que pueda encontrar nuestros módulos en la carpeta `src/`, y luego llama a `run()` del módulo `cli`.

Es literalmente como presionar el botón de encendido. Nada más. Todo el trabajo real pasa en `cli.py`.

---

## Paso 2: cli.py - El Director de Orquesta

Okay, aquí es donde empieza lo interesante. La función `run()` en `cli.py` es como un checklist que va marcando tareas:

### Tarea 1: Leer la gramática del usuario

```python
def read_grammar_input():
    lines = []
    first_line = input().strip()  # Lee "1"
    lines.append(first_line)
    n = int(first_line)            # n = 1

    for _ in range(n):             # Lee 1 línea
        line = input()             # Lee "S -> a"
        lines.append(line)

    return lines
```

Entonces el usuario escribe:
```
1
S -> a
```

Y la función devuelve:
```python
lines = ["1", "S -> a"]
```

Simple, ¿no? Solo leemos línea por línea.

### Tarea 2: Convertir el texto a objetos Grammar

```python
grammar = parse_grammar(lines)
```

Aquí llamamos a `grammar.py` para que convierta esas líneas de texto en una estructura de datos que podemos usar. Pero eso lo veremos en un momento.

### Tarea 3: Calcular FIRST y FOLLOW

```python
first_sets = compute_first_sets(grammar)
follow_sets = compute_follow_sets(grammar, first_sets)
```

Le pedimos a `first_follow.py` que haga su magia y calcule los conjuntos.

### Tarea 4: Intentar construir el parser LL(1)

```python
ll1_parser = None
try:
    ll1_parser = LL1Parser(grammar, first_sets, follow_sets)
except NotLL1Exception:
    pass  # No es LL(1), está bien
```

Intentamos crear un parser LL(1). Si la gramática no es LL(1), la excepción nos dice y seguimos adelante.

### Tarea 5: Intentar construir el parser SLR(1)

```python
slr1_parser = None
try:
    slr1_parser = SLR1Parser(grammar, first_sets, follow_sets)
except NotSLR1Exception:
    pass  # No es SLR(1), está bien
```

Lo mismo pero con SLR(1).

### Tarea 6: Decidir qué hacer según los resultados

```python
if ll1_parser and slr1_parser:
    # ¡Ambos funcionan! Modo interactivo
    interactive_mode(ll1_parser, slr1_parser)

elif ll1_parser:
    # Solo LL(1)
    print("Grammar is LL(1).")
    parse_strings_until_empty(ll1_parser.parse)

elif slr1_parser:
    # Solo SLR(1)
    print("Grammar is SLR(1).")
    parse_strings_until_empty(slr1_parser.parse)

else:
    # Ninguno funciona
    print("Grammar is neither LL(1) nor SLR(1).")
```

Dependiendo de qué parsers funcionaron, hace cosas diferentes. En nuestro ejemplo, ambos deberían funcionar porque `S -> a` es super simple.

---

## Paso 3: utils.py - Definiendo los Bloques Básicos

Okay, antes de seguir con el flujo, necesito explicarles qué es un **Symbol** porque todo el código usa esto.

### La clase Symbol

```python
class Symbol:
    def __init__(self, value, is_epsilon=False, is_end_marker=False):
        self.value = value
        self._is_epsilon = is_epsilon
        self._is_end_marker = is_end_marker

        # Determinar el tipo
        if is_epsilon:
            self.type = SymbolType.EPSILON
        elif is_end_marker:
            self.type = SymbolType.END_MARKER
        elif self._is_uppercase(value):
            self.type = SymbolType.NONTERMINAL
        else:
            self.type = SymbolType.TERMINAL
```

Entonces cuando creamos:
```python
Symbol('a')  # Es un terminal (minúscula)
Symbol('S')  # Es un no terminal (mayúscula)
Symbol('e', is_epsilon=True)  # Es epsilon
Symbol('$', is_end_marker=True)  # Es fin de entrada
```

Es como etiquetar cada pieza de Lego con su tipo. Esto hace que el resto del código sea más fácil porque podemos preguntar:
```python
if symbol.is_terminal():
    # hacer algo
elif symbol.is_nonterminal():
    # hacer otra cosa
```

### Convirtiendo strings a Symbols

```python
def char_to_symbol(char: str) -> Symbol:
    if char == 'e':
        return Symbol('e', is_epsilon=True)
    elif char == '$':
        return Symbol('$', is_end_marker=True)
    else:
        return Symbol(char)
```

Entonces `char_to_symbol('a')` nos da un Symbol de tipo TERMINAL.

Y `char_to_symbol('S')` nos da un Symbol de tipo NONTERMINAL.

---

## Paso 4: grammar.py - Entendiendo la Gramática

Ahora sí, volvamos al flujo. Teníamos:
```python
lines = ["1", "S -> a"]
grammar = parse_grammar(lines)
```

Veamos qué pasa dentro de `parse_grammar()`:

### Paso 4.1: Leer el número de producciones

```python
def parse_grammar(lines):
    n_str = lines[0].strip()  # "1"
    n = int(n_str)             # n = 1
```

Simple, la primera línea nos dice cuántas líneas de producciones vienen.

### Paso 4.2: Parsear cada línea de producción

```python
production_lines = lines[1:n+1]  # ["S -> a"]

all_productions = []
for line in production_lines:
    prods = parse_production_line(line)  # Parsea "S -> a"
    all_productions.extend(prods)
```

Ahora veamos `parse_production_line()`:

```python
def parse_production_line("S -> a"):
    parts = "S -> a".split(" -> ")
    # parts = ["S", "a"]

    lhs_str = "S"
    rhs_str = "a"

    lhs = char_to_symbol('S')  # Symbol('S', NONTERMINAL)

    # El lado derecho puede tener alternativas separadas por espacios
    alternatives = "a".split()  # ["a"]

    productions = []
    for alt in alternatives:  # alt = "a"
        rhs = string_to_symbols("a")  # [Symbol('a', TERMINAL)]
        productions.append(Production(lhs, rhs))

    return productions  # [Production(S, [a])]
```

Entonces `parse_production_line("S -> a")` nos devuelve:
```python
[Production(S, [a])]
```

Donde `Production` es una clase que tiene:
- `lhs`: El lado izquierdo (Symbol 'S')
- `rhs`: El lado derecho (lista de Symbols: [Symbol 'a'])

### Paso 4.3: Crear el objeto Grammar

```python
return Grammar(all_productions)
```

El constructor de Grammar hace varias cosas interesantes:

```python
class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.start_symbol = Symbol('S')  # Siempre es S

        # Extraer no terminales (todos los que están a la izquierda)
        self.nonterminals = set()
        for prod in productions:
            self.nonterminals.add(prod.lhs)
        # nonterminals = {S}

        # Extraer terminales (símbolos en el lado derecho que NO son no terminales)
        self.terminals = set()
        for prod in productions:
            for symbol in prod.rhs:
                if symbol.is_terminal():
                    self.terminals.add(symbol)
        # terminals = {a}

        # Crear un mapa: no terminal -> sus producciones
        self.production_map = {}
        for prod in productions:
            if prod.lhs not in self.production_map:
                self.production_map[prod.lhs] = []
            self.production_map[prod.lhs].append(prod)
        # production_map = {S: [S -> a]}
```

Entonces ahora tenemos un objeto `Grammar` que contiene toda la información organizada:
- Lista de producciones
- Conjunto de no terminales: {S}
- Conjunto de terminales: {a}
- Símbolo inicial: S
- Mapa de producciones por no terminal

---

## Paso 5: first_follow.py - La Magia de FIRST y FOLLOW

Okay, ahora viene una de las partes más importantes. Necesitamos calcular los conjuntos FIRST y FOLLOW.

### ¿Por qué los necesitamos?

Imagina que estás leyendo una cadena y ves el símbolo 'a'. ¿Qué producción deberías usar? Para saberlo, necesitas saber qué producciones pueden EMPEZAR con 'a'. Eso es exactamente lo que FIRST nos dice.

Y FOLLOW nos dice qué puede venir DESPUÉS de un no terminal, lo cual es útil cuando una producción termina.

### Calculando FIRST

```python
def compute_first_sets(grammar):
    first_sets = {}

    # Paso 1: FIRST de terminales es el terminal mismo
    for terminal in grammar.terminals:
        first_sets[terminal] = {terminal}
    # first_sets[a] = {a}

    # Paso 2: Inicializar FIRST de no terminales como vacío
    for nonterminal in grammar.nonterminals:
        first_sets[nonterminal] = set()
    # first_sets[S] = {}

    # Paso 3: Iterar hasta que no haya cambios
    changed = True
    while changed:
        changed = False

        for prod in grammar.productions:
            # Producción: S -> a
            lhs = prod.lhs  # S
            rhs = prod.rhs  # [a]

            # Calcular FIRST del lado derecho
            rhs_first = compute_first_of_string(rhs, first_sets)
            # rhs_first = FIRST([a]) = {a}

            # Agregarlo a FIRST(lhs)
            old_size = len(first_sets[lhs])
            first_sets[lhs] = first_sets[lhs].union(rhs_first)
            new_size = len(first_sets[lhs])

            if new_size > old_size:
                changed = True

    return first_sets
```

Para nuestro ejemplo:
- Iteración 1:
  - `FIRST(S)` empieza vacío: {}
  - Procesamos S -> a
  - `FIRST([a])` = {a}
  - Agregamos {a} a `FIRST(S)`
  - `FIRST(S)` = {a} ✓ (cambió!)

- Iteración 2:
  - Procesamos S -> a otra vez
  - `FIRST(S)` ya tiene {a}
  - No cambia nada
  - `changed = False` → terminamos

Resultado final:
```
FIRST(S) = {a}
FIRST(a) = {a}
```

### Calculando FOLLOW

```python
def compute_follow_sets(grammar, first_sets):
    follow_sets = {}

    # Paso 1: Inicializar todos como vacíos
    for nonterminal in grammar.nonterminals:
        follow_sets[nonterminal] = set()

    # Paso 2: Agregar $ a FOLLOW del símbolo inicial
    follow_sets[grammar.start_symbol].add(END_MARKER)
    # FOLLOW(S) = {$}

    # Paso 3: Iterar...
    changed = True
    while changed:
        changed = False

        for prod in grammar.productions:
            # S -> a
            # No hay no terminales en el lado derecho
            # Nada que hacer

    return follow_sets
```

Para nuestro ejemplo simple, el resultado es:
```
FOLLOW(S) = {$}
```

Porque S es el símbolo inicial y no aparece en ninguna otra producción.

---

## Paso 6: ll1.py - Construyendo el Parser LL(1)

Ahora que tenemos FIRST y FOLLOW, podemos intentar construir el parser LL(1).

```python
ll1_parser = LL1Parser(grammar, first_sets, follow_sets)
```

Dentro del constructor:

### Construyendo la Tabla LL(1)

```python
class LL1Parser:
    def __init__(self, grammar, first_sets, follow_sets):
        self.grammar = grammar
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.table = self._build_table()
```

Veamos `_build_table()`:

```python
def _build_table(self):
    table = {}

    for prod in self.grammar.productions:
        # Producción: S -> a
        lhs = prod.lhs  # S
        rhs = prod.rhs  # [a]

        # FIRST del lado derecho
        first_alpha = compute_first_of_string(rhs, self.first_sets)
        # first_alpha = FIRST([a]) = {a}

        # Para cada terminal en FIRST (excepto epsilon)
        for symbol in first_alpha:
            if not symbol.is_epsilon():
                key = (lhs, symbol)  # (S, a)

                # Verificar conflictos
                if key in table:
                    # ¡Conflicto! No es LL(1)
                    raise NotLL1Exception(...)

                table[key] = prod
                # table[(S, a)] = S -> a

        # Si epsilon está en FIRST, agregar entradas para FOLLOW
        if EPSILON in first_alpha:
            # En nuestro caso, no hay epsilon
            pass

    return table
```

Resultado:
```python
table = {
    (S, a): S -> a
}
```

Esta tabla dice: "Si estás procesando el no terminal S y ves el símbolo 'a' en la entrada, usa la producción S -> a".

¡No hubo conflictos! La gramática ES LL(1).

### Parseando una Cadena con LL(1)

Ahora el usuario nos da la cadena "a" para verificar. Veamos cómo `parse()` la procesa:

```python
def parse(self, input_string: str) -> bool:
    # Convertir "a" a símbolos y agregar $
    input_symbols = [char_to_symbol(c) for c in "a"]
    # input_symbols = [Symbol('a')]
    input_symbols.append(END_MARKER)
    # input_symbols = [Symbol('a'), Symbol('$')]

    # Inicializar pila con [$, S]
    stack = [END_MARKER, self.grammar.start_symbol]
    # stack = [Symbol('$'), Symbol('S')]

    input_idx = 0  # Apuntando a 'a'

    while stack:
        top = stack[-1]  # S
        current_input = input_symbols[input_idx]  # a

        # ¿Coinciden?
        if top == current_input:
            stack.pop()
            input_idx += 1
            continue

        # ¿El tope es no terminal?
        if top.is_nonterminal():
            key = (top, current_input)  # (S, a)

            # Buscar en la tabla
            if key not in self.table:
                return False  # No hay entrada -> rechazar

            prod = self.table[key]  # S -> a

            # Pop del no terminal
            stack.pop()  # stack = [$]

            # Push del lado derecho (en orden inverso)
            if prod.rhs != [EPSILON]:
                for symbol in reversed(prod.rhs):
                    stack.append(symbol)
            # stack = [$, a]

            continue

        # El tope es terminal pero no coincide
        return False

    # ¿Consumimos toda la entrada?
    return input_idx == len(input_symbols)
```

Traza completa:

```
Inicio:
  stack = [$, S]
  input = [a, $]
  input_idx = 0 (apuntando a 'a')

Paso 1:
  top = S (no terminal)
  current = a
  Buscar tabla[(S, a)] = S -> a
  Pop S
  Push 'a' (en reversa de [a])
  stack = [$, a]

Paso 2:
  top = a (terminal)
  current = a
  ¡Coinciden!
  Pop a
  Avanzar input_idx = 1
  stack = [$]

Paso 3:
  top = $
  current = $
  ¡Coinciden!
  Pop $
  Avanzar input_idx = 2
  stack = []

Stack vacío, entrada consumida
return True ✓
```

¡La cadena "a" es ACEPTADA!

---

## Paso 7: slr1.py - El Parser SLR(1)

Okay, ahora vamos con el parser SLR(1). Este es más complejo porque construye un autómata.

```python
slr1_parser = SLR1Parser(grammar, first_sets, follow_sets)
```

### Gramática Aumentada

Lo primero que hace SLR(1) es crear una gramática "aumentada":

```python
self.augmented_start = Symbol("'")  # S'
self.start_production = Production(
    self.augmented_start,
    [grammar.start_symbol]  # S' -> S
)
```

Ahora tenemos:
```
S' -> S
S -> a
```

¿Por qué? Para saber cuándo ACEPTAR. Cuando reduzcamos a S' es que terminamos exitosamente.

### Construyendo Items LR(0)

Un "item" es una producción con un punto (•) que marca dónde vamos en el parsing:

```python
[S' -> • S]    # No hemos visto nada
[S' -> S •]    # Ya vimos S completo
[S -> • a]     # Esperamos ver 'a'
[S -> a •]     # Ya vimos 'a' completo
```

### Estado 0: El Inicio

```python
initial_item = LR0Item(self.start_production, 0)
# [S' -> • S]

initial_state = self._closure({initial_item})
```

La función `_closure()` agrega items relacionados:

```python
def _closure(items):
    closure = set(items)  # {[S' -> • S]}

    changed = True
    while changed:
        changed = False
        for item in closure:
            symbol = item.symbol_after_dot()
            # Para [S' -> • S], symbol = S

            if symbol and symbol.is_nonterminal():
                # Agregar todas las producciones de S
                for prod in grammar.get_productions(S):
                    # prod = S -> a
                    new_item = LR0Item(prod, 0)
                    # new_item = [S -> • a]

                    if new_item not in closure:
                        closure.add(new_item)
                        changed = True

    return closure
```

Resultado:
```
Estado 0 = {
    [S' -> • S],
    [S -> • a]
}
```

### Generando Estados con GOTO

```python
def _goto(items, symbol):
    moved_items = set()

    for item in items:
        if item.symbol_after_dot() == symbol:
            # Mover el punto sobre el símbolo
            new_item = LR0Item(item.production, item.dot_pos + 1)
            moved_items.add(new_item)

    return _closure(moved_items)
```

Desde Estado 0:

**GOTO(Estado 0, S):**
```
Items con S después del punto: [S' -> • S]
Mover: [S' -> S •]
CLOSURE: {[S' -> S •]}

Estado 1 = {[S' -> S •]}
```

**GOTO(Estado 0, a):**
```
Items con 'a' después del punto: [S -> • a]
Mover: [S -> a •]
CLOSURE: {[S -> a •]}

Estado 2 = {[S -> a •]}
```

Autómata completo:
```
Estado 0: {[S' -> • S], [S -> • a]}
Estado 1: {[S' -> S •]}
Estado 2: {[S -> a •]}

Transiciones:
  (0, S) -> 1
  (0, a) -> 2
```

### Construyendo las Tablas ACTION y GOTO

```python
def _build_tables(self):
    action_table = {}
    goto_table = {}

    for state_id, state in enumerate(self.states):
        for item in state:
            sym_after_dot = item.symbol_after_dot()

            if sym_after_dot:
                # Item con algo después del punto
                if sym_after_dot.is_terminal():
                    # SHIFT
                    # Ejemplo: [S -> • a] en estado 0
                    key = (state_id, sym_after_dot)  # (0, a)
                    next_state = self.transitions[key]  # 2
                    action_table[key] = SLR1Action("shift", next_state)
                    # ACTION[0, a] = shift 2

            else:
                # Item con punto al final: REDUCE
                # Ejemplo: [S -> a •] en estado 2
                if item.production.lhs == self.augmented_start:
                    # [S' -> S •] = ACCEPT
                    action_table[(state_id, END_MARKER)] = SLR1Action("accept")
                    # ACTION[1, $] = accept
                else:
                    # Reduce en símbolos de FOLLOW
                    follow_set = self.follow_sets[item.production.lhs]
                    # FOLLOW(S) = {$}

                    for symbol in follow_set:
                        key = (state_id, symbol)  # (2, $)
                        action_table[key] = SLR1Action("reduce", item.production)
                        # ACTION[2, $] = reduce S -> a

        # GOTO table para no terminales
        for (src, symbol), dst in self.transitions.items():
            if src == state_id and symbol.is_nonterminal():
                goto_table[(state_id, symbol)] = dst
                # GOTO[0, S] = 1

    return action_table, goto_table
```

Tablas finales:
```
ACTION Table:
  [0, a] = shift 2
  [1, $] = accept
  [2, $] = reduce S -> a

GOTO Table:
  [0, S] = 1
```

### Parseando con SLR(1)

```python
def parse(self, input_string: str) -> bool:
    # Convertir entrada
    input_symbols = [char_to_symbol(c) for c in "a"]
    input_symbols.append(END_MARKER)
    # input_symbols = [a, $]

    # Inicializar pilas
    state_stack = [0]
    symbol_stack = []
    input_idx = 0

    while True:
        current_state = state_stack[-1]  # 0
        current_input = input_symbols[input_idx]  # a

        # Buscar acción
        key = (current_state, current_input)  # (0, a)
        action = self.action_table[key]  # shift 2

        if action.type == "accept":
            return True

        elif action.type == "shift":
            # Push símbolo y estado
            symbol_stack.append(current_input)
            state_stack.append(action.value)
            input_idx += 1
            # symbol_stack = [a]
            # state_stack = [0, 2]
            # input_idx = 1 (apuntando a $)

            # Siguiente iteración...
            current_state = 2
            current_input = $
            key = (2, $)
            action = reduce S -> a

        elif action.type == "reduce":
            prod = action.value  # S -> a

            # Pop |rhs| símbolos y estados
            rhs_len = len(prod.rhs)  # 1
            for _ in range(rhs_len):
                symbol_stack.pop()  # Quitar 'a'
                state_stack.pop()   # Quitar 2
            # symbol_stack = []
            # state_stack = [0]

            # Push LHS
            symbol_stack.append(prod.lhs)  # S
            # symbol_stack = [S]

            # GOTO
            goto_state = state_stack[-1]  # 0
            goto_key = (goto_state, prod.lhs)  # (0, S)
            next_state = self.goto_table[goto_key]  # 1
            state_stack.append(next_state)
            # state_stack = [0, 1]

            # Siguiente iteración...
            current_state = 1
            current_input = $
            key = (1, $)
            action = accept

            return True ✓
```

¡También acepta "a"!

---

## Paso 8: cli.py - Mostrando Resultados

Volviendo a `cli.py`, después de construir ambos parsers:

```python
if ll1_parser and slr1_parser:
    # ¡Ambos funcionan!
    interactive_mode(ll1_parser, slr1_parser)
```

Modo interactivo:

```python
def interactive_mode(ll1_parser, slr1_parser):
    while True:
        print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
        choice = input().strip()

        if choice in ['Q', 'q']:
            break

        elif choice in ['T', 't']:
            # Usar LL(1)
            parse_strings_until_empty(ll1_parser.parse)

        elif choice in ['B', 'b']:
            # Usar SLR(1)
            parse_strings_until_empty(slr1_parser.parse)
```

Y `parse_strings_until_empty()`:

```python
def parse_strings_until_empty(parse_function):
    while True:
        line = input()
        trimmed = line.strip()

        if not trimmed:  # Línea vacía = parar
            break

        # Parsear la cadena
        result = parse_function(trimmed)
        print("yes" if result else "no")
```

Entonces si el usuario escribe:
```
T
a

```

El programa responde:
```
yes
```

---

## Resumen del Flujo Completo

Déjenme hacer un resumen rápido de todo el viaje:

1. **main.py** arranca el programa
2. **cli.py** lee la gramática del usuario
3. **grammar.py** convierte el texto a objetos Python
4. **utils.py** proporciona la clase Symbol que todos usan
5. **first_follow.py** calcula conjuntos FIRST y FOLLOW
6. **ll1.py** intenta construir parser LL(1)
7. **slr1.py** intenta construir parser SLR(1)
8. **cli.py** decide qué hacer y parsea cadenas

Todo trabaja junto como una máquina bien aceitada. Cada módulo tiene una responsabilidad clara y bien definida.

---

## Ejemplos de Salida

Para finalizar, déjenme mostrarles algunos ejemplos de ejecución:

### Ejemplo 1: Gramática solo SLR(1)
```
Input:
3
S -> S+T T
T -> T*F F
F -> (S) i
i+i

Output:
Grammar is SLR(1).
yes
```

Esta gramática tiene recursión izquierda (S -> S+...), por eso NO es LL(1), pero SÍ es SLR(1).

### Ejemplo 2: Gramática ambos
```
Input:
1
S -> a
T
a

Q

Output:
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
yes
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
```

Ambos parsers funcionan, entra en modo interactivo.

### Ejemplo 3: Gramática ni LL(1) ni SLR(1)
```
Input:
1
S -> SS a

Output:
Grammar is neither LL(1) nor SLR(1).
```

Esta gramática es ambigua, ningún parser puede manejarla.

---

## Conclusión

Y eso es todo. Mi proyecto puede:

✅ Leer gramáticas libres de contexto
✅ Calcular conjuntos FIRST y FOLLOW
✅ Construir parsers LL(1) y SLR(1)
✅ Clasificar automáticamente la gramática
✅ Validar cadenas de entrada

Todo implementado desde cero en Python, con una arquitectura modular y fácil de entender.

El código está bien documentado, tiene ejemplos de prueba, y cada componente está separado en su propio módulo con una responsabilidad específica.

¿Alguna pregunta?

---

**¡Gracias por su atención!** 🎓
