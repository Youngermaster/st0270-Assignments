# Simple Grammar Examples (Verificables a Papel)

Estos son ejemplos adicionales diseñados para ser **fáciles de verificar manualmente** (a papel). Son ideales para aprender y entender cómo funcionan los parsers LL(1) y SLR(1).

---

## Example 5: `example5_simple_neither.txt` - Neither LL(1) nor SLR(1)

**Gramática**:
```
S -> aSa | bSb | e
```

**Tipo**: Neither (Ni LL(1) ni SLR(1))

**¿Por qué?**:
- **Conflicto LL(1)**: Cuando vemos 'a' o 'b', no sabemos si:
  - Usar S → aSa/bSb (consumir el símbolo)
  - Usar S → e (dejar el símbolo para el contexto exterior)
- FOLLOW(S) = {a, b, $}
- Esto crea conflicto: M[S, a] tiene S→aSa Y S→e

**Verificación a papel - FIRST/FOLLOW**:
```
FIRST(S) = {a, b, ε}
FOLLOW(S) = {a, b, $}

Tabla LL(1) tendría:
M[S, a] = S → aSa
M[S, a] = S → e  ← CONFLICTO!
M[S, b] = S → bSb
M[S, b] = S → e  ← CONFLICTO!
```

**Salida esperada**:
```
Grammar is neither LL(1) nor SLR(1).
```

---

## Example 6: `example6_simple_slr1.txt` - SLR(1) Only

**Gramática**:
```
S -> S+n | n
```

**Tipo**: SLR(1) only (NO es LL(1))

**¿Por qué es SLR(1)?**:
- Tiene recursión izquierda
- LL(1) NO puede manejar recursión izquierda
- SLR(1) sí puede (usa análisis bottom-up)

**¿Por qué NO es LL(1)?**:
- S → S+n tiene S al inicio (recursión izquierda)
- No podemos calcular FIRST(S+n) sin entrar en bucle infinito

**Verificación a papel - Derivación**:
```
Para "n+n+n":
  S → S+n
    → S+n+n
    → S+n+n+n
    → n+n+n+n (error en derivación)

Correcto con SLR(1):
  S → n (reduce)
  S → S+n (reduce)
  S → S+n (reduce)
```

**Test strings**:
- `n+n` → yes
- `n+n+n` → yes
- `n` → yes
- `+n` → no (no empieza con 'n')

**Salida esperada**:
```
Grammar is SLR(1).
yes
yes
yes
no
```

---

## Example 7: `example7_simple_neither.txt` - Neither LL(1) nor SLR(1)

**Gramática**:
```
S -> aS | Sa | a
```

**Tipo**: Neither

**¿Por qué?**:
- **Recursión izquierda** (S → Sa) → NO es LL(1)
- **Shift/Reduce conflicts** → NO es SLR(1)
- Cuando vemos 'a', el parser no sabe si hacer shift o reduce

**Verificación a papel**:
```
Para "aa":
¿Cómo derivar?
  Opción 1: S → aS → aa (S→a)
  Opción 2: S → Sa → aa (S→a)

Hay ambigüedad en el proceso de parsing.
```

**Salida esperada**:
```
Grammar is neither LL(1) nor SLR(1).
```

---

## Example 8: `example8_single_terminal.txt` - Both (Más Simple Posible)

**Gramática**:
```
S -> a
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: La gramática MÁS SIMPLE posible. Solo acepta la cadena "a".

**Verificación a papel - FIRST/FOLLOW**:
```
FIRST(S) = {a}
FOLLOW(S) = {$}

Tabla LL(1):
M[S, a] = S → a

Derivación para "a":
  S → a ✓
```

**Test strings**:
- `a` → yes
- `aa` → no (solo acepta una 'a')
- `b` → no (solo acepta 'a')

**Salida esperada**:
```
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
yes
no
no
```

---

## Example 9: `example9_two_nonterminals.txt` - Both (Dos No Terminales)

**Gramática**:
```
S -> aA
A -> b
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: Gramática simple con dos no terminales. Solo acepta "ab".

