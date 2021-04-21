'''
Akul Patel
Recursive Descent Parser: Phase 3
'''
'''
This program implements a recursive descent parser for the CFG below:

The grammar has added rule 0 to the previous program.
------------------------------------------------------------
0 <statement> → <id> = <exp>
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → | <func>
4 <func> → <func name>(<exp>)
5 <func name> → sin | cos | tan | exp | sqrt | abs

'''
"""
@author: rutkowsk
"""
import math

class ParseError(Exception): pass

#==============================================================
# FRONT END PARSER
#==============================================================

i = 0 # keeps track of what character we are currently reading.
err = None
symbol_table = {}

#---------------------------------------
#0
#Parse an Expression   <statement> → <id> = <exp>
#
def statement():
    global i, err
    while True:
        if w[i].isalpha():
            temp = w[i]
            i+=1
            if w[i] == '=':
                i += 1
                value = exp()
            else:
                print("missing '=' ")
        assign(temp, value)
        
        return value
    
#---------------------------------------   
#1
#Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value
#---------------------------------------
#2
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
#---------------------------------------
#3
# Parse a Factor    <factor> → (<exp>) | <number> | <func>
#       
def factor():
    global i, err
    value = None
    
    if w[i] == '(':
        i += 1
        value = exp()
        if w[i] == ')':
            i += 1
            return value
        else:
            print('missing )')
            raise ParserError
    elif (w[i] == 'sin' or w[i] == 'cos' or w[i] == 'tan' or w[i] == 'exp' or w[i] == 'sqrt' or w[i] == 'abs'):
        value = func()        
    elif w[i] == 'pi':
        i += 1
        return math.pi
    elif w[i] == '-':
        i += 1
        return -factor()
    
    else:
        try:
            value = atomic(w[i])
            i += 1          # read the next character
        except ValueError:
            print('number expected')
            value = None
    
    
    #print('factor returning', value)
    
    if value == None: raise ParseError
    return value
#---------------------------------------
#4
# <func> → <func name>(<exp>)
#
def func():
    global i, err

    #value = func_name()
    if w[i] == 'sin':
        i +=1
        if w[i] == '(':
            i += 1
            value = exp()
            math_func = func_name(value, 'sin')
            if w[i] == ')':
                i+= 1
                #print(math_func)
                return math_func
            else:
                print('missing )')
                raise ParseError
    elif w[i] == 'cos':
        i +=1
        if w[i] == '(':
            i += 1
            value = exp()
            math_func = func_name(value, 'cos')
            if w[i] == ')':
                i+= 1
                #print (math_func)
                return math_func
            else:
                print('missing )')
                raise ParseError
    elif w[i] == 'tan':
        i +=1
        if w[i] == '(':
            i += 1
            value = exp()
            math_func = func_name(value, 'tan')
            if w[i] == ')':
                i+= 1
                #print (math_func)
                return math_func
            else:
                print('missing )')
                raise ParseError
    elif w[i] == 'exp':
        i +=1
        if w[i] == '(':
            i += 1
            value = exp()
            math_func = func_name(value, 'exp')
            if w[i] == ')':
                i+= 1
                #print (math_func)
                return math_func
            else:
                print('missing )')
                raise ParseError
    elif w[i] == 'sqrt':
        i +=1
        if w[i] == '(':
            i += 1
            value = exp()
            math_func = func_name(value, 'sqrt')
            if w[i] == ')':
                i+= 1
                #print(math_func)
                return math_func
            else:
                print('missing )')
                raise ParseError
    elif w[i] == 'abs':
        i +=1
        if w[i] == '(':
            i += 1
            value = exp()
            math_func = func_name(value, 'abs')
            if w[i] == ')':
                i+= 1
                #print (math_func)
                return math_func
            else:
                print('missing )')
                raise ParseError
    if value == None: raise ParseError
    return value
#---------------------------------------
#5
# <func> → sin | cos | tan | exp | sqrt | abs
# 
def func_name(value,mathfun):
    global i, err

    #print(mathfun)

    if mathfun == 'sin':
        value = math.sin(value)
        return value
    elif mathfun == 'cos':
        value = math.cos(value)
        return value
    elif mathfun == 'tan':
        value = math.tan(value)
        return value
    elif mathfun == 'exp':
        value = math.exp(value)
        return value
    elif mathfun == 'sqrt':
        value = math.sqrt(value)
        return value
    elif mathfun == 'abs':
        value = abs(value)
        return value
    else:
        print('missing math function')
        value = None
        return value

#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================
def assign(iD, val):
    symbol_table[iD] = val
def binary_op(op, lhs, rhs):
    if op == '+': return lhs + rhs
    elif op == '-': return lhs - rhs
    elif op == '*': return lhs * rhs
    elif op == '/': return lhs // rhs
    else: return None

def atomic(token):
    try:
        return float(token)
    except:
        for x in symbol_table:
            if token == x:
                return symbol_table[token]
        print("float literal or variable expected")


#==============================================================
# User Interface Loop
#==============================================================
w = input('\nEnter statement: ')
while w != '':
    #------------------------------
    # Split string into token list.
    #
    for c in '=()+-*/':
        w = w.replace(c, ' '+c+' ')
    w = w.split()
    w.append('$') # EOF marker

    print('\nToken Stream:     ', end = '')
    for t in w: print(t, end = '  ')
    print('\n')
    i = 0
    try: 
        print('Value:           ', statement()) # call the parser
    except:
        print('parse error')
    print()
    if w[i] != '$': print('Syntax error:')
    print('read | un-read:   ', end = '')
    for c in w[:i]: print(c, end = '')
    print(' | ', end = '')
    for c in w[i:]: print(c, end = '')
    print()
    w = input('\n\nEnter statement: ')
#print(w[:i], '|', w[i:])



