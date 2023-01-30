import nltk
import numpy as np
from beautifultable import BeautifulTable
import tokenize
from keyword import iskeyword
import sys

try:
    action = sys.argv[1]
except:
    print(f"---------------\n{sys.argv[0]}\n---------------\n-t file_location")
    quit()

fileLocation = ""

try:
    assert action in ['-t', "-h", "--help"], 'Action is not known try -t: ' + action
except AssertionError as msg:
    print("AssertionError: ", msg)
    quit()

if action == "-t":
    fileLocation = sys.argv[2]
elif action == "-h" or action == "--help":
    print(f"---------------\n{sys.argv[0]}\n---------------\n-t file_location")
    quit()

res_words = ['while', 'do']


f = open(fileLocation, 'rb')

tokens = tokenize.tokenize(f.readline)
tokens_table = []
tokens_table_2 = []
for toknum, tokval, _, _, _ in tokens:
    if tokenize.tok_name[toknum] in ['OP', 'NAME', 'NUMBER']:
        if tokenize.tok_name[toknum] == 'NUMBER' or (tokenize.tok_name[toknum] == 'NAME' and tokval != 'do' and tokval != 'while') : # split all numbers for cfg
            tmp_str = str(tokval) 
            for i in tmp_str:
                tokens_table_2.append(i)
        else:
            tokens_table_2.append(tokval)
        tmp_lst = [tokenize.tok_name[toknum], tokval] # accepts type,data ie ['NAME', 'x']
        tokens_table.append(tmp_lst)

# replace type of reserved words from NAME to RESWORD  
for ls in tokens_table: 
    if ls[0] == 'NAME' and ls[1] in res_words:
        ls[0] = 'RESWORD'


# error if a var begins with a number or a number is present where it should not
for i in range(len(tokens_table)-1):
    if ((tokens_table[i][0] == 'NUMBER') and (tokens_table[i+1][0] == 'NAME')):
        print("error number present")
        exit()


print(tokens_table)
print(tokens_table_2)
 
f.close()



r = "\33[1;31m"
g = "\33[1;32m"
y = "\33[0;33m"
b = "\33[1;34m"

table = BeautifulTable(maxwidth=200,default_padding=3)
table.columns.header = [g+"Stack",g+"Buffer",g+"Action"]

def compare(a,b):
    if(not a or not b or len(a)<len(b)):
        return False
    return b==a[len(a)-len(b):]

def nonterminaltostr(a):
    b=[]
    for i in a:
        b.append(str(i))
    return b

def viewstack(x):
    y="$ "
    for i in x:
        y=y+str(i)+" "
    return y

def viewbuffer(x):
    y=""
    for i in x:
        y=y+str(i)+" "
    y=y+" $"
    return y

def printCFG2(g):
    print("\n\nCFG:\n")
    for i in g:
        print(i)

def printCFG():
        print("""\n\nCFG:\n
SS -> SS stat | SS assign | stat | assign
assign -> var '=' exp ';' |  var '=' var ';' |  var '=' num ';' 
stat -> 'do' '{' SS '}' 'while' cond ';'|'do' '{' '}' 'while' cond ';'
exp -> var op exp | num op exp | var op var | num op var | var op num | num op num
cond -> '(' num cop num ')' | '(' exp cop exp ')' | '(' var cop var ')' | '(' var cop num ')' | '(' num cop var ')' | '(' var cop exp ')' | '(' num cop exp ')' | '(' exp cop num ')' | '(' exp cop var ')'
op -> '+' | '-' | '*' | '/' | '%'
cop -> '==' | '!=' | '<' | '>' | '<=' | '>='
num -> num'0'|num'1'|num'2'|num'3'|num'4'|num'5'|num'6'|num'7'|num'8'|num'9'|'0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'
var -> var num|var'_'|var'a'|var'b'|var'c'|var'd'|var'e'|var'f'|var'g'|var'h'|var'i'|var'j'|var'k'|var'l'|var'm'|var'n'|var'o'|var'p'|var'q'|var'r'|var's'|var't'|var'u'|var'v'|var'w'|var'x'|var'y'|var'z'
var -> var'A'|var'B'|var'C'|var'D'|var'E'|var'F'|var'G'|var'H'|var'I'|var'J'|var'K'|var'L'|var'M'|var'N'|var'O'|var'P'|var'Q'|var'R'|var'S'|var'T'|var'U'|var'V'|var'W'|var'X'|var'Y'|var'Z'
var -> '_'|'a'|'A'|'b'|'B'|'c'|'C'|'d'|'D'|'e'|'E'|'f'|'F'|'g'|'G'|'h'|'H'|'i'|'I'|'j'|'J'|'k'|'K'|'l'|'L'|'m'|'M'|'n'|'N'|'o'|'O'|'p'|'P'|'q'|'Q'|'r'|'R'|'s'|'S'|'t'|'T'|'u'|'U'|'v'|'V'|'w'|'W'|'x'|'X'|'y'|'Y'|'z'|'Z'
""")