**Verificación a papel - Derivación**:
```
Para "ab":
  S → aA
    → ab (A→b) ✓

Para "a":
  S → aA
    → a??? (A debe derivar algo) ✗
```

**FIRST/FOLLOW**:
```
FIRST(S) = {a}
FIRST(A) = {b}
FOLLOW(S) = {$}
FOLLOW(A) = {$}
```

**Test strings**:
- `ab` → yes
- `a` → no (incompleto)
- `b` → no (debe empezar con 'a')
- `abb` → no (solo acepta "ab")

---

## Example 10: `example10_repetition.txt` - Both (Repetición Simple)

**Gramática**:
```
S -> aS | e
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: Acepta cero o más 'a's (a*).

**Verificación a papel - Derivaciones**:
```
Para "":
  S → e ✓

Para "a":
  S → aS → ae → a ✓

Para "aa":
  S → aS → a(aS) → a(ae) → aa ✓

Para "aaa":
  S → aS → a(aS) → a(a(aS)) → a(a(ae)) → aaa ✓
```

**FIRST/FOLLOW**:
```
FIRST(S) = {a, ε}
FOLLOW(S) = {$}

Tabla LL(1):
M[S, a] = S → aS
M[S, $] = S → e
```

**Test strings**:
- `a` → yes
- `aa` → yes
- `aaa` → yes
- `aaaa` → yes
- `` (vacío) → yes

---

## Example 11: `example11_optional.txt` - Both (Elemento Opcional)

**Gramática**:
```
S -> aAb
A -> c | e
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: 'a' seguido de 'c' opcional, seguido de 'b'. Acepta "ab" o "acb".

**Verificación a papel**:
```
Para "ab":
  S → aAb → a(e)b → ab ✓

Para "acb":
  S → aAb → a(c)b → acb ✓

Para "accb":
  S → aAb → a(c)b → acb ✗ (A solo puede ser una 'c')
```

**FIRST/FOLLOW**:
```
FIRST(S) = {a}
FIRST(A) = {c, ε}
FOLLOW(S) = {$}
FOLLOW(A) = {b}

Tabla LL(1):
M[S, a] = S → aAb
M[A, c] = A → c
M[A, b] = A → e
```

**Test strings**:
- `ab` → yes (sin 'c')
- `acb` → yes (con 'c')
- `accb` → no (solo una 'c')
- `aab` → no (falta 'c' o sobra 'a')

---

## Example 12: `example12_alternation.txt` - Both (Alternancia Simple)

**Gramática**:
```
S -> ab | ba
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: Acepta exactamente "ab" O "ba".

**Verificación a papel**:
```
FIRST(ab) = {a}
FIRST(ba) = {b}

Son disjuntos → No hay conflicto LL(1)

Tabla LL(1):
M[S, a] = S → ab
M[S, b] = S → ba
```

**Test strings**:
- `ab` → yes
- `ba` → yes
- `aa` → no
- `bb` → no
- `aba` → no (solo 2 caracteres)

---

## Example 13: `example13_nested.txt` - Both (Anidamiento Balanceado)

**Gramática**:
```
S -> aSb | e
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: Genera cadenas balanceadas: n 'a's seguidas de n 'b's (a^n b^n).

**Verificación a papel - Derivaciones**:
```
Para "ab":
  S → aSb → a(e)b → ab ✓

Para "aabb":
  S → aSb → a(aSb)b → a(a(e)b)b → aabb ✓

Para "aaabbb":
  S → aSb → a(aSb)b → a(a(aSb)b)b → a(a(a(e)b)b)b → aaabbb ✓

Para "aab":
  S → aSb → a(aSb)b = ?
  Para generar "aab" necesitaríamos a^2 b^1, imposible ✗
```

**FIRST/FOLLOW**:
```
FIRST(S) = {a, ε}
FOLLOW(S) = {b, $}

Tabla LL(1):
M[S, a] = S → aSb
M[S, b] = S → e
M[S, $] = S → e
```

**Test strings**:
- `ab` → yes (1a, 1b)
- `aabb` → yes (2a, 2b)
- `aaabbb` → yes (3a, 3b)
- `aab` → no (2a, 1b - desbalanceado)
- `b` → no (0a, 1b - desbalanceado)

