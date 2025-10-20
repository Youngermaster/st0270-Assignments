# Assignment 1 - C2561-ST0270-4382

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/41pgA8Qo)

This project implements the DFA minimization algorithm described in Kozen 1997 (Lecture 14) as an assignment for the Formal Languages and Compilers course.

## Student Information

- **Name:** Juan Manuel Young Hoyos
- **Class Number:** C2561-ST0270-2025-1

## Environment and Tools

- **Operating System:** MacOS Sequoia (15.3)
- **Programming Language:** Elixir 1.18.2 (compiled with Erlang/OTP 27)

## Running the Implementation

1. **Install Elixir:**  
   Ensure that Elixir is installed on your system. You can verify by running:

   ```shell
   elixir --version
   ```

2. **Files:**  
   Place the following files in the same directory:
   - `minimization.exs` (the Elixir implementation)
   - `input.txt` (the input file for the DFAs)

3. **Execute the Code:**  
   Run the program from the command line with:

   ```shell
   elixir minimization.exs
   ```

   The program will read the DFA definitions from `input.txt` and output the pairs of equivalent states in lexicographical order.

4. **Expected Output:**  
   Running the code should produce output similar to:

   ```plaintext
   (1, 2) (3, 4)
   (1, 2) (3, 4) (3, 5) (4, 5)
   (0, 3) (1, 4) (2, 5)
   (0, 1)
   ```

## Explanation of the Algorithm

The minimization algorithm implemented in this project follows the approach from Kozen's Lecture 14:

1. **Input Parsing:**  
   The DFA is described by:
   - The number of states.
   - The alphabet (symbols separated by spaces).
   - The final states.
   - A transition table where each line corresponds to a state and its transitions.

2. **Eliminating Inaccessible States:**  
   Even though the input is assumed to have no inaccessible states, a breadth-first search (BFS) starting from the initial state (state 0) is performed to ensure that only reachable states are processed.

3. **Marking Non-Equivalent Pairs:**  
   - All ordered pairs of states (p, q) with `p < q` are generated.
   - Initially, pairs where one state is final and the other is not are marked as non-equivalent.
   - Then, the algorithm iteratively refines the marking by checking for each unmarked pair whether a transition on some symbol leads to a pair already marked as non-equivalent. If so, that pair is marked as non-equivalent.

4. **Output Generation:**  
   The pairs that remain unmarked after the refinement process are equivalent states. These pairs are printed in lexicographical order, as required by the assignment.

## References

- Kozen, Dexter C. (1997). *Automata and Computability*. 1st edition, Berlin, Heidelberg: Springer-Verlag. doi: [10.1007/978-1-4612-1844-9](https://doi.org/10.1007/978-1-4612-1844-9).
