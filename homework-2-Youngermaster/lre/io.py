from typing import List
from .grammar import Grammar, Production

def parse_cases_from_lines(lines: List[str]) -> List[Grammar]:
    """
    Input format:
      t
      (repeat t times)
        k
        k lines:  LHS -> RHS1 RHS2 ... RHSm
      - Symbols are 1-char (A..Z for NT, a..z for terminals).
      - 'e' denotes epsilon on output only (input has no epsilon).
    """
    ptr = 0
    t = int(lines[ptr]); ptr += 1
    cases: List[Grammar] = []

    for _ in range(t):
        k = int(lines[ptr]); ptr += 1
        G = Grammar(start="S")

        for _ in range(k):
            line = lines[ptr]; ptr += 1
            lhs_raw, rhs_raw = line.split("->")
            A = lhs_raw.strip()
            rhs_items = rhs_raw.strip().split()

            alts: List[Production] = []
            for item in rhs_items:
                alts.append([ch for ch in item])  # split into 1-char symbols

            G.add_nonterminal(A, alts)

        cases.append(G)

    return cases
