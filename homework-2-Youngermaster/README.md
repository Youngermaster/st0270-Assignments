# Left-Recursion Elimination (Aho et al., 2006 §4.3.3)

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/offgSnTp)

## Authors

- Juan Manuel Young Hoyos

## Overview

This project implements exactly the algorithm from **Aho et al. (2006), _Compilers: Principles, Techniques, and Tools_ (2nd Ed.) §4.3.3** to eliminate **indirect** and **immediate** left recursion from a context-free grammar.

Key implementation details:

- Fresh nonterminals are chosen by scanning **Z, Y, X, …, A** (descending), matching the expected outputs.
- Printing order: original nonterminals in input order, then any fresh ones **appended at the end**.
- Output has **no blank line between test cases** (as in the course samples).

## Project Layout

```bash
lre/grammar.py          # grammar container + printing
lre/left_recursion.py   # Aho §4.3.3 algorithm
lre/io.py               # input parser
main.py                 # CLI entry point
```

## Assumptions

- Start symbol is **S**.
- Nonterminals are **single uppercase** letters (`A..Z`).
- Terminals are **lowercase** letters.
- Input grammars **do not** contain epsilon; the algorithm introduces epsilon as `e` in the output where required.
- No cycles in the input.

## Environment

- **Python** ≥ 3.8 (tested on 3.12+)
- Standard library only

## Input Format

```bash
t
k <LHS> -> <Alt1> <Alt2> ... <Altm>
...
(repeat k lines)
(repeat for t test cases)
```

- Each `<Alt>` is a **sequence of 1-char symbols** with **no spaces inside** (e.g., `Sa`, `b`, `Ac`).
- On **output**, `e` denotes epsilon.

## Output Format

- One production per line, same LHS order as input (fresh nonterminals appended).
- **No blank line** between cases.
- Epsilon printed as `e`.

## How to Run

From the project root:

```bash
# read from stdin
python main.py < input.txt

# or pass a path
python main.py input.txt
````

## Example

**Input:**

```bash
3
1
S -> Sa b
2
S -> Aa b
A -> Ac Sd m
2
S -> Sa Ab
A -> Ac Sc c
```

**Output:**

```bash
S -> bZ
Z -> aZ e

S -> Aa b
A -> bdZ mZ
Z -> cZ adZ e

S -> AbZ
A -> cY
Z -> aZ e
Y -> cY bZcY e
```

## Algorithm (Aho §4.3.3)

Let the original nonterminals be \$A\_1, A\_2, \dots, A\_n\$ in input order.

1. **Remove indirect left recursion**
   For each \$i=1..n\$ and for each \$j=1..i-1\$, replace every production

   $A_i \rightarrow A_j\,\alpha$

   by

   $A_i \rightarrow \beta_1\alpha \ \mid\ \cdots \ \mid\ \beta_m\alpha$

   for all productions \$A\_j \rightarrow \beta\_1 \mid \cdots \mid \beta\_m\$.

2. **Eliminate immediate left recursion** (for the current \$A\_i\$)
   If

   $A \rightarrow A\,\alpha_1 \ \mid\ \cdots \ \mid\ A\,\alpha_r \ \mid\ \beta_1 \ \mid\ \cdots \ \mid\ \beta_s$

   with each \$\beta\_i\$ **not** starting with \$A\$, introduce a fresh \$A'\$ (chosen from \$Z,Y,\dots\$) and rewrite:

   $A \rightarrow \beta_1 A' \ \mid\ \cdots \ \mid\ \beta_s A', \qquad$
   $A' \rightarrow \alpha_1 A' \ \mid\ \cdots \ \mid\ \alpha_r A' \ \mid\ e.$

After these two phases (performed for \$i=1\$ to \$n\$), the grammar is free of left recursion and generates the same language.

## Notes

- If a nonterminal has **only** immediate left-recursive alternatives (no \$\beta\_i\$), we emit:

  ```bash
  A -> A'
  A' -> α1 A' | ... | αr A' | e
  ```

  to keep the grammar well-formed.

- The algorithm preserves determinism of naming and ordering so results are stable for testing/autograding.