---

## Example 14: `example14_simple_both.txt` - Both (Combinaciones Opcionales)

**Gramática**:
```
S -> AB
A -> a | e
B -> b | e
```

**Tipo**: Both LL(1) and SLR(1)

**Descripción**: Genera todas las combinaciones de 'a' opcional y 'b' opcional: "", "a", "b", "ab".

**Verificación a papel - Todas las derivaciones**:
```
Para "":
  S → AB → (e)(e) → ε ✓

Para "a":
  S → AB → (a)(e) → a ✓

Para "b":
  S → AB → (e)(b) → b ✓

Para "ab":
  S → AB → (a)(b) → ab ✓

Para "aa":
  S → AB → (a)(a) ✗ (B no puede ser 'a')
```

**FIRST/FOLLOW**:
```
FIRST(S) = FIRST(A) = {a, ε}
  Si A→e, entonces agregar FIRST(B) = {b, ε}
  Resultado: FIRST(S) = {a, b, ε}

FIRST(A) = {a, ε}
FIRST(B) = {b, ε}

FOLLOW(S) = {$}
FOLLOW(A) = FIRST(B) - {ε} ∪ FOLLOW(S) = {b, $}
FOLLOW(B) = FOLLOW(S) = {$}

Tabla LL(1):
M[S, a] = S → AB
M[S, b] = S → AB
M[S, $] = S → AB
M[A, a] = A → a
M[A, b] = A → e
M[A, $] = A → e
M[B, b] = B → b
M[B, $] = B → e
```

**Test strings**:
- `ab` → yes
- `a` → yes
- `b` → yes
- `` (vacío) → yes
- `aa` → no (solo una 'a')

---

## Resumen de Ejemplos Simples

| Example | Gramática | Tipo | Acepta | Concepto |
|---------|-----------|------|--------|----------|
| 5 | S → aSa \| bSb \| e | Neither | Palíndromos complejos | Conflictos FIRST/FOLLOW |
| 6 | S → S+n \| n | SLR(1) | n, n+n, n+n+n | Recursión izquierda |
| 7 | S → aS \| Sa \| a | Neither | - | Ambigüedad |
| 8 | S → a | Both | a | Más simple |
| 9 | S → aA; A → b | Both | ab | Dos no terminales |
| 10 | S → aS \| e | Both | a* | Repetición |
| 11 | S → aAb; A → c \| e | Both | ab, acb | Opcional |
| 12 | S → ab \| ba | Both | ab, ba | Alternancia |
| 13 | S → aSb \| e | Both | aⁿbⁿ | Balanceado |
| 14 | S → AB; A,B → a/b \| e | Both | ε,a,b,ab | Combinaciones |

---

## Cómo Usar Estos Ejemplos

### Para Verificación Manual:

1. **Calcula FIRST y FOLLOW a papel**
2. **Construye la tabla LL(1)** (si aplica)
3. **Traza la derivación** de las cadenas de prueba
4. **Compara con el output del programa**

### Para Probar:

```bash
# Ejemplo individual
python3 main.py < examples/example8_single_terminal.txt

# Todos los ejemplos simples
for i in {5..14}; do
    echo "=== Example $i ==="
    python3 main.py < examples/example${i}_*.txt 2>&1 | head -6
    echo ""
done
```

---

## Tips para Verificación a Papel

1. **FIRST**: Anota qué terminales pueden empezar cada producción
2. **FOLLOW**: Anota qué puede venir después de cada no terminal
3. **Tabla LL(1)**: Una fila por no terminal, una columna por terminal
4. **Derivación**: Escribe cada paso de la transformación
5. **Pila (LL1)**: Simula la pila paso a paso

**Ejemplo de verificación para S → a:**
```
1. FIRST(S) = {a}
2. FOLLOW(S) = {$}
3. Tabla: M[S,a] = S→a
4. Para "a":
   Pila: [$, S] → [$, a] → [$] → [] ✓
```

¡Estos ejemplos son perfectos para practicar parsing a mano y entender los conceptos fundamentales!
