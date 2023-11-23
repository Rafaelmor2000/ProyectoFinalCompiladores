import sys

from MemoryMap import CBOOL, CCHAR, CFLOAT, CINT, CLIM, CSTRING


# Module for management of memory assigned to constants
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

    # Assign and initialize memory for constants
    def malloc(self, var):
        varType = var.get("type")
        value = var.get("id")

        if varType == "bool":
            dir = CBOOL
            dir += self.boolCount
            if dir < CBOOL or dir >= CINT:
                print("no memory available")
                sys.exit()
            else:
                self.boolCount += 1
                self.boolList.append(value)

        elif varType == "int":
            dir = CINT
            dir += self.intCount
            if dir < CINT or dir >= CFLOAT:
                print("no memory available")
                sys.exit()
            else:
                self.intCount += 1
                self.intList.append(int(value))

        elif varType == "float":
            dir = CFLOAT
            dir += self.floatCount
            if dir < CFLOAT or dir >= CCHAR:
                print("no memory available")
                sys.exit()

            else:
                self.floatCount += 1
                self.floatList.append(float(value))

        elif varType == "char":
            dir = CCHAR
            dir += self.charCount
            if dir < CCHAR or dir >= CSTRING:
                print("no memory available")
                sys.exit()

            else:
                self.charCount += 1
                self.charList.append(value)

        else:
            dir = CSTRING
            dir += self.stringCount
            if dir < CSTRING or dir >= CLIM:
                print("no memory available")
                sys.exit()

            else:
                self.stringCount += 1
                self.stringList.append(value)

        return dir

    # return value stored in direction
    def getValue(self, dir):
        if dir < CBOOL or dir >= CLIM:
            print("Invalid direction for temp")
            sys.exit()

        elif dir < CINT:
            return self.boolList[dir - CBOOL]

        elif dir < CFLOAT:
            return self.intList[dir - CINT]

        elif dir < CCHAR:
            return self.floatList[dir - CFLOAT]

        elif dir < CSTRING:
            return self.charList[dir - CCHAR]

        elif dir < CLIM:
            return self.stringList[dir - CSTRING]
