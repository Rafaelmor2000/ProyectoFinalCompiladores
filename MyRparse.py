import sys

import MyRCube
import MyRlex
import ply.yacc as yacc
from Quad import *

tokens = MyRlex.tokens

precedence = (
    ("left", "AND", "OR"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
)

funcID = ""
programID = ""
currType = ""
paramCounter = 0
fnTable = {}
cube = MyRCube.MyRCube().CUBE
quadList = []
operandStack = []
tempCont = 0


def p_program(p):
    "program : PROGRAM ID init SEMICOLON vars programp main"


def p_init(p):
    "init :"
    global programID, funcID
    programID = p[-1]
    funcID = programID
    fnTable[programID] = {"type": "void", "vars": {}}


def p_programp(p):
    """programp : function programp
    | empty"""


def p_vars(p):
    """vars : VARS varsp
    | empty"""


def p_varsp(p):
    """varsp : type varspp SEMICOLON varsp
    | empty"""


def p_varspp(p):
    """varspp : varsppp
    | varsppp COMMA varspp"""


def p_varsppp(p):
    "varsppp : ID varspppp"


def p_varspppp(p):
    """varspppp : LBRACKET CTE_I RBRACKET
    | empty"""
    varID = p[-1]
    arrSize = 0
    if len(p) == 4:
        arrSize = p[2]
    checkVarOverlap(varID, arrSize)


def p_function(p):
    """function : FUNCTION functionp ID funcID parameters vars statements
    | empty"""


def p_functionp(p):
    """functionp : type
    | VOID"""
    global currType
    if p[1] == "void":
        currType = p[1]


def p_funcID(p):
    "funcID :"
    global funcID
    funcID = p[-1]
    checkFuncOverlap()


def p_parameters(p):
    "parameters : LPAREN parametersp RPAREN linkParams"
    global paramCounter
    paramCounter = 0


def p_linkParams(p):
    "linkParams :"
    fnTable[funcID]["params"] = paramCounter


def p_parametersp(p):
    """parametersp : type ID parameterspp
    | empty"""
    if len(p) == 4:
        global paramCounter
        varID = p[2]
        paramCounter += 1
        checkVarOverlap(varID, 0)


def p_parameterspp(p):
    """parameterspp : COMMA parametersp
    | empty"""


def p_main(p):
    "main : MAIN mainID LPAREN RPAREN vars statements"


def p_mainID(p):
    "mainID :"
    global funcID, currType
    funcID = "main"
    currType = "void"
    fnTable[funcID] = {"type": currType, "vars": {}}


def p_statements(p):
    "statements : LBRACE statementsp RBRACE"


def p_statementsp(p):
    """statementsp : statementspp SEMICOLON statementsp
    | statementsppp statementsp
    | empty"""


def p_statementspp(p):
    """statementspp : assignment
    | call
    | return
    | read
    | write"""


def p_statementsppp(p):
    """statementsppp : condition
    | loop"""


def p_assignment(p):
    "assignment : variable EQUAL assignmentp"


def p_assignmentp(p):
    """assignmentp : expression
    | call"""


def p_call(p):
    "call : ID LPAREN callp RPAREN"


def p_callp(p):
    """callp : expression callpp
    | empty"""


def p_callpp(p):
    """callpp : COMMA callp
    | empty"""


def p_return(p):
    "return : RETURN LPAREN expression RPAREN"


def p_read(p):
    "read : READ LPAREN variable readp RPAREN"


def p_readp(p):
    """readp : COMMA variable readp
    | empty"""


def p_write(p):
    "write : WRITE LPAREN writep RPAREN"


def p_writep(p):
    """writep : expression writepp
    | CTE_S writepp"""


def p_writepp(p):
    """writepp : COMMA writep
    | empty"""


def p_condition(p):
    "condition : IF LPAREN expression RPAREN THEN statements conditionp"


def p_conditionp(p):
    """conditionp : ELSE statements
    | empty"""


def p_loop(p):
    """loop : while
    | for"""


def p_while(p):
    "while : WHILE LPAREN expression RPAREN DO statements"


def p_for(p):
    "for : FOR ID EQUAL expression TO expression DO statements"


def p_expression(p):
    "expression : bool_exp expressionp"


def p_expressionp(p):
    """expressionp : AND bool_exp
    | OR bool_exp
    | empty"""
    global quadList
    if len(p) == 3:
        genQuad(p[1])


def p_bool_exp(p):
    "bool_exp : arit_exp bool_expp"


def p_bool_expp(p):
    """bool_expp : LTHAN arit_exp
    | GTHAN arit_exp
    | EQUALS arit_exp
    | DIFFERENCE arit_exp
    | LEQUAL arit_exp
    | GEQUAL arit_exp
    | empty"""
    global quadList
    if len(p) == 3:
        genQuad(p[1])


def p_arit_exp(p):
    "arit_exp : term arit_expp"


def p_arit_expp(p):
    """arit_expp : PLUS arit_exp
    | MINUS arit_exp
    | empty"""
    global quadList
    if len(p) == 3:
        genQuad(p[1])


def p_term(p):
    "term : factor termp"


def p_termp(p):
    """termp : TIMES term
    | DIVIDE term
    | MOD term
    | empty"""
    global quadList
    if len(p) == 3:
        genQuad(p[1])


def p_factor(p):
    """factor : LPAREN expression RPAREN
    | var_cte
    | variable"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_variable(p):
    "variable : ID variablep"
    global operandStack

    varType = findIdType(p[1])
    if varType != "error":
        operandStack.append({"id": p[1], "type": varType})

    else:
        print(f"Variable name {p[1]} has not been declared")
        sys.exit()


def p_variablep(p):
    """variablep : LBRACKET expression RBRACKET
    | empty"""


def p_var_cte(p):
    """var_cte : TRUE bool
    | FALSE bool
    | CTE_C char
    | CTE_S string
    | CTE_I int
    | CTE_F float"""


def p_bool(p):
    "bool :"
    global operandStack
    operandStack.append({"id": p[-1], "type": "bool"})


def p_char(p):
    "char :"
    global operandStack
    operandStack.append({"id": p[-1], "type": "char"})


def p_string(p):
    "string :"
    global operandStack
    operandStack.append({"id": p[-1], "type": "string"})


def p_int(p):
    "int :"
    global operandStack
    operandStack.append({"id": p[-1], "type": "int"})


def p_float(p):
    "float :"
    global operandStack
    operandStack.append({"id": p[-1], "type": "float"})


def p_type(p):
    """type : INT
    | FLOAT
    | CHAR"""
    global currType
    currType = p[1]


def p_empty(p):
    "empty :"
    pass


def p_error(p):
    if p is None:
        print(f"Missing \u007D at end of file")
    else:
        print(f"Syntax error at {p.value!r} in line {p.lineno!r}")
    sys.exit()


def checkVarOverlap(id, arrSize):
    global fnTable
    overlap = False
    if id in fnTable[programID]["vars"]:
        overlap = True
    if funcID != programID:
        if id in fnTable[funcID]["vars"]:
            overlap = True
    if not overlap:
        fnTable[funcID]["vars"][id] = {
            "type": currType,
            "arrSize": arrSize,
            "dir": None,
        }
    else:
        print(f"Variable name {id} has been declared elsewhere")
        sys.exit()


def findIdType(id):
    idType = "error"
    if id in fnTable[programID]["vars"]:
        idType = fnTable[programID]["vars"][id].get("type")
    elif funcID != programID:
        if id in fnTable[funcID]["vars"]:
            idType = fnTable[funcID]["vars"][id].get("type")
    return idType


def checkFuncOverlap():
    global fnTable
    if funcID in fnTable:
        print(f"Function name {funcID} has been declared elsewhere")
        sys.exit()
    else:
        fnTable[funcID] = {"type": currType, "vars": {}}


def genQuad(operator):
    global operandStack, quadList, tempCont
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    tempType = cube[operand1.get("type")][operand2.get("type")][operator]

    if tempType != "error":
        temp = "temp" + str(tempCont)
        tempCont += 1
        operandStack.append({"id": temp, "type": tempType})
        newQuad = Quad(operator, operand1, operand2, temp)
        quadList.append(newQuad)
    else:
        print(f"Type mismatch caused by {operand1.get('id')} and {operand2.get('id')}")
        sys.exit()


# Build the parser
parser = yacc.yacc()

# temporary input
if __name__ == "__main__":
    fileName = sys.argv[1]

    inputFile = open(fileName, "r")
    inputCode = inputFile.read()
    inputFile.close()

    parser.parse(inputCode)
    print("All good!")

    # mostrar tabla de funciones
    for key in fnTable:
        print(f"{key} : {fnTable[key]}")

    # print(operandStack)

    # mostrar quads en lista
    for quad in quadList:
        print(str(quad))
