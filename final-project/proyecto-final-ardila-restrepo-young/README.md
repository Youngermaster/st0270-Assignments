# Context-Free Grammar Analyser - LL(1) & SLR(1)

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/CgVx9Psf)

Tiny, dependency-free Python package that:

* computes **FIRST** / **FOLLOW** sets  
* builds predictive-parsing tables for **LL(1)**  
* builds ACTION / GOTO tables for **SLR(1)**  
* lets you parse input strings interactively from the CLI.

## Authors

* Jean Carlo Ardila Acevedo  
* Andres Felipe Restrepo Giraldo  
* Juan Manuel Young Hoyos

## Tested environment

| OS | Python |
|----|--------|
| Ubuntu 24.04 LTS | 3.12.9 |
| macOS 15.4.1     | 3.12.9 |

> The code uses only the standard library, so anything ≥ 3.9 should work.

## Quick start

### 1 · Run the program

```bash
# preferred: package entry-point
python -m cfp

# explicit (same result)
python -m cfp.cli
```

### 2 · Feed a grammar

```plaintext
3
S -> S+T T
T -> T*F F
F -> (S) i
```

### 3 · See what the analyser says

```plaintext
Grammar is SLR(1).
```

### 4 · Parse some strings (end with an empty line)

```plaintext
i+i
yes
(i)
yes
(i+i)*i)
no

<empty line pressed — session ends>
```

### What if the grammar is both LL(1) and SLR(1)?

The tool will prompt:

```plaintext
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
```

* **T** → LL(1) predictive parser
* **B** → SLR(1) bottom-up parser
* **Q** → return to grammar prompt / exit

## Project layout

```plaintext
cfp/
├── __init__.py         # package marker
├── __main__.py         # allows `python -m cfp`
├── cli.py              # console UI
├── grammar.py          # Grammar class + helpers
├── first_follow.py     # FIRST/FOLLOW algorithms (pure functions)
├── ll1.py              # LL(1) table builder + parser
├── slr1.py             # SLR(1) table builder + parser
└── utils.py            # misc helpers (tokens, flatten, predicates)
```

## 📝 Input format

```plaintext
n                     # number of non-terminals
A -> α β γ            # exactly n lines, one per non-terminal
...
```

* `ε` is written as the single letter `e`.
* End-of-input marker is `$` (added automatically, do **not** use it in the grammar).
* Each alternative is separated by whitespace.

## Minimal smoke test

```bash
python -m cfp <<'EOF'
3
S -> S+T T
T -> T*F F
F -> (S) i
EOF
```

Output should be exactly:

```plaintext
Grammar is SLR(1).
```

## 📜 License

MIT — see `LICENSE` file.
