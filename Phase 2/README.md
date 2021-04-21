# Recursive Descent Parser: Phase 2
------------------------------------------------------------
This program implements a recursive descent parser for the CFG below:
The grammar has added rule 3, 4, and 5 to the previous program.

1 `<exp> → <term>{+<term> | -<term>}`
2 `<term> → <factor>{*<factor> | /<factor>}`
3 `<factor> → | <func>`
4 `<func> → <func name>(<exp>)`
5 `<func name> → sin | cos | tan | exp | sqrt | abs`
