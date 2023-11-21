import sys

from MemoryMap import CLIM, GLIM, GLOBALLIM, LLIM, LOCALLIM


class VirtualMachine:
    def __init__(self, fnTable, gMemory, lMemory, cMemory, tMemory) -> None:
        self.jumpStack = []
        self.funcStack = []
        self.params = []

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
            # print(quad)
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
                    print(self.getValue(quad.temp), end=" ")
                    # print(self.getValue(quad.temp))

                elif quad.operator == "VER":
                    min = 0
                    max = quad.temp
                    op1 = self.getValue(quad.operand1)
                    if op1 < min or op1 >= max:
                        print(f"Error: Array index {op1} out of range")
                        sys.exit()

                elif quad.operator == "ERA":
                    reqTemps = self.fnTable[quad.temp]["reqTemps"]
                    reqVars = self.fnTable[quad.temp]["reqVars"]

                    self.lMemory.era(reqVars)
                    self.tMemory.era(reqTemps)

                    self.funcStack.append(quad.temp)
                    keys = list(self.fnTable[self.funcStack[-1]]["vars"])
                    self.params = keys[: self.fnTable[self.funcStack[-1]]["params"]]

                elif quad.operator == "PARAM":
                    key = self.params[quad.temp]
                    arrSize = self.fnTable[self.funcStack[-1]]["vars"][key].get(
                        "arrSize"
                    )
                    dir = self.fnTable[self.funcStack[-1]]["vars"][key].get("dir")
                    if arrSize > 1:
                        for i in range(arrSize):
                            value = self.getParam(quad.operand1 + i)
                            self.saveValue(dir + i, value)
                    else:
                        value = self.getParam(quad.operand1)
                        self.saveValue(dir, value)

                elif quad.operator == "ENDFUNC":
                    reqTemps = self.fnTable[quad.temp]["reqTemps"]
                    reqVars = self.fnTable[quad.temp]["reqVars"]
                    # print(
                    #     self.lMemory.varOffsetMap,
                    #     reqVars,
                    # )

                    self.lMemory.pop(reqVars)
                    self.tMemory.pop(reqTemps)
                    curr = self.jumpStack.pop()
                    self.funcStack.pop()
                    if len(self.funcStack) > 0:
                        reqTemps = self.fnTable[self.funcStack[-1]]["reqTemps"]
                        reqVars = self.fnTable[self.funcStack[-1]]["reqVars"]
                        self.lMemory.revertOffset(reqVars)
                        self.tMemory.revertOffset(reqTemps)

                    self.params = []

                    # print(
                    #     self.lMemory.varOffsetMap,
                    #     reqVars,
                    # )
                elif quad.operator == "GOSUB":
                    self.jumpStack.append(curr)
                    curr = quad.temp - 1

            else:
                # execute simple operation
                op1 = self.getValue(quad.operand1)
                op2 = self.getValue(quad.operand2)
                res = self.do(quad.operator, op1, op2)
                self.saveValue(quad.temp, res)

            curr += 1

    # return value from appropriate memory direction
    def getValue(self, dir):
        dir = self.getPointer(dir)

        if dir < GLOBALLIM:
            value = self.gMemory.getValue(dir)
        elif dir < LOCALLIM:
            value = self.lMemory.getValue(dir)
        elif dir < CLIM:
            value = self.cMemory.getValue(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        elif dir < GLIM:
            value = self.tMemory.getValue(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        else:
            print(f"{dir} is an invalid memory direction")
            sys.exit()
        return value

    def getParam(self, dir):
        if dir < GLOBALLIM:
            value = self.gMemory.getValue(dir)
        elif dir < LOCALLIM:
            reqVars = self.fnTable[self.funcStack[-1]]["reqVars"]
            value = self.lMemory.getParam(dir, reqVars)

        elif dir < CLIM:
            value = self.cMemory.getValue(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False

        elif dir < LLIM:
            reqTemps = self.fnTable[self.funcStack[-1]]["reqTemps"]
            value = self.tMemory.getParam(dir, reqTemps)

            if value == "true":
                value = True
            elif value == "false":
                value = False

        elif dir < GLIM:
            value = self.tMemory.getValue(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        else:
            print(f"{dir} is an invalid memory direction")
            sys.exit()

        return value

    # save value to appropriate direction
    def saveValue(self, dir, value):
        dir = self.getPointer(dir)

        if dir < GLOBALLIM:
            self.gMemory.saveValue(dir, value)
        elif dir < LOCALLIM:
            self.lMemory.saveValue(dir, value)
        elif dir < CLIM:
            self.cMemory.saveValue(dir, value)
        elif dir < GLIM:
            self.tMemory.saveValue(dir, value)
        else:
            print(f"{dir} is an invalid memory direction")
            sys.exit()

    def getPointer(self, dir):
        if type(dir) == str:
            dir = int(dir[1:])
            dir = self.getValue(dir)
        return dir

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
