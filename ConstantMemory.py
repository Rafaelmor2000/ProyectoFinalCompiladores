import sys

from MemoryMap import CBOOL, CCHAR, CFLOAT, CINT, CLIM, CSTRING

BOOL = CBOOL
INT = CINT
FLOAT = CFLOAT
CHAR = CCHAR
STRING = CSTRING
LIM = CLIM


class ConstantMemory:
    def __init__(self) -> None:
        self.boolCount = 0
        self.boolList = []
        self.intCount = 0
        self.intList = []
        self.floatCount = 0
        self.floatList = []
        self.charCount = 0
        self.charList = []
        self.stringCount = 0
        self.stringList = []

    def malloc(self, var):
        varType = var.get("type")
        value = var.get("id")

        if varType == "bool":
            dir = BOOL
            dir += self.boolCount
            if dir < BOOL or dir >= INT:
                print("no memory available")
                sys.exit()
            else:
                self.boolCount += 1
                self.boolList.append(value)

        elif varType == "int":
            dir = INT
            dir += self.intCount
            if dir < INT or dir >= FLOAT:
                print("no memory available")
                sys.exit()
            else:
                self.intCount += 1
                self.intList.append(int(value))

        elif varType == "float":
            dir = FLOAT
            dir += self.floatCount
            if dir < FLOAT or dir >= CHAR:
                print("no memory available")
                sys.exit()

            else:
                self.floatCount += 1
                self.floatList.append(float(value))

        elif varType == "char":
            dir = CHAR
            dir += self.charCount
            if dir < CHAR or dir >= STRING:
                print("no memory available")
                sys.exit()

            else:
                self.charCount += 1
                self.charList.append(value)

        else:
            dir = STRING
            dir += self.stringCount
            if dir < STRING or dir >= LIM:
                print("no memory available")
                sys.exit()

            else:
                self.stringCount += 1
                self.stringList.append(value)

        return dir

    def getValue(self, dir):
        if dir < BOOL or dir >= LIM:
            print("Invalid direction for temp")
            sys.exit()

        elif dir < INT:
            return self.boolList[dir - BOOL]

        elif dir < FLOAT:
            return self.intList[dir - INT]

        elif dir < CHAR:
            return self.floatList[dir - FLOAT]

        elif dir < STRING:
            return self.charList[dir - CHAR]

        elif dir < LIM:
            return self.stringList[dir - STRING]
