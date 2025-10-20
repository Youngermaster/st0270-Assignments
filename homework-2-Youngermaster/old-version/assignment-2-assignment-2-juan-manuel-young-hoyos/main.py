def eliminate_left_recursion():
    import sys
    
    sys.setrecursionlimit(10**7)
    
    # ----------------------------------------
    # 1) Parsing Input
    # ----------------------------------------
    input_data = sys.stdin.read().strip().splitlines()
    # First line is number of test cases:
    t = int(input_data[0].strip())
    pointer = 1
    
    # We'll define a helper function to get the next available capital letter.
    def next_new_nonterminal(used_nonterminals):
        # We want a single capital letter from A..Z that is not used.
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if c not in used_nonterminals:
                return c
        # If all letters used, raise an error or fallback to something else
        raise ValueError("Ran out of single-letter nonterminals!")
    
    # ----------------------------------------
    # For each test case, parse grammar, eliminate left recursion, then print.
    # ----------------------------------------
    results = []  # We'll collect the output for each test case.
    
    for _case_i in range(t):
        # k = number of nonterminals
        k = int(input_data[pointer].strip())
        pointer += 1
        
        # Grammar stored as:
        #    grammar[NT] = list of alternatives
        # Each alternative is a list of tokens: uppercase=NT, lowercase=terminal, 'e'=epsilon
        grammar = {}
        order_of_nt = []  # to preserve the order in which nonterminals appear
        
        # We'll parse k lines of productions
        used_nonterminals = set()
        
        for _ in range(k):
            line = input_data[pointer].strip()
            pointer += 1
            # e.g.  "S -> Sa b"
            lhs, rhs_part = line.split("->")
            lhs = lhs.strip()
            used_nonterminals.add(lhs)
            
            # The right side has alternatives separated by spaces.
            # For example: "Sa b" => alternatives "Sa" and "b"
            # Each alternative can be multiple tokens concatenated
            # (e.g., "Sa" => [ 'S','a' ])
            rhs_alts = rhs_part.strip().split()
            
            # parse each alt into a list of tokens
            # Each token is either uppercase (nonterminal) or lowercase (terminal)
            # or 'e' for epsilon.
            alternatives = []
            for alt in rhs_alts:
                # alt is a string like "Sa" or "b" or "Ac".
                # We'll parse it character by character:
                tokens = []
                for ch in alt:
                    tokens.append(ch)
                alternatives.append(tokens)
            
            grammar[lhs] = alternatives
            order_of_nt.append(lhs)
        
        # Because we might create new nonterminals, keep track of them in order_of_nt as well.
        # We'll do the standard left recursion elimination (Aho, §4.3.3):
        
        def eliminate_immediate_left_recursion(A):
            """
            Eliminate immediate left recursion on the productions of nonterminal A.
            Grammar is stored in 'grammar' dict. Modifies grammar in place.
            If A -> A alpha_1 | ... | A alpha_r | beta_1 | ... | beta_s
            with each beta_i not starting with A,
            then we rewrite as:
               A -> beta_1 A' | ... | beta_s A'
               A' -> alpha_1 A' | ... | alpha_r A' | e
            """
            prods = grammar[A]  # all alternatives for A
            alpha_parts = []
            beta_parts = []
            
            for alt in prods:
                if len(alt) > 0 and alt[0] == A:
                    # Then we have A -> A alpha
                    # alpha is alt[1..]
                    alpha_parts.append(alt[1:])
                else:
                    # A -> beta
                    beta_parts.append(alt)
            
            if len(alpha_parts) == 0:
                # no immediate left recursion, do nothing
                return
            
            # We do have immediate left recursion. We'll create a new nonterminal A'.
            Aprime = next_new_nonterminal(used_nonterminals)
            used_nonterminals.add(Aprime)
            
            # Replace productions of A
            #    A -> beta_1 A' | ... | beta_s A'
            new_A_productions = []
            for beta in beta_parts:
                new_A_productions.append(beta + [Aprime])  # append A' at the end
            
            grammar[A] = new_A_productions
            
            # Define A' -> alpha_1 A' | ... | alpha_r A' | e
            new_Aprime_productions = []
            for alpha in alpha_parts:
                new_Aprime_productions.append(alpha + [Aprime])  # alpha then A'
            # plus epsilon
            new_Aprime_productions.append(['e'])
            
            grammar[Aprime] = new_Aprime_productions
            order_of_nt.append(Aprime)  # so we can eventually print it in some order
        
        # We implement the 2-level loop for indirect recursion:
        # Let the nonterminals be A1, A2, ..., A_k in the input order.
        # for i in range(len(order_of_nt)):  # but we must be careful with newly added NTs
        # A more standard approach is to walk only the *original* order for i,
        # but still handle expansions for j < i. Then do immediate left recursion on Ai.
        
        # Convert order_of_nt to a stable list, ignoring newly introduced ones at the time of the loop.
        # We'll do the loop over the original nonterminals first. If new nonterminals appear, they won't cause more expansions in the Aho algorithm.
        original_nts = list(order_of_nt)  # snapshot
        
        for i in range(len(original_nts)):
            Ai = original_nts[i]
            
            # For j in 0..i-1, replace Ai->Aj alpha by Ai->(productions of Aj) alpha
            for j in range(i):
                Aj = original_nts[j]
                new_prods = []
                changed_something = False
                for alt in grammar[Ai]:
                    if len(alt) > 0 and alt[0] == Aj:
                        # expand
                        changed_something = True
                        # For each production Aj -> gamma
                        for gamma in grammar[Aj]:
                            new_prods.append(gamma + alt[1:])
                    else:
                        new_prods.append(alt)
                if changed_something:
                    grammar[Ai] = new_prods
            
            # Now eliminate immediate left recursion for Ai
            eliminate_immediate_left_recursion(Ai)
        
        # ----------------------------------------
        # Output: print the resulting grammar in the same format:
        # A -> alpha1 alpha2 ...
        # use 'e' for epsilon
        # each alternative separated by a space, no extra lines except one blank line between cases
        # We'll keep track of all nonterminals encountered in order_of_nt
        # but might have duplicates if we appended the same new nonterminal multiple times.
        # We'll do a final pass to get them in the order they first appeared.
        # ----------------------------------------
        
        final_seen = set()
        final_ordered_nts = []
        for nt in order_of_nt:
            if nt not in final_seen and nt in grammar:
                final_seen.add(nt)
                final_ordered_nts.append(nt)
        
        # Build the textual output
        case_output_lines = []
        for nt in final_ordered_nts:
            # gather each alt, flatten to string (with no spaces), and join with space
            alts_str = []
            for alt in grammar[nt]:
                # alt is a list of tokens
                # if it's ['e'], that means epsilon
                if alt == ['e']:
                    alts_str.append('e')
                else:
                    alts_str.append("".join(alt))
            line = f"{nt} -> {' '.join(alts_str)}"
            case_output_lines.append(line)
        
        results.append("\n".join(case_output_lines))
    
    # Print all test cases, each separated by a blank line
    print("\n\n".join(results))


if __name__ == "__main__":
    # You can run this file directly.  It will read from standard input.
    # For example, with the sample input in the PDF, you might do:
    #
    #   python left_recursion.py  <  sample_input.txt
    #
    # The output should match the left‐recursion‐eliminated grammar.
    #
    eliminate_left_recursion()
