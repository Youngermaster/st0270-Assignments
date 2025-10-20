"""
Utility functions and classes for DFA minimization.

This module contains helper classes that support the main DFA minimization algorithm.
"""

from typing import List, Set, Tuple
from collections import deque


class InputParser:
    """Handles parsing of DFA input data."""
    
    @staticmethod
    def parse_transitions(transition_lines: List[str]) -> List[List[int]]:
        """
        Parse transition table lines into a structured format.
        
        Each line contains: state_number followed by transitions for each alphabet symbol.
        Returns a list where index i contains transitions for state i.
        
        Args:
            transition_lines: Lines containing transition data
            
        Returns:
            List of transition lists, indexed by state number
        """
        # Parse each line and extract state number and transitions
        parsed_transitions = []
        
        for line in transition_lines:
            values = list(map(int, line.split()))
            state_num = values[0]
            transitions = values[1:]
            parsed_transitions.append((state_num, transitions))
        
        # Sort by state number to ensure correct indexing
        parsed_transitions.sort(key=lambda x: x[0])
        
        # Extract just the transition lists
        return [transitions for _, transitions in parsed_transitions]


class StateUtils:
    """Utilities for state operations and reachability analysis."""
    
    @staticmethod
    def find_reachable_states(
        transitions: List[List[int]], 
        alphabet: List[str], 
        initial_state: int = 0
    ) -> Set[int]:
        """
        Find all states reachable from the initial state using BFS.
        
        Args:
            transitions: Transition table
            alphabet: List of alphabet symbols
            initial_state: Starting state (default: 0)
            
        Returns:
            Set of reachable state numbers
        """
        visited = set()
        queue = deque([initial_state])
        
        while queue:
            current_state = queue.popleft()
            
            if current_state in visited:
                continue
                
            visited.add(current_state)
            
            # Add all states reachable via transitions from current state
            for symbol_index in range(len(alphabet)):
                next_state = StateUtils.get_transition(transitions, current_state, symbol_index)
                if next_state not in visited:
                    queue.append(next_state)
        
        return visited
    
    @staticmethod
    def get_transition(transitions: List[List[int]], state: int, symbol_index: int) -> int:
        """
        Get the next state for a given state and symbol.
        
        Args:
            transitions: Transition table
            state: Current state
            symbol_index: Index of the alphabet symbol
            
        Returns:
            Next state number
        """
        return transitions[state][symbol_index]


class PairUtils:
    """Utilities for working with state pairs."""
    
    @staticmethod
    def canonical_pair(a: int, b: int) -> Tuple[int, int]:
        """
        Return the canonical (ordered) representation of a pair.
        
        Args:
            a: First state
            b: Second state
            
        Returns:
            Tuple with smaller state first
        """
        return (a, b) if a <= b else (b, a)
    
    @staticmethod
    def format_pairs(pairs: List[Tuple[int, int]]) -> str:
        """
        Format state pairs for output.
        
        Args:
            pairs: List of state pairs
            
        Returns:
            Formatted string representation
        """
        if not pairs:
            return ""
            
        formatted_pairs = [
            f"({p}, {q})" for p, q in pairs
        ]
        
        return " ".join(formatted_pairs)


class ValidationUtils:
    """Utilities for input validation and error checking."""
    
    @staticmethod
    def validate_dfa_input(
        num_states: int,
        alphabet: List[str],
        final_states: Set[int],
        transitions: List[List[int]]
    ) -> bool:
        """
        Validate that DFA input is well-formed.
        
        Args:
            num_states: Number of states
            alphabet: Alphabet symbols
            final_states: Set of final states
            transitions: Transition table
            
        Returns:
            True if input is valid
            
        Raises:
            ValueError: If input is malformed
        """
        # Check that we have the right number of transition rows
        if len(transitions) != num_states:
            raise ValueError(
                f"Expected {num_states} transition rows, got {len(transitions)}"
            )
        
        # Check that each state has transitions for all alphabet symbols
        for i, state_transitions in enumerate(transitions):
            if len(state_transitions) != len(alphabet):
                raise ValueError(
                    f"State {i} has {len(state_transitions)} transitions, "
                    f"expected {len(alphabet)}"
                )
        
        # Check that final states are valid
        for state in final_states:
            if state < 0 or state >= num_states:
                raise ValueError(f"Final state {state} is out of range [0, {num_states-1}]")
        
        # Check that all transition targets are valid states
        for i, state_transitions in enumerate(transitions):
            for j, target in enumerate(state_transitions):
                if target < 0 or target >= num_states:
                    raise ValueError(
                        f"Transition from state {i} on symbol {j} "
                        f"leads to invalid state {target}"
                    )
        
        return True