gram = nltk.CFG.fromstring("""
SS -> SS stat | SS assign | stat | assign
assign -> var '=' exp ';' |  var '=' var ';' |  var '=' num ';' 
stat -> 'do' '{' SS '}' 'while' cond ';'|'do' '{' '}' 'while' cond ';'
exp -> var op exp | num op exp | var op var | num op var | var op num | num op num
cond -> '(' num cop num ')' | '(' exp cop exp ')' | '(' var cop var ')' | '(' var cop num ')' | '(' num cop var ')' | '(' var cop exp ')' | '(' num cop exp ')' | '(' exp cop num ')' | '(' exp cop var ')'
op -> '+' | '-' | '*' | '/' | '%'
cop -> '==' | '!=' | '<' | '>' | '<=' | '>='
num -> num'0'|num'1'|num'2'|num'3'|num'4'|num'5'|num'6'|num'7'|num'8'|num'9'|'0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'
var -> var num|var'_'|var'a'|var'b'|var'c'|var'd'|var'e'|var'f'|var'g'|var'h'|var'i'|var'j'|var'k'|var'l'|var'm'|var'n'|var'o'|var'p'|var'q'|var'r'|var's'|var't'|var'u'|var'v'|var'w'|var'x'|var'y'|var'z'
var -> var'A'|var'B'|var'C'|var'D'|var'E'|var'F'|var'G'|var'H'|var'I'|var'J'|var'K'|var'L'|var'M'|var'N'|var'O'|var'P'|var'Q'|var'R'|var'S'|var'T'|var'U'|var'V'|var'W'|var'X'|var'Y'|var'Z'
var -> '_'|'a'|'A'|'b'|'B'|'c'|'C'|'d'|'D'|'e'|'E'|'f'|'F'|'g'|'G'|'h'|'H'|'i'|'I'|'j'|'J'|'k'|'K'|'l'|'L'|'m'|'M'|'n'|'N'|'o'|'O'|'p'|'P'|'q'|'Q'|'r'|'R'|'s'|'S'|'t'|'T'|'u'|'U'|'v'|'V'|'w'|'W'|'x'|'X'|'y'|'Y'|'z'|'Z'
""")
print (gram)

#buffer = ['x','=','0',';','x','_','t','1','y','=','1','9','0',';','do','{','do','{','}','while','(','x','<','y',')',';','y','=','y','-','1',';','x','=','x','+','1',';','}','while','(','x','<','y',')',';']
buffer =  tokens_table_2
stack = []
next = False

gp = gram.productions()
# for i in gp:
#     print(i.lhs())
#     print(i.rhs())
#     print('\n\n')
printCFG2(gp)
printCFG()
while(buffer):
    table.rows.append([viewstack(stack),viewbuffer(buffer),b+"Shift"])
    stack.append(buffer.pop(0))
    while(True):
        for i in gp:
            tmp = nonterminaltostr(np.asarray(i.rhs()))
            next = True
            if(compare(stack,tmp)):
                table.rows.append([viewstack(stack),viewbuffer(buffer),y+"Reduce "+str(i)])
                for j in tmp:
                    stack.pop()
                stack.append(str(i.lhs()))
                next = False
                break
        if(next):
            break

if (len(stack)==1):
    if (stack[0]==str(gram.start())):
        table.rows.append([y+viewstack(stack),y+viewbuffer(buffer),g+"Accept"])
        print(table)
