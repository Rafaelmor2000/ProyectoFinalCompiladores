import sys

from MemoryMap import GLOBALCHAR, GLOBALFLOAT, GLOBALINT, GLOBALLIM

INT = GLOBALINT
FLOAT = GLOBALFLOAT
CHAR = GLOBALCHAR
LIM = GLOBALLIM


class GlobalMemory:
    def __init__(self) -> None:
        self.intCount = 0
        self.intList = []
        self.floatCount = 0
        self.floatList = []
        self.charCount = 0
        self.charList = []

    def malloc(self, var):
        varType = var.get("type")

        if varType == "int":
            dir = INT
            arrSize = int(var.get("arrSize"))
            dir += self.intCount + arrSize
            if dir < INT or dir >= FLOAT:
                print("no global memory for int variables available")
                sys.exit()
            else:
                if arrSize > 1:
                    self.intCount += arrSize
                    dir -= arrSize
                    for i in range(arrSize):
                        self.intList.append(0)
                else:
                    self.intCount += 1
                    self.intList.append(0)

        elif varType == "float":
            dir = FLOAT
            arrSize = int(var.get("arrSize"))
            dir += self.floatCount + arrSize
            if dir < FLOAT or dir >= CHAR:
                print("no global memory for float variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.floatCount += arrSize
                    dir -= arrSize
                    for i in range(arrSize):
                        self.floatList.append(0.0)
                else:
                    self.floatCount += 1
                    self.floatList.append(0.0)

        else:
            dir = CHAR
            arrSize = int(var.get("arrSize"))
            dir += self.charCount + arrSize
            if dir < CHAR or dir >= LIM:
                print("no global memory for char variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.charCount += arrSize
                    dir -= arrSize
                    for i in range(arrSize):
                        self.charList.append(" ")
                else:
                    self.charCount += 1
                    self.charList.append(" ")

        return dir

    def getValue(self, dir):
        if dir < INT or dir >= LIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < FLOAT:
            return self.intList[dir - INT]

        elif dir < CHAR:
            return self.floatList[dir - FLOAT]

        elif dir < LIM:
            return self.charList[dir - CHAR]

    def saveValue(self, dir, value):
        if dir < INT or dir >= LIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < FLOAT:
            self.intList[dir - INT] = value

        elif dir < CHAR:
            self.floatList[dir - FLOAT] = value

        elif dir < LIM:
            self.charList[dir - CHAR] = value

    def read(self, dir, value):
        if dir < INT or dir >= LIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < FLOAT:
            try:
                int(value)
            except:
                print(f"Input value {value} is not of type int")
                sys.exit()
            self.intList[dir - INT] = value

        elif dir < CHAR:
            try:
                float(value)
            except:
                print(f"Input value {value} is not of type float")
                sys.exit()
            self.floatList[dir - FLOAT] = value

        elif dir < LIM:
            if len(value) > 1:
                print(f"Input value {value} is not of type char")
            else:
                self.charList[dir - CHAR] = value
