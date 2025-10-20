# Left Recursion Elimination

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5d8IV8cj)

## Authors

- Juan Manuel Young Hoyos

## Overview

This project implements the algorithms from [Aho et al. (2006), *Compilers: Principles, Techniques, and Tools* (2nd Ed.) Section 4.3.3] to eliminate both direct and indirect left recursion from a context-free grammar.

The program reads grammars from standard input, applies the left recursion elimination procedure, and prints an equivalent grammar without left recursion. We assume:
- The initial symbol is **S**.
- Nonterminals are single uppercase letters.
- Terminals are lowercase letters.
- **e** denotes the empty string (epsilon).
- No cycles in the grammar.
- No epsilon-productions in the original grammar.

---

## Environment and Versions

- **Operating System:** [e.g., Ubuntu 22.04 / Windows 11 / macOS Ventura]
- **Programming Language:** Python [3.x]
- **Other Tools Used:** None (standard library only)

---

## How to Run

1. **Clone** or **download** this repository.
2. **Navigate** to the directory containing the file `left_recursion.py`.
3. **Prepare** an input file (e.g., `input.txt`) following the specified format:
   - First line: number of test cases (integer).
   - For each test case:
     1. An integer **k**, the number of nonterminals.
     2. **k** lines, each containing:

        ```bash
        <Nonterminal> -> <Alternative1> <Alternative2> ...
        ```

      where each `<Alternative>` is a sequence of terminals/nonterminals (no spaces within a single alternative).
      For epsilon, use `e`.
4. **Run**:

   ```bash
   python left_recursion.py < input.txt
   ```

   The program will print the transformed grammar(s) to standard output, separating each test case’s output with a blank line.

---

## Explanation of the Algorithm

The algorithm is based on the formal procedure described in Section 4.3.3 of the “Dragon Book” (*Compilers: Principles, Techniques, and Tools* by Aho, Sethi, and Ullman, 2nd Edition). It proceeds in two main phases:

1. **Indirect Left Recursion Removal**  
   For nonterminals \(A_1, A_2, \ldots, A_n\) in the grammar, we systematically replace any production of the form
   \[
       A_i \rightarrow A_j\,\alpha
   \]
   (where \(j < i\)) with
   \[
       A_i \rightarrow \beta\,\alpha
   \]
   for each production \(A_j \rightarrow \beta\). This step ensures no production introduces a left recursion path indirectly.

2. **Immediate Left Recursion Elimination**  
   For any nonterminal \(A\) with productions of the form
   \[
       A \rightarrow A\,\alpha_1 \;|\;\cdots\;|\; A\,\alpha_r \;|\; \beta_1 \;|\;\cdots\;|\; \beta_s
   \]
   (where each \(\beta_i\) does **not** start with \(A\)), we introduce a new nonterminal \(A'\) and rewrite:
   \[
       A \rightarrow \beta_1 A' \;|\;\cdots\;|\; \beta_s A'
   \]
   \[
       A' \rightarrow \alpha_1 A' \;|\;\cdots\;|\; \alpha_r A' \;|\; e
   \]
   This removes any direct left recursion in the resulting grammar.

After these steps, the grammar will be free of left recursion while preserving the language it generates.
