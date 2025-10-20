from typing import List
from .grammar import Grammar, Production

def eliminate_immediate_left_recursion(G: Grammar, A: str) -> None:
    """
    Aho §4.3.3 immediate step:
      A -> A α1 | ... | A αr | β1 | ... | βs,   (βi do not start with A)
      =>
      A  -> β1 A' | ... | βs A'
      A' -> α1 A' | ... | αr A' | e
    """
    alts = G.prods[A]
    alpha: List[Production] = []
    beta:  List[Production] = []
    for prod in alts:
        if len(prod) > 0 and prod[0] == A:
            alpha.append(prod[1:])
        else:
            beta.append(prod)

    if not alpha:
        return  # nothing to do (no immediate left recursion)

    A1 = G.next_fresh_nonterminal()

    # A -> beta A'
    new_A: List[Production] = []
    if beta:
        for b in beta:
            new_A.append(b + [A1])
    else:
        # degenerate case: A had only A αi
        new_A.append([A1])

    # A' -> alpha A' | e
    new_A1: List[Production] = [a + [A1] for a in alpha]
    new_A1.append(["e"])

    G.set_productions(A, new_A)
    G.add_nonterminal(A1, new_A1)


def eliminate_left_recursion(G: Grammar) -> Grammar:
    """
    Aho §4.3.3:
      Let A1..An be the nonterminals in the *original* order.
      for i = 1..n:
        for j = 1..i-1:
          replace Ai -> Aj γ by Ai -> δ1 γ | ... | δm γ for all Aj -> δ1|...|δm
        eliminate immediate left recursion on Ai
    """
    original = list(G.order)  # snapshot: only the originals are Ai's

    for i, Ai in enumerate(original):
        # Expand leading Aj (j < i) in Ai's productions
        for j in range(i):
            Aj = original[j]
            expanded: List[Production] = []
            changed = False
            for prod in G.prods[Ai]:
                if len(prod) > 0 and prod[0] == Aj:
                    changed = True
                    tail = prod[1:]
                    for gamma in G.prods[Aj]:
                        expanded.append(gamma + tail)
                else:
                    expanded.append(prod)
            if changed:
                G.set_productions(Ai, expanded)

        # Remove immediate left recursion on Ai
        eliminate_immediate_left_recursion(G, Ai)

    return G
