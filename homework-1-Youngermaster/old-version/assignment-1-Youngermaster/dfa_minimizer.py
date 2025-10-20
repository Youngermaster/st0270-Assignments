"""
DFA Minimization Algorithm

This module contains the main DFAMinimizer class that implements the DFA minimization
algorithm from Kozen 1997 (Lecture 14).
"""

from typing import List, Set, Tuple, Dict
from utils import InputParser, StateUtils, PairUtils


class DFAMinimizer:
    """
    DFA Minimizer implementing Kozen's algorithm for finding equivalent states.
    
    The algorithm works by:
    1. Removing inaccessible states
    2. Initially marking pairs where one state is final and other is not
    3. Iteratively refining by marking pairs whose transitions lead to already marked pairs
    4. Returning unmarked pairs as equivalent states
    """
    
    def __init__(self):
        self.parser = InputParser()
        self.state_utils = StateUtils()
        self.pair_utils = PairUtils()
    
    def process_input_file(self, filename: str) -> List[str]:
        """
        Process all test cases from the input file.
        
        Args:
            filename: Path to the input file
            
        Returns:
            List of output strings, one per test case
        """
        with open(filename, 'r') as file:
            content = file.read().strip()
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        num_cases = int(lines[0])
        
        results = []
        line_index = 1
        
        for _ in range(num_cases):
            result, line_index = self._process_single_case(lines, line_index)
            results.append(result)
            
        return results
    
    def _process_single_case(self, lines: List[str], start_index: int) -> Tuple[str, int]:
        """
        Process a single DFA test case.
        
        Args:
            lines: All input lines
            start_index: Index to start reading from
            
        Returns:
            Tuple of (result string, next line index)
        """
        # Parse DFA components
        num_states = int(lines[start_index])
        start_index += 1
        
        alphabet = lines[start_index].split()
        start_index += 1
        
        final_states = set(map(int, lines[start_index].split()))
        start_index += 1
        
        # Parse transition table
        transition_lines = lines[start_index:start_index + num_states]
        transitions = self.parser.parse_transitions(transition_lines)
        start_index += num_states
        
        # Find equivalent state pairs
        equivalent_pairs = self._minimize_dfa(
            num_states, alphabet, final_states, transitions
        )
        
        # Format output
        output = self.pair_utils.format_pairs(equivalent_pairs)
        return output, start_index
    
    def _minimize_dfa(
        self, 
        num_states: int, 
        alphabet: List[str], 
        final_states: Set[int], 
        transitions: List[List[int]]
    ) -> List[Tuple[int, int]]:
        """
        Apply the DFA minimization algorithm to find equivalent state pairs.
        
        Args:
            num_states: Number of states in the DFA
            alphabet: List of alphabet symbols
            final_states: Set of final states
            transitions: Transition table
            
        Returns:
            List of equivalent state pairs
        """
        # Remove inaccessible states (though input assumes none exist)
        reachable_states = self.state_utils.find_reachable_states(
            transitions, alphabet, initial_state=0
        )
        reachable = sorted(list(reachable_states))
        
        # Generate all ordered pairs (p, q) with p < q
        pairs = [(p, q) for p in reachable for q in reachable if p < q]
        
        # Initially mark pairs where one state is final and other is not
        marked = self._mark_initial_pairs(pairs, final_states)
        
        # Iteratively refine the marked set
        marked = self._refine_marked_pairs(pairs, alphabet, transitions, marked)
        
        # Equivalent pairs are those not marked
        equivalent_pairs = [
            pair for pair in pairs 
            if pair not in marked
        ]
        
        # Sort lexicographically
        return sorted(equivalent_pairs)
    
    def _mark_initial_pairs(
        self, 
        pairs: List[Tuple[int, int]], 
        final_states: Set[int]
    ) -> Set[Tuple[int, int]]:
        """
        Mark pairs where one state is final and the other is not.
        
        Args:
            pairs: All state pairs to consider
            final_states: Set of final states
            
        Returns:
            Set of initially marked pairs
        """
        marked = set()
        
        for p, q in pairs:
            p_is_final = p in final_states
            q_is_final = q in final_states
            
            if p_is_final != q_is_final:
                marked.add((p, q))
                
        return marked
    
    def _refine_marked_pairs(
        self,
        pairs: List[Tuple[int, int]],
        alphabet: List[str],
        transitions: List[List[int]],
        marked: Set[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        """
        Iteratively refine the set of marked pairs.
        
        Args:
            pairs: All state pairs to consider
            alphabet: List of alphabet symbols  
            transitions: Transition table
            marked: Initially marked pairs
            
        Returns:
            Final set of marked (non-equivalent) pairs
        """
        changed = True
        
        while changed:
            new_marked = set(marked)
            
            for p, q in pairs:
                if (p, q) not in marked:
                    # Check if any symbol transition leads to a marked pair
                    should_mark = False
                    
                    for symbol_index in range(len(alphabet)):
                        p_next = transitions[p][symbol_index]
                        q_next = transitions[q][symbol_index]
                        
                        if p_next != q_next:
                            # Create canonical (ordered) pair
                            canonical_pair = self.pair_utils.canonical_pair(p_next, q_next)
                            
                            if canonical_pair in new_marked:
                                should_mark = True
                                break
                    
                    if should_mark:
                        new_marked.add((p, q))
            
            changed = len(new_marked) != len(marked)
            marked = new_marked
            
        return marked