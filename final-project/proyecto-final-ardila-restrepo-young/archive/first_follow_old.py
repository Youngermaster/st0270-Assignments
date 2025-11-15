"""
Pure, unit-test-friendly algorithms for FIRST / FOLLOW.
They do not mutate Grammar - they only *read* it and return dicts.
"""

from typing import Dict, List, Set

from .utils import is_terminal, is_nonterminal
from .grammar import Grammar, Symbol


def compute_first_sets(G: Grammar) -> Dict[Symbol, Set[Symbol]]:
    first: Dict[Symbol, Set[Symbol]] = {t: {t} for t in G.terminals | {"e"}} | {
        nt: set() for nt in G.nonterminals
    }

    changed = True
    while changed:
        changed = False
        for A, rhs_list in G.productions.items():
            for rhs in rhs_list:
                # ε-production
                if rhs == ["e"]:
                    if "e" not in first[A]:
                        first[A].add("e")
                        changed = True
                    continue

                for sym in rhs:
                    before = len(first[A])
                    first[A] |= first[sym] - {"e"}
                    if "e" not in first[sym]:
                        break
                    if before != len(first[A]):
                        changed = True
                else:  # all symbols derive ε
                    if "e" not in first[A]:
                        first[A].add("e")
                        changed = True
    return first


def compute_follow_sets(G: Grammar) -> Dict[Symbol, Set[Symbol]]:
    follow: Dict[Symbol, Set[Symbol]] = {nt: set() for nt in G.nonterminals}
    follow["S"].add("$")  # start symbol’s FOLLOW gets $

    changed = True
    while changed:
        changed = False
        for A, rhs_list in G.productions.items():
            for rhs in rhs_list:
                for i, B in enumerate(rhs):
                    if is_nonterminal(B):
                        beta = rhs[i + 1 :]
                        first_beta = G.first_of_string(beta)
                        before = len(follow[B])
                        follow[B] |= first_beta - {"e"}
                        if "e" in first_beta or not beta:
                            follow[B] |= follow[A]
                        changed |= before != len(follow[B])
    return follow