else:
    table.rows.append([y+viewstack(stack),y+viewbuffer(buffer),r+"Reject"])
    print(table)
    #print(r+"Syntax Error\33[0m")
    exit()





def isOperator(C):
    return (C == '-' or C == '+' or C == '*' or C == '/' or C == '%' or C == '=' or C == '>' or C == '<' or C == '==' or C == '!=' or C == '<=' or C == '>=')
 
def getPriority(C):
    if (C == '-' or C == '+'):
        return 2
    elif (C == '*' or C == '/' or C == '%'):
        return 3
    elif (C == '=' or C == '>' or C == '<' or C == '==' or C == '!=' or C == '<=' or C == '>='):
        return 1
    return 0
 
def infixToPrefix(infix):
    operators = []
    operands = []
 
    for i in range(len(infix)):
        # If current character is an
        # opening bracket, then
        # push into the operators stack.
        if (infix[i] == '(' or infix[i] == '{'):
            operators.append(infix[i])
 
        # If current character is a
        # closing bracket, then pop from
        # both stacks and push result
        # in operands stack until
        # matching opening bracket is
        # not found.
        elif (infix[i] == ')' or infix[i] == '}'):
            while (len(operators)!=0 and (operators[-1] != '(' or operators[-1] != '}')):
                # operand 1
                op1 = operands[-1]
                if (len(operands)):
                    operands.pop()
 
                # operand 2
                op2 = operands[-1]
                if (len(operands)):
                    operands.pop()
 
                # operator
                op = operators[-1]
                if (len(operators)):
                    operators.pop()
 
                # Add operands and operator
                # in form operator +
                # operand1 + operand2.
                tmp = '(' + op + ' '  + op2 + ' '  + op1 + ')'
                operands.append(tmp)
 
            # Pop opening bracket
            # from stack.
            if (len(operators)):
                operators.pop()
 
        # If current character is an
        # operand then push it into
        # operands stack.
        elif (not isOperator(infix[i])):
            operands.append(infix[i] + "")
 
        # If current character is an
        # operator, then push it into
        # operators stack after popping
        # high priority operators from
        # operators stack and pushing
        # result in operands stack.
        else:
            while (len(operators)!=0 and getPriority(infix[i]) <= getPriority(operators[-1])):
                op1 = operands[-1]
                operands.pop()
 
                op2 = operands[-1]
                operands.pop()
 
                op = operators[-1]
                operators.pop()
 
                tmp = '(' + op + ' '  + op2 + ' ' + op1 + ')'
                operands.append(tmp)
            operators.append(infix[i])
 
    # Pop operators from operators
    # stack until it is empty and
    # operation in add result of
    # each pop operands stack.
    while (len(operators)!=0):
        op1 = operands[-1]
        operands.pop()
 
        op2 = operands[-1]
        operands.pop()
 
        op = operators[-1]
        operators.pop()
 
        tmp = '(' + op + ' '  + op2 + ' '  + op1 + ')'
        operands.append(tmp)
 
    # Final prefix expression is
    # present in operands stack.
    return operands[-1]

sin = []
subsin = []
body = '(body '
body2 = '(body '
cond = '(cond '
for i , j in tokens_table:
    sin.append(j)

while (sin):
    if (sin[0]=='do'):
        sin.pop(0)
        sin.pop(0)
        while (sin[0]!='}'):
            while (sin[0]!=';'):
                subsin.append(sin.pop(0))
            body2 = body2 + ' ' + infixToPrefix(subsin)
            subsin.clear()
            sin.pop(0)
        sin.pop(0)
        sin.pop(0)
        sin.pop(0)
        while (sin[0]!=')'):
            subsin.append(sin.pop(0))
        cond = cond + ' ' + infixToPrefix(subsin)
        subsin.clear()
        sin.pop(0)
        sin.pop(0)

    else:
        while (sin[0]!=';'):
            subsin.append(sin.pop(0))
        body = body + ' ' + infixToPrefix(subsin)
        subsin.clear()
        sin.pop(0)

body = body +')'
body2 = body2 +')'
cond = cond +')'

t=nltk.Tree.fromstring('(program '+body+'(doWhile '+body2+cond+'))')
print(t)
nltk.Tree.draw(t)
