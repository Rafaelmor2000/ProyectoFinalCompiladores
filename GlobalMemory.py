import sys


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
            dir = 10000
            arrSize = int(var.get("arrSize"))
            dir += self.intCount + arrSize
            if dir < 10000 or dir >= 11000:
                print("no memory available")
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
            dir = 11000
            arrSize = int(var.get("arrSize"))
            dir += self.floatCount + arrSize
            if dir < 11000 or dir >= 12000:
                print("no memory available")
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
            dir = 12000
            arrSize = int(var.get("arrSize"))
            dir += self.charCount + arrSize
            if dir < 12000 or dir >= 13000:
                print("no memory available")
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
