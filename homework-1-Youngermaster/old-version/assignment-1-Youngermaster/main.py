#!/usr/bin/env python3
"""
DFA Minimization Algorithm Implementation

This module implements the DFA minimization algorithm described in Kozen 1997 (Lecture 14).
It reads DFA definitions from input.txt and outputs pairs of equivalent states.

Author: Converted from Elixir to Python
"""

from dfa_minimizer import DFAMinimizer


def main():
    """Entry point for the DFA minimization program."""
    minimizer = DFAMinimizer()
    results = minimizer.process_input_file("input.txt")
    
    for result in results:
        print(result)


if __name__ == "__main__":
    main()