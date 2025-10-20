from dataclasses import dataclass, field
from typing import Dict, List, Iterable, Set

Symbol = str
Production = List[Symbol]         # e.g. ["S","a"] or ["b"] or ["e"]
GrammarMap = Dict[Symbol, List[Production]]

@dataclass
class Grammar:
    """Minimal grammar container."""
    start: Symbol = "S"
    prods: GrammarMap = field(default_factory=dict)
    order: List[Symbol] = field(default_factory=list)  # input LHS order

    @property
    def nonterminals(self) -> Set[Symbol]:
        return set(self.prods.keys())

    def add_nonterminal(self, A: Symbol, alts: Iterable[Production]) -> None:
        if A not in self.prods:
            self.prods[A] = []
            self.order.append(A)
        self.prods[A].extend(alts)

    def set_productions(self, A: Symbol, alts: Iterable[Production]) -> None:
        if A not in self.prods:
            self.order.append(A)
        self.prods[A] = list(alts)

    # ---------- naming helpers ----------
    def next_fresh_nonterminal(self) -> Symbol:
        """
        Choose an unused single capital letter, scanning Z..A (descending).
        This matches the expected outputs in the assignment (Z, then Y, ...).
        """
        used = set(self.prods.keys())
        for c in "ZYXWVUTSRQPONMLKJIHGFEDCBA":
            if c not in used:
                return c
        raise ValueError("Ran out of single-letter nonterminals (Z..A)")

    # ---------- pretty printing ----------
    @staticmethod
    def prod_to_str(p: Production) -> str:
        if p == ["e"]:
            return "e"
        return "".join(p)

    def to_lines(self) -> List[str]:
        seen: Set[Symbol] = set()
        ordered: List[Symbol] = []
        for A in self.order:
            if A in self.prods and A not in seen:
                seen.add(A)
                ordered.append(A)
        return [f"{A} -> " + " ".join(self.prod_to_str(p) for p in self.prods[A])
                for A in ordered]
