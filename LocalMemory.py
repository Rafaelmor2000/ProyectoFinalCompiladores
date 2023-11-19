import sys


class LocalMemory:
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
            dir = 20000
            arrSize = int(var.get("arrSize"))
            dir += self.intCount + arrSize
            if dir < 20000 or dir >= 21000:
                print("no local memory for int variables available")
                sys.exit()
            else:
                if arrSize > 1:
                    self.intCount += arrSize
                    dir -= arrSize
                else:
                    self.intCount += 1

        elif varType == "float":
            dir = 21000
            arrSize = int(var.get("arrSize"))
            dir += self.floatCount + arrSize

            if dir < 21000 or dir >= 22000:
                print("no local memory for float variables available")
                sys.exit()

            else:
                if arrSize > 1:
                    self.floatCount += arrSize
                    dir -= arrSize
                else:
                    self.floatCount += 1

        else:
            dir = 22000
            arrSize = int(var.get("arrSize"))
            dir += self.charCount + arrSize
            if dir < 22000 or dir >= 23000:
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
