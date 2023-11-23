import sys

from MemoryMap import LOCALCHAR, LOCALFLOAT, LOCALINT, LOCALLIM


# Module designed for management of local variables
class LocalMemory:
    def __init__(self) -> None:
        self.intCount = 0
        self.intList = []
        self.floatCount = 0
        self.floatList = []
        self.charCount = 0
        self.charList = []
        self.varOffsetMap = {"int": 0, "float": 0, "char": 0}

    # Assign memory for local variables, save offset map
    def malloc(self, var):
        varType = var.get("type")

        if varType == "int":
            dir = LOCALINT
            arrSize = int(var.get("arrSize"))
            dir += self.intCount + arrSize
            if dir < LOCALINT or dir >= LOCALFLOAT:
                print("no local memory for int variables available")
                sys.exit()
            else:
                if arrSize > 1:
                    self.intCount += arrSize
                    dir -= arrSize
                else:
                    self.intCount += 1

        elif varType == "float":
            dir = LOCALFLOAT
            arrSize = int(var.get("arrSize"))
            dir += self.floatCount + arrSize

            if dir < LOCALFLOAT or dir >= LOCALCHAR:
                print("no local memory for float variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.floatCount += arrSize
                    dir -= arrSize
                else:
                    self.floatCount += 1

        else:
            dir = LOCALCHAR
            arrSize = int(var.get("arrSize"))
            dir += self.charCount + arrSize
            if dir < LOCALCHAR or dir >= LOCALLIM:
                print("no local memory for char variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.charCount += arrSize
                    dir -= arrSize
                else:
                    self.charCount += 1

        return dir

    # Save required memory for function, reset counters
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
        if self.intCount >= LOCALFLOAT:
            print("no local memory for int variables available")
            sys.exit()
        else:
            for i in range(ints):
                self.intList.append(0)

        if self.floatCount >= LOCALCHAR:
            print("no local memory for float variables available")
            sys.exit()
        else:
            for i in range(floats):
                self.floatList.append(0.0)

        if self.charCount >= LOCALLIM:
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

    # revert offset to previous state
    def revertOffset(self, reqMem):
        ints = reqMem.get("int")
        floats = reqMem.get("float")
        chars = reqMem.get("char")

        self.varOffsetMap["int"] -= ints
        if self.varOffsetMap["int"] < 0:
            self.varOffsetMap["int"] = 0
        self.varOffsetMap["float"] -= floats
        if self.varOffsetMap["float"] < 0:
            self.varOffsetMap["float"] = 0
        self.varOffsetMap["char"] -= chars
        if self.varOffsetMap["char"] < 0:
            self.varOffsetMap["char"] = 0

    # get value stored in a memory direction
    def getValue(self, dir):
        if dir < LOCALINT or dir >= LOCALLIM:
            print("Invalid direction for variable")
            sys.exit()
        elif dir < LOCALFLOAT:
            return self.intList[dir - LOCALINT + self.varOffsetMap["int"]]

        elif dir < LOCALCHAR:
            return self.floatList[dir - LOCALFLOAT + self.varOffsetMap["float"]]

        elif dir < LOCALLIM:
            return self.charList[dir - LOCALCHAR + self.varOffsetMap["char"]]

    # get param from a previous function
    def getParam(self, dir, reqMem):
        if dir < LOCALINT or dir >= LOCALLIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < LOCALFLOAT:
            return self.intList[
                dir - LOCALINT + self.varOffsetMap["int"] - reqMem["int"]
            ]

        elif dir < LOCALCHAR:
            return self.floatList[
                dir - LOCALFLOAT + self.varOffsetMap["float"] - reqMem["float"]
            ]

        elif dir < LOCALLIM:
            return self.charList[
                dir - LOCALCHAR + self.varOffsetMap["char"] - reqMem["char"]
            ]

    # save value to a memory direction
    def saveValue(self, dir, value):
        if dir < LOCALINT or dir >= LOCALLIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < LOCALFLOAT:
            self.intList[dir - LOCALINT + self.varOffsetMap["int"]] = value

        elif dir < LOCALCHAR:
            self.floatList[dir - LOCALFLOAT + self.varOffsetMap["float"]] = value

        elif dir < LOCALLIM:
            self.charList[dir - LOCALCHAR + self.varOffsetMap["char"]] = value

    # Verify input is of correct type, save to a memory direction
    def read(self, dir, value):
        if dir < LOCALINT or dir >= LOCALLIM:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < LOCALFLOAT:
            try:
                value = int(value)
            except:
                print(f"Input value {value} is not of type int")
                sys.exit()
            self.intList[dir - LOCALINT + self.varOffsetMap["int"]] = value

        elif dir < LOCALCHAR:
            try:
                value = float(value)
            except:
                print(f"Input value {value} is not of type float")
                sys.exit()
            self.floatList[dir - LOCALFLOAT + self.varOffsetMap["float"]] = value

        elif dir < LOCALLIM:
            if len(value) > 1:
                print(f"Input value {value} is not of type char")
                sys.exit()
            else:
                self.charList[dir - LOCALCHAR + self.varOffsetMap["char"]] = value
