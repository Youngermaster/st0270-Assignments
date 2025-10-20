# Assignment 1 - C2566-ST0270-3952

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/LWRaO1j1)
[![Work in MakeCode](https://classroom.github.com/assets/work-in-make-code-8824cc13a1a3f34ffcd245c82f0ae96fdae6b7d554b6539aec3a03a70825519c.svg)](https://classroom.github.com/online_ide?assignment_repo_id=20051665&assignment_repo_type=AssignmentRepo)

This project implements the DFA minimization algorithm described in Kozen 1997 (Lecture 14) as an assignment for the Formal Languages and Compilers course. This is a Python implementation that follows best practices for Python development.

## Student Information

- **Name:** Juan Manuel Young Hoyos
- **Class Number:** C2566-ST0270-3952-2025-2

## Environment and Tools

- **Operating System:** MacOS Sequoia (15.3)
- **Programming Language:** Python 3.6+ (tested with Python 3.8+)

## Project Structure

```bash
├── main.py                    # Entry point for the program
├── dfa_minimizer.py           # Main DFAMinimizer class with core algorithm
├── utils.py                   # Utility classes (InputParser, StateUtils, PairUtils, ValidationUtils)
├── input.txt                  # Input file with DFA test cases
├── requirements.txt           # Dependencies (none - uses standard library only)
├── README.md                  # Project documentation
└── Homework1_minimization.pdf # Assignment description and requirements
```

## Running the Implementation

1. **Prerequisites:**

   - Python 3.6+ (tested with Python 3.8+)
   - No external dependencies required

2. **Execute the Code:**
   Run the program from the command line with:

   ```bash
   python3 main.py
   ```

   The program will read the DFA definitions from `input.txt` and output the pairs of equivalent states in lexicographical order.

3. **Expected Output:**
   Running the code should produce output similar to:

   ```plaintext
   (1, 2) (3, 4)
   (1, 2) (3, 4) (3, 5) (4, 5)
   (0, 3) (1, 4) (2, 5)
   (0, 1)
   ```

## Architecture and Best Practices

### Object-Oriented Design

- **DFAMinimizer**: Main class implementing the minimization algorithm
- **InputParser**: Handles parsing of transition tables
- **StateUtils**: Utilities for state operations and reachability analysis
- **PairUtils**: Utilities for working with state pairs
- **ValidationUtils**: Input validation and error checking

### Code Quality Features

- **Type Hints**: Full type annotations for better code documentation and IDE support
- **Docstrings**: Comprehensive documentation for all classes and methods
- **DRY Principle**: Reusable utility functions avoid code duplication
- **Separation of Concerns**: Each class has a single, well-defined responsibility
- **Error Handling**: Input validation with descriptive error messages

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

### Algorithm Implementation Steps

The Python implementation faithfully follows these steps:

1. **Input Processing**: Parses multiple test cases from input.txt
2. **State Reachability**: BFS to find all reachable states
3. **Initial Marking**: Mark pairs where one state is final and other is not
4. **Iterative Refinement**: Mark pairs whose transitions lead to already marked pairs
5. **Output Formatting**: Return unmarked pairs as equivalent states

## Verification

The Python implementation produces identical output to the original Elixir version and follows the expected algorithm behavior as described in Kozen's textbook.

## Development Notes

- Uses only Python standard library (no external dependencies)
- Follows PEP 8 style guidelines
- Implements proper error handling and input validation
- Designed for maintainability and extensibility
- Originally converted from an Elixir implementation

## References

- Kozen, Dexter C. (1997). _Automata and Computability_. 1st edition, Berlin, Heidelberg: Springer-Verlag. doi: [10.1007/978-1-4612-1844-9](https://doi.org/10.1007/978-1-4612-1844-9).
