# DFA Minimization Algorithm - Python Implementation

This is a Python conversion of the original Elixir implementation, following best practices for Python development.

## Project Structure

```markdown
├── main.py              # Entry point for the program
├── dfa_minimizer.py     # Main DFAMinimizer class with core algorithm
├── utils.py             # Utility classes (InputParser, StateUtils, PairUtils, ValidationUtils)
├── input.txt            # Input file with DFA test cases
└── requirements.txt     # Dependencies (none - uses standard library only)
```

## Running the Python Implementation

1. **Prerequisites:**

   - Python 3.6+ (tested with Python 3.8+)
   - No external dependencies required

2. **Execute:**

   ```bash
   python3 main.py
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

### Algorithm Implementation

The Python version faithfully implements the same algorithm as the Elixir version:

1. **Input Processing**: Parses multiple test cases from input.txt
2. **State Reachability**: BFS to find all reachable states
3. **Initial Marking**: Mark pairs where one state is final and other is not
4. **Iterative Refinement**: Mark pairs whose transitions lead to already marked pairs
5. **Output Formatting**: Return unmarked pairs as equivalent states

## Verification

The Python implementation produces identical output to the original Elixir version:

```bash
(1, 2) (3, 4)
(1, 2) (3, 4) (3, 5) (4, 5)
(0, 3) (1, 4) (2, 5)
(0, 1)
```

## Development Notes

- Uses only Python standard library (no external dependencies)
- Follows PEP 8 style guidelines
- Implements proper error handling and input validation
- Designed for maintainability and extensibility
