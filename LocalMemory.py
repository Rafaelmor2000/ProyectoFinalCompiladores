import sys

from MemoryMap import LOCALCHAR, LOCALFLOAT, LOCALINT, LOCALLIM

INT = LOCALINT
FLOAT = LOCALFLOAT
CHAR = LOCALCHAR
LIM = LOCALLIM


class LocalMemory:
    def __init__(self) -> None:
        self.intCount = 0
        self.intList = []
        self.floatCount = 0
        self.floatList = []
        self.charCount = 0
        self.charList = []
        self.varOffsetMap = {"int": 0, "float": 0, "char": 0}

    def malloc(self, var):
        varType = var.get("type")

        if varType == "int":
            dir = INT
            arrSize = int(var.get("arrSize"))
            dir += self.intCount + arrSize
            if dir < INT or dir >= FLOAT:
                print("no local memory for int variables available")
                sys.exit()
            else:
                if arrSize > 1:
                    self.intCount += arrSize
                    dir -= arrSize
                else:
                    self.intCount += 1

        elif varType == "float":
            dir = FLOAT
            arrSize = int(var.get("arrSize"))
            dir += self.floatCount + arrSize

            if dir < FLOAT or dir >= CHAR:
                print("no local memory for float variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.floatCount += arrSize
                    dir -= arrSize
                else:
                    self.floatCount += 1

        else:
            dir = CHAR
            arrSize = int(var.get("arrSize"))
            dir += self.charCount + arrSize
            if dir < CHAR or dir >= LIM:
                print("no local memory for char variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.charCount += arrSize
                    dir -= arrSize
                else:
                    self.charCount += 1

        return dir

    def clear(self):
        reqMem = {
            "int": self.intCount,
            "float": self.floatCount,
            "char": self.charCount,
        }

        self.intCount = 0
        self.floatCount = 0
        self.charCount = 0

        return reqMem

    # Assign space and initialize local variables, save offset
    def era(self, reqMem):
        self.varOffsetMap = {
            "int": self.intCount,
            "float": self.floatCount,
            "char": self.charCount,
        }

        ints = reqMem.get("int")
        self.intCount += ints
        floats = reqMem.get("float")
        self.floatCount += floats
        chars = reqMem.get("char")
        self.charCount += chars

        # evaluate if there is enough space available, initialize and make space for function.
        if self.intCount >= FLOAT:
            print("no local memory for int variables available")
            sys.exit()
        else:
            for i in range(ints):
                self.intList.append(0)

        if self.floatCount >= CHAR:
            print("no local memory for float variables available")
            sys.exit()
        else:
            for i in range(floats):
                self.floatList.append(0.0)

        if self.charCount >= LIM:
            print("no local memory for char variables available")
            sys.exit()
        else:
            for i in range(chars):
                self.lCharList.append(" ")

    # release unrequired memory and revert offset to previous state
    def pop(self, reqMem):
        ints = reqMem.get("int")
        self.intCount -= ints
        floats = reqMem.get("float")
        self.floatCount -= floats
        chars = reqMem.get("char")
        self.charCount -= chars

        self.revertOffset(reqMem)

        if ints > 0:
            self.intList = self.intList[:-ints]
        if floats > 0:
            self.floatList = self.floatList[:-floats]
        if chars > 0:
            self.charListharList = self.charList[:-chars]

    def revertOffset(self, reqMem):
        ints = reqMem.get("int")
        floats = reqMem.get("float")
        chars = reqMem.get("char")

        self.varOffsetMap["int"] -= ints
        self.varOffsetMap["float"] -= floats
        self.varOffsetMap["char"] -= chars

    def getValue(self, dir):
        if dir < INT or dir >= LIM:
            print("Invalid direction for variable")
            sys.exit()
        elif dir < FLOAT:
            return self.intList[dir - INT + self.varOffsetMap["int"]]

        elif dir < CHAR:
            return self.floatList[dir - FLOAT + self.varOffsetMap["float"]]

        elif dir < LIM:
            return self.charList[dir - CHAR + self.varOffsetMap["char"]]

    def getParam(self, dir, reqMem):
        if dir < INT or dir >= LIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < FLOAT:
            return self.intList[dir - INT + self.varOffsetMap["int"] - reqMem["int"]]

        elif dir < CHAR:
            return self.floatList[
                dir - FLOAT + self.varOffsetMap["float"] - reqMem["float"]
            ]

        elif dir < LIM:
            return self.charList[
                dir - CHAR + self.varOffsetMap["char"] - reqMem["char"]
            ]

    def saveValue(self, dir, value):
        if dir < INT or dir >= LIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < FLOAT:
            self.intList[dir - INT + self.varOffsetMap["int"]] = value

        elif dir < CHAR:
            self.floatList[dir - FLOAT + self.varOffsetMap["float"]] = value

        elif dir < LIM:
            self.charList[dir - CHAR + self.varOffsetMap["char"]] = value
