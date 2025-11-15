#!/bin/bash

# Test script for all grammar examples

echo "========================================="
echo "Testing Grammar Parser Examples"
echo "========================================="
echo ""

# Example 1: SLR(1) only
echo "1. Testing example1_slr1.txt (SLR(1) only - Arithmetic)"
echo "   Expected: 'Grammar is SLR(1).'"
python3 main.py < examples/example1_slr1.txt
echo ""

# Example 2: Both parsers
echo "2. Testing example2_both.txt (Both LL(1) and SLR(1))"
echo "   Expected: Interactive mode (enters mode, tests with LL(1))"
timeout 2 python3 main.py < examples/example2_both.txt 2>&1 | head -10
echo ""

# Example 3: Neither parser
echo "3. Testing example3_neither.txt (Neither LL(1) nor SLR(1))"
echo "   Expected: 'Grammar is neither LL(1) nor SLR(1).'"
python3 main.py < examples/example3_neither.txt
echo ""

# Example 4 (palindrome): Both parsers
echo "4. Testing example4_both_palindrome.txt (Both - Palindromes)"
echo "   Expected: Interactive mode"
timeout 2 python3 main.py < examples/example4_both_palindrome.txt 2>&1 | head -10
echo ""

# Example 4 (balanced parens): Both parsers
echo "5. Testing example4_balanced_parens.txt (Both - Balanced Parentheses)"
echo "   Expected: Interactive mode"
timeout 2 python3 main.py < examples/example4_balanced_parens.txt 2>&1 | head -10
echo ""

echo "========================================="
echo "All tests completed!"
echo "========================================="
