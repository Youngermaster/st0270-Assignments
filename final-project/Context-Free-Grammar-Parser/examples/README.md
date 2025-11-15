# Grammar Parser Examples

This directory contains example grammars to test the LL(1) and SLR(1) parsers.

## Example Files

### 1. `example1_slr1.txt` - SLR(1) Only Grammar
**Grammar**: Arithmetic expressions with left recursion
```
S -> S+T | T
T -> T*F | F
F -> (S) | i
```

**Why it's SLR(1) but not LL(1)**:
- Contains left recursion (S -> S+T and T -> T*F)
- LL(1) parsers cannot handle left recursion
- SLR(1) can handle it using bottom-up parsing

**Test strings**:
- `i+i` → yes (valid: identifier + identifier)
- `(i)` → yes (valid: parenthesized identifier)
- `(i+i)*i)` → no (invalid: extra closing parenthesis)

**Usage**:
```bash
python3 main.py < examples/example1_slr1.txt
```

---

### 2. `example2_both.txt` - Both LL(1) and SLR(1) Grammar
**Grammar**: Simple sequence grammar
```
S -> AB
A -> aA | d
B -> bBc | e
```

**Why it's both LL(1) and SLR(1)**:
- No left recursion
- No conflicts in parsing table
- FIRST and FOLLOW sets are disjoint
- Well-structured with clear alternatives

**Interactive Mode**:
- Choose `T` or `t` for LL(1) parser
- Choose `B` or `b` for SLR(1) parser
- Choose `Q` or `q` to quit

**Test strings** (using LL(1)):
- `d` → yes (A->d, B->e)
- `adbc` → yes (A->aA->ad, B->bBc->bc)
- `a` → no (incomplete)

**Usage**:
```bash
python3 main.py < examples/example2_both.txt
```

---

### 3. `example3_neither.txt` - Neither LL(1) nor SLR(1) Grammar
**Grammar**: Ambiguous grammar
```
S -> SS | a
```

**Why it's neither LL(1) nor SLR(1)**:
- **Ambiguous**: The string "aa" can be parsed as (S->a)(S->a) or S->SS where both S derive a
- **LL(1) conflict**: FIRST(SS) = {a} and FIRST(a) = {a}, so M[S,a] has multiple entries
- **SLR(1) conflict**: Shift/reduce conflict when seeing 'a' after reducing to S

This grammar demonstrates why ambiguous grammars cannot be parsed deterministically.

**Usage**:
```bash
python3 main.py < examples/example3_neither.txt
```

**Expected output**:
```
Grammar is neither LL(1) nor SLR(1).
```

---

### 4. `example4_both_palindrome.txt` - Both LL(1) and SLR(1) (Palindrome)
**Grammar**: Balanced strings (similar to palindromes)
```
S -> aSb | e
```

**Why it's both LL(1) and SLR(1)**:
- Clean structure with no recursion conflicts
- FIRST(aSb) = {a}, FIRST(e) uses FOLLOW
- No parsing conflicts in either method

**Test strings**:
- `aabb` → yes (valid: a(a(e)b)b)
- `ab` → yes (valid: a(e)b)
- `aaabbb` → yes (valid: a(a(a(e)b)b)b)
- `aab` → no (invalid: unbalanced)

**Usage**:
```bash
python3 main.py < examples/example4_both_palindrome.txt
```

---

### 5. `example4_balanced_parens.txt` - Both LL(1) and SLR(1) (Parentheses)
**Grammar**: Balanced parentheses
```
S -> (S)S | e
```

**Why it's both LL(1) and SLR(1)**:
- Classic example of balanced parentheses
- Well-structured recursive grammar
- No ambiguity or conflicts

**Test strings**:
- `(())` → yes (valid: nested parentheses)
- `()(())` → yes (valid: sequence of balanced pairs)
- `((()))` → yes (valid: deeply nested)
- `(()` → no (invalid: missing closing paren)
- `())(` → no (invalid: extra closing paren)

**Usage**:
```bash
python3 main.py < examples/example4_balanced_parens.txt
```

---

## Running All Examples

To test all examples at once:

```bash
for file in examples/example*.txt; do
    echo "=== Testing $file ==="
    python3 main.py < "$file"
    echo ""
done
```

## Summary Table

| Example | LL(1) | SLR(1) | Key Feature |
|---------|-------|--------|-------------|
| example1_slr1.txt | ✗ | ✓ | Left recursion |
| example2_both.txt | ✓ | ✓ | Simple clean grammar |
| example3_neither.txt | ✗ | ✗ | Ambiguous grammar |
| example4_both_palindrome.txt | ✓ | ✓ | Balanced strings |
| example4_balanced_parens.txt | ✓ | ✓ | Balanced parentheses |

## Grammar Notation

- `->` : Production rule
- `|` : Alternative (OR)
- `e` : Epsilon (empty string)
- Uppercase letters (A-Z): Non-terminals
- Lowercase letters, symbols: Terminals
