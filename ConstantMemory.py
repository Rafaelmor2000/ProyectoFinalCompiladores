import sys


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
            dir = 30000
            dir += self.boolCount
            if dir < 30000 or dir >= 30002:
                print("no memory available")
                sys.exit()
            else:
                self.boolCount += 1
                self.boolList.append(value)

        elif varType == "int":
            dir = 30002
            dir += self.intCount
            if dir < 30002 or dir >= 30500:
                print("no memory available")
                sys.exit()
            else:
                self.intCount += 1
                self.intList.append(int(value))

        elif varType == "float":
            dir = 30500
            dir += self.floatCount
            if dir < 30500 or dir >= 31000:
                print("no memory available")
                sys.exit()

            else:
                self.floatCount += 1
                self.floatList.append(float(value))

        elif varType == "char":
            dir = 31000
            dir += self.charCount
            if dir < 31000 or dir >= 31500:
                print("no memory available")
                sys.exit()

            else:
                self.charCount += 1
                self.charList.append(value)

        else:
            dir = 31500
            dir += self.stringCount
            if dir < 31500 or dir >= 32000:
                print("no memory available")
                sys.exit()

            else:
                self.stringCount += 1
                self.stringList.append(value)

        return dir
