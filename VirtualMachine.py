import sys

GLIM = 13000
LLIM = 23000
CLIM = 32500
TLIM = 52500


class VirtualMachine:
    def __init__(self, fnTable, gMemory, lMemory, cMemory, tMemory) -> None:
        self.varOffsetMap = {"int": 0, "float": 0, "char": 0}
        self.tempOffsetMap = {"bool": 0, "int": 0, "float": 0, "char": 0, "string": 0}
        self.jumpStack = []

        self.fnTable = fnTable
        self.gMemory = gMemory
        self.lMemory = lMemory
        self.cMemory = cMemory
        self.tMemory = tMemory

    # execute quads from quadlist
    def run(self, quadList):
        curr = 0
        while quadList[curr].operator != "DONE":
            quad = quadList[curr]
            if quad.operand2 == None:
                # execute more complex operations
                if quad.operator == "=":
                    op1 = self.getValue(quad.operand1)
                    self.saveValue(quad.temp, op1)

                elif quad.operator == "GOTO":
                    curr = quad.temp - 1

                elif quad.operator == "GOTOF":
                    op1 = self.getValue(quad.operand1)
                    if not op1:
                        curr = quad.temp - 1

                elif quad.operator == "PRINT":
                    print(self.getValue(quad.temp))

                elif quad.operator == "VER":
                    min = 0
                    max = quad.temp
                    op1 = self.getValue(quad.operand1)
                    if op1 < min or op1 >= max:
                        print(f"Error: Array index out of range")

            else:
                op1 = self.getValue(quad.operand1)
                op2 = self.getValue(quad.operand2)
                res = self.do(quad.operator, op1, op2)
                self.saveValue(quad.temp, res)

            print(quad)
            curr += 1

    # return value from appropriate memory direction
    def getValue(self, dir):
        if type(dir) == str:
            dir = int(dir[1:])
            dir = self.getValue(dir)

        if dir < GLIM:
            value = self.gMemory.getValue(dir)
        elif dir < LLIM:
            value = self.lMemory.getValue(dir)
        elif dir < CLIM:
            value = self.cMemory.getValue(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        elif dir < TLIM:
            value = self.tMemory.getValue(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        else:
            print("Invalid memory direction")
        return value

    # save value to appropriate direction
    def saveValue(self, dir, value):
        if type(dir) == str:
            dir = int(dir[1:])
            dir = self.getValue(dir)

        if dir < GLIM:
            self.gMemory.saveValue(dir, value)
        elif dir < LLIM:
            self.lMemory.saveValue(dir, value)
        elif dir < CLIM:
            self.cMemory.saveValue(dir, value)
        elif dir < TLIM:
            self.tMemory.saveValue(dir, value)
        else:
            print("Invalid memory direction")

    # execute simple expressions
    def do(self, operator, op1, op2):
        if operator == "+":
            res = op1 + op2
        elif operator == "-":
            res = op1 - op2

        elif operator == "*":
            res = op1 * op2
        elif operator == "/":
            if op2 == 0:
                print("Error: cannot divide by 0")
                sys.exit()
            else:
                res = op1 / op2
        elif operator == "%":
            res = op1 % op2

        elif operator == ">":
            res = op1 > op2
        elif operator == "<":
            res = op1 < op2
        elif operator == ">=":
            res = op1 >= op2
        elif operator == "<=":
            res = op1 <= op2
        elif operator == "<>":
            res = op1 != op2
        elif operator == "==":
            res = op1 == op2

        elif operator == "&":
            res = op1 and op2
        elif operator == "|":
            res = op1 or op2

        else:
            print(f"Error: unrecognized operator {operator}")
            sys.exit()

        return res
