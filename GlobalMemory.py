import sys

from MemoryMap import GLOBALCHAR, GLOBALFLOAT, GLOBALINT, GLOBALLIM


# Module designed for management of global memory
class GlobalMemory:
    def __init__(self) -> None:
        self.intCount = 0
        self.intList = []
        self.floatCount = 0
        self.floatList = []
        self.charCount = 0
        self.charList = []

    # Assign and initialize memory for global variables
    def malloc(self, var):
        varType = var.get("type")

        if varType == "int":
            dir = GLOBALINT
            arrSize = int(var.get("arrSize"))
            dir += self.intCount + arrSize
            if dir < GLOBALINT or dir >= GLOBALFLOAT:
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
            dir = GLOBALFLOAT
            arrSize = int(var.get("arrSize"))
            dir += self.floatCount + arrSize
            if dir < GLOBALFLOAT or dir >= GLOBALCHAR:
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
            dir = GLOBALCHAR
            arrSize = int(var.get("arrSize"))
            dir += self.charCount + arrSize
            if dir < GLOBALCHAR or dir >= GLOBALLIM:
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

    # Get value stored in direction
    def getValue(self, dir):
        if dir < GLOBALINT or dir >= GLOBALLIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < GLOBALFLOAT:
            return self.intList[dir - GLOBALINT]

        elif dir < GLOBALCHAR:
            return self.floatList[dir - GLOBALFLOAT]

        elif dir < GLOBALLIM:
            return self.charList[dir - GLOBALCHAR]

    # Save value to direction
    def saveValue(self, dir, value):
        if dir < GLOBALINT or dir >= GLOBALLIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < GLOBALFLOAT:
            self.intList[dir - GLOBALINT] = value

        elif dir < GLOBALCHAR:
            self.floatList[dir - GLOBALFLOAT] = value

        elif dir < GLOBALLIM:
            self.charList[dir - GLOBALCHAR] = value

    # Verify input is of appropriate type, save to direction
    def read(self, dir, value):
        if dir < GLOBALINT or dir >= GLOBALLIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < GLOBALFLOAT:
            try:
                value = int(value)
            except:
                print(f"Input value {value} is not of type int")
                sys.exit()
            self.intList[dir - GLOBALINT] = value

        elif dir < GLOBALCHAR:
            try:
                value = float(value)
            except:
                print(f"Input value {value} is not of type float")
                sys.exit()
            self.floatList[dir - GLOBALFLOAT] = value

        elif dir < GLOBALLIM:
            if len(value) > 1:
                print(f"Input value {value} is not of type char")
                sys.exit()
            else:
                self.charList[dir - GLOBALCHAR] = value
