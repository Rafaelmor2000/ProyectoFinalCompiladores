import sys


class TempMemory:
    def __init__(self) -> None:
        # global temps
        self.gBoolCount = 0
        self.gBoolList = []
        self.gIntCount = 0
        self.gIntList = []
        self.gFloatCount = 0
        self.gFloatList = []
        self.gCharCount = 0
        self.gCharList = []
        self.gStringCount = 0
        self.gStringList = []

        # local temps
        self.lBoolCount = 0
        self.lBoolList = []
        self.lIntCount = 0
        self.lIntList = []
        self.lFloatCount = 0
        self.lFloatList = []
        self.lCharCount = 0
        self.lCharList = []
        self.lStringCount = 0
        self.lStringList = []

    def malloc(self, tempType, isLocal):
        # local temps
        if isLocal:
            if tempType == "bool":
                dir = 40000
                dir += self.lBoolCount
                if dir < 40000 or dir >= 40500:
                    print("no memory available")
                    sys.exit()
                else:
                    self.lBoolCount += 1

            elif tempType == "int":
                dir = 40500
                dir += self.lIntCount
                if dir < 40500 or dir >= 41000:
                    print("no memory available")
                    sys.exit()
                else:
                    self.lIntCount += 1

            elif tempType == "float":
                dir = 41000
                dir += self.lFloatCount
                if dir < 41000 or dir >= 41500:
                    print("no memory available")
                    sys.exit()

                else:
                    self.lFloatCount += 1

            elif tempType == "char":
                dir = 41500
                dir += self.lCharCount
                if dir < 41500 or dir >= 42000:
                    print("no memory available")
                    sys.exit()

                else:
                    self.lCharCount += 1

            else:
                dir = 42000
                dir += self.lStringCount
                if dir < 42500 or dir >= 42500:
                    print("no memory available")
                    sys.exit()

                else:
                    self.lStringCount += 1

        # global temps
        else:
            if tempType == "bool":
                dir = 50000
                dir += self.gBoolCount
                if dir < 50000 or dir >= 50500:
                    print("no memory available")
                    sys.exit()
                else:
                    self.gBoolCount += 1
                    self.gBoolList.append(True)

            elif tempType == "int":
                dir = 50500
                dir += self.gIntCount
                if dir < 50500 or dir >= 51000:
                    print("no memory available")
                    sys.exit()
                else:
                    self.gIntCount += 1
                    self.gIntList.append(0)

            elif tempType == "float":
                dir = 51000
                dir += self.gFloatCount
                if dir < 51000 or dir >= 51500:
                    print("no memory available")
                    sys.exit()

                else:
                    self.gFloatCount += 1
                    self.gFloatList.append(0.0)

            elif tempType == "char":
                dir = 51500
                dir += self.gCharCount
                if dir < 51500 or dir >= 52000:
                    print("no memory available")
                    sys.exit()

                else:
                    self.gCharCount += 1
                    self.gCharList.append(" ")

            else:
                dir = 52000
                dir += self.gStringCount
                if dir < 52500 or dir >= 52500:
                    print("no memory available")
                    sys.exit()

                else:
                    self.gStringCount += 1
                    self.gStringList.append(" ")
        return dir

    def clear(self):
        self.lBoolCount = 0
        self.lIntCount = 0
        self.lFloatCount = 0
        self.lCharCount = 0
        self.lStringCount = 0
