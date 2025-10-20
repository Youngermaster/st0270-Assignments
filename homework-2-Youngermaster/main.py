import argparse
import sys
from lre.io import parse_cases_from_lines
from lre.left_recursion import eliminate_left_recursion

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Eliminate left recursion (Aho et al., 2006 §4.3.3).")
    parser.add_argument(
        "input",
        nargs="?",
        help="path to input file; if omitted, read from stdin")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            raw = f.read().strip().splitlines()
    else:
        raw = sys.stdin.read().strip().splitlines()

    cases = parse_cases_from_lines(raw)

    outputs = []
    for G in cases:
        G2 = eliminate_left_recursion(G)
        outputs.append("\n".join(G2.to_lines()))

    print("\n\n".join(outputs))

if __name__ == "__main__":
    main()
