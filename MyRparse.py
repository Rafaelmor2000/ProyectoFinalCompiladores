import sys

from genericpath import isfile

import MyRCube
import MyRlex
import ply.yacc as yacc
from ConstantMemory import *
from GlobalMemory import *
from LocalMemory import *
from Quad import Quad
from TempMemory import *
from VirtualMachine import *

tokens = MyRlex.tokens

# funcion para determinar precedencia y asociatividad de expresiones
precedence = (
    ("left", "AND", "OR"),
    ("nonassoc", "LTHAN", "GTHAN", "EQUALS", "DIFFERENCE", "LEQUAL", "GEQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
)

EMPTY = {"id": " "}

funcID = ""
programID = ""
currType = ""
paramCounter = 0
fnTable = {}
cnTable = {}
cube = MyRCube.MyRCube().CUBE
quadList = []
operandStack = []
tempCont = 0
jumpStack = []

# memory
gMemory = GlobalMemory()
lMemory = LocalMemory()
cMemory = ConstantMemory()
tMemory = TempMemory()


def p_program(p):
    "program : PROGRAM ID init SEMICOLON vars programp main"
    newQuad = Quad("DONE", EMPTY, EMPTY, " ")
    quadList.append(newQuad)


def p_init(p):
    "init :"
    global programID, funcID
    programID = p[-1]
    funcID = programID
    fnTable[programID] = {"type": "void", "vars": {}}
    newQuad = Quad("GOTO", EMPTY, EMPTY, EMPTY)
    quadList.append(newQuad)
    jumpStack.append(0)


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
    global paramCounter
    newQuad = Quad("ENDFUNC", EMPTY, EMPTY, p[3])
    quadList.append(newQuad)
    fnTable[funcID]["reqTemps"] = tMemory.clear()
    fnTable[funcID]["reqVars"] = lMemory.clear()


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
    "parameters : LPAREN parametersp RPAREN"
    global paramCounter, currType
    fnTable[funcID]["params"] = paramCounter

    while paramCounter > 0:
        temp = operandStack.pop(-paramCounter)
        currType = temp[1]
        checkVarOverlap(temp[0], temp[2])
        paramCounter = paramCounter - 1


def p_parametersp(p):
    """parametersp : type ID parameterArray parameterspp
    | empty"""
    if len(p) == 4:
        global paramCounter
        operandStack.append([p[2], p[1]])
        paramCounter += 1


def p_parameterArray(p):
    """parameterArray : LBRACKET CTE_I RBRACKET
    | empty"""
    global paramCounter
    if len(p) == 4:
        var = [p[-1], p[-2], p[2]]
    else:
        var = [p[-1], p[-2], 0]
    operandStack.append(var)
    paramCounter += 1


def p_parameterspp(p):
    """parameterspp : COMMA parametersp
    | empty"""


def p_main(p):
    "main : MAIN mainID LPAREN RPAREN statements"


def p_mainID(p):
    "mainID :"
    global funcID
    funcID = programID
    quadList[jumpStack.pop()].fill(len(quadList))


def p_statements(p):
    "statements : LBRACE statementsp RBRACE"


def p_statementsp(p):
    """statementsp : statementspp SEMICOLON statementsp
    | statementsppp statementsp
    | empty"""


def p_statementspp(p):
    """statementspp : assignment
    | voidCall
    | return
    | read
    | write"""


def p_voidCall(p):
    """voidCall : call
    | specCall"""
    if p[1] in fnTable:
        if fnTable[p[1]].get("type") != "void":
            print(f"Return from function is not being saved")
            sys.exit()
    elif p[1] != "reg" and p[1] != "plot":
        print(f"Return from function is not being saved")
        sys.exit()


def p_statementsppp(p):
    """statementsppp : condition
    | loop"""


def p_assignment(p):
    "assignment : variable EQUAL assignmentp"
    assignment()


def p_assignmentp(p):
    """assignmentp : expression
    | funcCall"""


def p_funcCall(p):
    """funcCall : call
    | specCall"""
    if p[1] in fnTable:
        if fnTable[p[1]].get("type") == "void":
            print(f"Cannot assign from void function")
            sys.exit()
    elif p[1] == "reg" or p[1] == "plot":
        print(f"Cannot assign from void function")
        sys.exit()


def p_call(p):
    "call : ID initParams LPAREN callp RPAREN"
    global paramCounter, tempCont
    id = p[1]
    p[0] = p[1]
    currType, dir, params = findFunc(id)
    if params != paramCounter:
        print(f"Wrong number of parameters in call to {id}")
        sys.exit()

    newQuad = Quad("ERA", EMPTY, EMPTY, id)
    quadList.append(newQuad)

    keys = list(fnTable[id]["vars"])
    while paramCounter > 0:
        parameter = operandStack.pop(-paramCounter)
        key = keys[params - paramCounter]
        if parameter.get("type") == fnTable[id]["vars"][key].get(
            "type"
        ) and parameter.get("arrSize") == fnTable[id]["vars"][key].get("arrSize"):
            newQuad = Quad("PARAM", parameter, EMPTY, params - paramCounter)

            quadList.append(newQuad)
            paramCounter -= 1
        else:
            print(
                f"Parameter types or arrSize in line {p.lineno(1)!r} do not match call to {id}"
            )
            sys.exit()

    newQuad = Quad("GOSUB", EMPTY, EMPTY, dir)
    quadList.append(newQuad)

    if currType != "void":
        genTemp(currType)
        temp = operandStack[-1]
        aux = fnTable[programID]["vars"][id]
        operandStack.append(
            {"id": id, "type": aux.get("type"), "dir": aux.get("dir"), "arrSize": 0}
        )
        assignment()
        operandStack.append(temp)


def p_specCall(p):
    "specCall : specCallp initParams LPAREN callp RPAREN"
    global paramCounter, tempCont
    id = p[1]
    p[0] = p[1]

    newQuad = Quad("ERA", EMPTY, EMPTY, id)
    quadList.append(newQuad)

    if id == "int":
        if paramCounter != 1:
            print(f"Wrong number of parameters in call to int")
            sys.exit()

        parameter = operandStack.pop()
        if parameter.get("type") != "float" or parameter.get("arrSize") != 0:
            print(
                f"Parameter types or arrSize in line {p.lineno!r} do not match call to {id}"
            )
            sys.exit()
        newQuad = Quad("PARAM", parameter, EMPTY, 0)
        quadList.append(newQuad)

        genTemp("int")

    elif id == "float":
        if paramCounter != 1:
            print(f"Wrong number of parameters in call to int")
            sys.exit()

        parameter = operandStack.pop()
        if parameter.get("type") != "int" or parameter.get("arrSize") != 0:
            print(
                f"Parameter types or arrSize in line {p.lineno!r} do not match call to {id}"
            )
            sys.exit()
        newQuad = Quad("PARAM", parameter, EMPTY, 0)
        quadList.append(newQuad)

        genTemp("float")

    elif id == "pow":
        if paramCounter != 2:
            print(f"Wrong number of parameters in call to int")
            sys.exit()

        for i in range(2):
            parameter = operandStack.pop(-2 + i)
            if (
                parameter.get("type") == "float"
                or parameter.get("type") == "int"
                and parameter.get("arrSize") == 0
            ):
                newQuad = Quad("PARAM", parameter, EMPTY, i)
                quadList.append(newQuad)

            else:
                print(
                    f"Parameter types or arrSize in line {p.lineno(1)!r} do not match call to {id}"
                )
                sys.exit()

        genTemp("float")

    elif id == "rand":
        if paramCounter != 0:
            print(f"Wrong number of parameters in call to {id}")
            sys.exit()

        genTemp("float")

    elif id == "plot" or id == "reg":
        if paramCounter != 1:
            print(f"Wrong number of parameters in call to {id}")
            sys.exit()

        parameter = operandStack.pop()
        if (
            parameter.get("type") == "float"
            or parameter.get("type") == "int"
            and parameter.get("arrSize") > 1
        ):
            newQuad = Quad("PARAM", parameter, EMPTY, 0)
            quadList.append(newQuad)

        else:
            print(
                f"Parameter types or arrSize in line {p.lineno(1)!r} do not match call to {id}"
            )
            sys.exit()

    else:
        if paramCounter != 1:
            print(f"Wrong number of parameters in call to {id}")
            sys.exit()

        parameter = operandStack.pop()
        if (
            parameter.get("type") != "int"
            or parameter.get("type") != "float"
            and parameter.get("arrSize") > 1
        ):
            newQuad = Quad("PARAM", parameter, EMPTY, 0)
            quadList.append(newQuad)
        else:
            print(f"Parameter types or arrSize do not match call to {id}")
            sys.exit()

        genTemp("float")

    newQuad = Quad("GOSUB", EMPTY, EMPTY, "spec")
    quadList.append(newQuad)


def p_specCallp(p):
    """specCallp : INT
    | FLOAT
    | POW
    | RAND
    | MED
    | MODA
    | VAR
    | REG
    | PLOT"""
    p[0] = p[1]


def p_callp(p):
    """callp : expression callpp
    | empty"""
    global paramCounter
    if len(p) == 3:
        paramCounter += 1


def p_callpp(p):
    """callpp : COMMA callp
    | empty"""


def p_return(p):
    "return : RETURN LPAREN expression RPAREN"
    aux = operandStack.pop()

    if programID == funcID:
        print(f"Cannot have return on function main")
        sys.exit()

    elif aux.get("type") == fnTable[funcID].get("type"):
        newQuad = Quad("RETURN", EMPTY, EMPTY, aux.get("dir"))
        quadList.append(newQuad)

    else:
        print(f"Type mismatch on return for function {funcID}")
        sys.exit()


# generate quads to read inputs
def p_read(p):
    "read : READ initParams LPAREN readp RPAREN"
    global operandStack, paramCounter
    while paramCounter > 0:
        temp = operandStack.pop(-paramCounter)
        newQuad = Quad("READ", EMPTY, EMPTY, temp.get("dir"))
        quadList.append(newQuad)
        paramCounter = paramCounter - 1


# count parameters in read
def p_readp(p):
    "readp : variable readpp"
    global paramCounter
    paramCounter = paramCounter + 1


def p_readpp(p):
    """readpp : COMMA readp
    | empty"""


# Create quads to print everything in call in the same line, then to print newline
def p_write(p):
    "write : WRITE initParams LPAREN writep RPAREN"
    global operandStack, paramCounter
    while paramCounter > 0:
        temp = operandStack.pop(-paramCounter)
        arrSize = temp.get("arrSize")
        if arrSize > 1:
            checkConstOverlap({"type": "string", "id": "[ "})
            newQuad = Quad("PRINT", EMPTY, EMPTY, operandStack.pop().get("dir"))
            quadList.append(newQuad)
            for i in range(arrSize):
                newQuad = Quad("PRINT", EMPTY, EMPTY, temp.get("dir") + i)
                quadList.append(newQuad)
                checkConstOverlap({"type": "string", "id": " "})
                newQuad = Quad("PRINT", EMPTY, EMPTY, operandStack.pop().get("dir"))
                quadList.append(newQuad)
            checkConstOverlap({"type": "string", "id": "]"})
            newQuad = Quad("PRINT", EMPTY, EMPTY, operandStack.pop().get("dir"))
            quadList.append(newQuad)
        else:
            newQuad = Quad("PRINT", EMPTY, EMPTY, temp.get("dir"))
            quadList.append(newQuad)
        paramCounter = paramCounter - 1
    checkConstOverlap({"type": "string", "id": "\n"})
    newQuad = Quad("PRINT", EMPTY, EMPTY, operandStack.pop().get("dir"))
    quadList.append(newQuad)


# initialize parameters
def p_initParams(p):
    "initParams :"
    global paramCounter
    paramCounter = 0


# count amount of parameters in write
def p_writep(p):
    """writep : expression writepp
    | CTE_S string writepp"""
    global paramCounter
    paramCounter = paramCounter + 1


def p_writepp(p):
    """writepp : COMMA writep
    | empty"""


def p_condition(p):
    "condition : IF LPAREN expression c1 THEN statements conditionp c3"


def p_conditionp(p):
    """conditionp : c2 ELSE statements
    | empty"""


# test expression is of bool type, add jump to stack
def p_c1(p):
    "c1 : RPAREN"
    jumpStack.append(len(quadList))
    aux = operandStack.pop()
    if aux.get("type") == "bool":
        newQuad = Quad("GOTOF", aux, EMPTY, EMPTY)
        quadList.append(newQuad)
    else:
        print(f"expression in line {p.lineno(1)!r} needs to result in boolean type")
        sys.exit()


# generate quad to skip to end of else, fill jump from stack
def p_c2(p):
    "c2 :"
    quadList[jumpStack.pop()].fill(len(quadList) + 1)
    newQuad = Quad("GOTO", EMPTY, EMPTY, EMPTY)

    jumpStack.append(len(quadList))
    quadList.append(newQuad)


# fill jump from stack
def p_c3(p):
    "c3 :"
    quadList[jumpStack.pop()].fill(len(quadList))


def p_loop(p):
    """loop : while
    | for"""


def p_while(p):
    "while : WHILE w1 LPAREN expression w2 DO statements w3"


# add jump to stack
def p_w1(p):
    "w1 :"
    jumpStack.append(len(quadList))


# test expression is of bool type and add jump to stack
def p_w2(p):
    "w2 : RPAREN"
    aux = operandStack.pop()
    if aux.get("type") == "bool":
        newQuad = Quad("GOTOF", aux, EMPTY, EMPTY)
        jumpStack.append(len(quadList))
        quadList.append(newQuad)
    else:
        print(f"expression in line {p.lineno(1)!r} needs to result in boolean type")
        sys.exit()


# generate quad to go back to beginning of while
def p_w3(p):
    "w3 :"
    aux = jumpStack.pop()
    newQuad = Quad("GOTO", EMPTY, EMPTY, jumpStack.pop())
    quadList.append(newQuad)
    quadList[aux].fill(len(quadList))


# create quads to sum 1 to variable and to go back to beginning of for
def p_for(p):
    "for : FOR ID EQUAL expression f1 expression f2 statements"
    var = operandStack.pop()
    aux = jumpStack.pop()
    checkConstOverlap({"type": "int", "id": 1})
    newQuad = Quad("+", var, operandStack.pop(), var.get("dir"))

    quadList.append(newQuad)
    newQuad = Quad("GOTO", EMPTY, EMPTY, jumpStack.pop())
    quadList.append(newQuad)
    quadList[aux].fill(len(quadList))


# test starting value is of int type and add jump to stack
def p_f1(p):
    "f1 : TO"
    aux = operandStack.pop()
    if aux.get("type") == "int":
        var = findIdType(p[-3])
        operandStack.append(aux)
        assignment()
        operandStack.append(var)
        operandStack.append(aux)
        jumpStack.append(len(quadList))
    else:
        print(
            f"first expression in line {p.lineno(1)!r} needs to result in integer type"
        )
        sys.exit()


# generate quads to test var is less or equal to limit and to go to end of for when false
def p_f2(p):
    "f2 : DO"
    global tempCont
    exp2 = operandStack.pop()
    exp1 = operandStack.pop()
    var = operandStack.pop()
    if exp2.get("type") == "int":
        operandStack.append(var)
        operandStack.append(exp2)
        genQuad("<=")
        jumpStack.append(len(quadList))
        newQuad = Quad("GOTOF", operandStack.pop(), EMPTY, " ")
        quadList.append(newQuad)
        operandStack.append(var)

    else:
        print(
            f"second expression in line {p.lineno(1)!r} needs to result in integer type"
        )
        sys.exit()


def p_expression(p):
    """expression : expression expressionp
    | factor"""
    p[0] = p[1]


def p_expressionp(p):
    """expressionp : AND expression
    | OR expression

    | LTHAN expression
    | GTHAN expression
    | EQUALS expression
    | DIFFERENCE expression
    | LEQUAL expression
    | GEQUAL expression

    | PLUS expression
    | MINUS expression

    | TIMES expression
    | DIVIDE expression
    | MOD expression"""
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


# load variable to operand stack
def p_variablep(p):
    """variablep : LBRACKET expression RBRACKET
    | empty"""
    findIdType(p[-1])
    if len(p) == 4:
        global quadList

        var = operandStack.pop()
        exp = operandStack.pop()
        if exp.get("type") != "int":
            print(
                f"Expression for array in line {p.lineno(1)!r} needs to result in integer type"
            )
            sys.exit()
        else:
            newQuad = Quad("VER", exp, EMPTY, var.get("arrSize"))
            quadList.append(newQuad)
            checkConstOverlap({"type": var.get("type"), "id": var.get("dir")})
            operandStack.append(exp)
            genQuad("+")
            temp = operandStack.pop()
            temp["dir"] = f"*{temp.get('dir')}"
            operandStack.append(temp)


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
    cn = {"id": p[-1], "arrSize": 0, "type": "bool"}
    checkConstOverlap(cn)


def p_char(p):
    "char :"
    global operandStack
    cn = {"id": p[-1], "arrSize": 0, "type": "char"}
    checkConstOverlap(cn)


def p_string(p):
    "string :"
    global operandStack
    string = p[-1]
    cn = {"id": string[1:-1], "arrSize": 0, "type": "string"}
    checkConstOverlap(cn)


def p_int(p):
    "int :"
    global operandStack
    cn = {"id": p[-1], "arrSize": 0, "type": "int"}
    checkConstOverlap(cn)


def p_float(p):
    "float :"
    global operandStack
    cn = {"id": p[-1], "arrSize": 0, "type": "float"}
    checkConstOverlap(cn)


def p_type(p):
    """type : INT
    | FLOAT
    | CHAR"""
    global currType
    currType = p[1]
    p[0] = p[1]


def p_empty(p):
    "empty :"
    p[0] = "void"
    pass


def p_error(p):
    if p is None:
        print(f"Missing \u007D at end of file")
    else:
        print(f"Syntax error at {p.value!r} in line {p.lineno!r}")
    sys.exit()


# generate quad to save last element of the operand stack into the second last
def assignment():
    temp = operandStack.pop()
    variable = operandStack.pop()
    arrSize = variable.get("arrSize")
    if temp.get("type") == variable.get("type"):
        if temp.get("arrSize") == arrSize:
            if arrSize < 2:
                newQuad = Quad("=", temp, EMPTY, variable.get("dir"))
                quadList.append(newQuad)
            else:
                for i in range(arrSize):
                    newQuad = Quad(
                        "=",
                        {"dir": temp.get("dir") + i},
                        EMPTY,
                        variable.get("dir") + i,
                    )
                    quadList.append(newQuad)
        else:
            print(
                f"Mismatched size of arrays caused by = on {temp.get('id')} and {variable.get('id')}"
            )
            sys.exit()
    else:
        print(f"Type mismatch caused by = on {temp.get('id')} and {variable.get('id')}")
        sys.exit()


# Verify if a variable has already been declared, if not, add to fnTable
def checkVarOverlap(id, arrSize):
    global fnTable
    overlap = False
    if id in fnTable[programID]["vars"]:
        overlap = True
    if funcID != programID:
        if id in fnTable[funcID]["vars"]:
            overlap = True

    if not overlap:
        var = {"type": currType, "arrSize": arrSize}
        if funcID == programID:
            dir = gMemory.malloc(var)
        else:
            dir = lMemory.malloc(var)
        var["dir"] = dir

        fnTable[funcID]["vars"][id] = var
    else:
        print(f"Variable name {id} has been declared elsewhere")
        sys.exit()


# verify id has been declared, append to operand stack and return type
def findIdType(id):
    global operandStack
    idType = "error"
    local = False
    if id in fnTable[programID]["vars"]:
        idType = fnTable[programID]["vars"][id].get("type")
        dir = fnTable[programID]["vars"][id].get("dir")
        arrSize = fnTable[programID]["vars"][id].get("arrSize")
    elif funcID != programID:
        if id in fnTable[funcID]["vars"]:
            idType = fnTable[funcID]["vars"][id].get("type")
            dir = fnTable[funcID]["vars"][id].get("dir")
            arrSize = fnTable[funcID]["vars"][id].get("arrSize")
            local = True

    if idType != "error":
        var = {"id": id, "arrSize": arrSize, "type": idType, "dir": dir}
        operandStack.append(var)
        if local:
            return fnTable[funcID]["vars"][id]
        else:
            return fnTable[programID]["vars"][id]

    else:
        print(f"Variable name {id} has not been declared")
        sys.exit()


# verify if function has been declared, if not, create variable to store returns and add to fnTable
def checkFuncOverlap():
    global fnTable, funcID
    if funcID in fnTable:
        print(f"Function name {funcID} has been declared elsewhere")
        sys.exit()
    else:
        fnTable[funcID] = {"type": currType, "dir": len(quadList), "vars": {}}
        if currType != "void":
            id = funcID
            funcID = programID
            checkVarOverlap(id, 0)
            funcID = id


# Verify function exists in fnTable, return function data
def findFunc(func):
    global funcID
    if func in fnTable:
        return (
            fnTable[func].get("type"),
            fnTable[func].get("dir"),
            fnTable[func].get("params"),
        )
    else:
        print(f"Function {func} has not been declared")
        sys.exit()


# append constand to operand stack, assign direction and add to cnTable if it does not exist yet
def checkConstOverlap(cn):
    global cnTable
    id = cn.get("id")
    if id not in cnTable:
        dir = cMemory.malloc(cn)
        cnTable[id] = {"type": cn.get("type"), "arrSize": 0, "dir": dir}
    else:
        dir = cnTable[id].get("dir")

    cn["dir"] = dir
    operandStack.append(cn)


# create quad for simple operations
def genQuad(operator):
    global operandStack, quadList, tempCont, currType
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    tempType = cube[operand1.get("type")][operand2.get("type")][operator]

    if tempType != "error":
        genTemp(tempType)
        newQuad = Quad(operator, operand1, operand2, operandStack[-1].get("dir"))
        quadList.append(newQuad)
    else:
        print(
            f"Type mismatch caused by {operator} on {operand1.get('id')} and {operand2.get('id')}"
        )
        sys.exit()


# generate new temp and add to operand stack
def genTemp(tempType):
    global tempCont
    temp = "temp" + str(tempCont)
    tempCont += 1
    isLocal = programID != funcID
    dir = tMemory.malloc(tempType, isLocal)
    operandStack.append({"id": temp, "type": tempType, "dir": dir, "arrSize": 0})


# Build the parser
parser = yacc.yacc()

# get input
if __name__ == "__main__":
    fileName = sys.argv[1]

    # Probar que exista archivo y abrirlo
    if isfile(fileName):
        inputFile = open(fileName, "r")
        inputCode = inputFile.read()
        inputFile.close()
        parser.parse(inputCode)
    else:
        print("File does not exist")
        sys.exit()

    # mostrar tabla de funciones
    for key in fnTable:
        print(f"{key}:")
        for element in fnTable[key]:
            print(f"{element}: {fnTable[key][element]}")
        print()

    # mostrar tabla de constantes
    # print(cnTable)

    # mostrar quads en lista
    cont = 0
    for quad in quadList:
        print(cont, str(quad))
        cont = cont + 1

    # inicializar y correr Maquina virtual
    vm = VirtualMachine(programID, fnTable, gMemory, lMemory, cMemory, tMemory)

    # show internal running data
    show = True
    vm.run(quadList, show)
