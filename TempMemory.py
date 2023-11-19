import sys

LBOOL = 40000
LINT = 40500
LFLOAT = 41000
LCHAR = 41500
LSTRING = 42000
LLIM = 42500

GBOOL = 50000
GINT = 50500
GFLOAT = 51000
GCHAR = 51500
GSTRING = 52000
GLIM = 52500


# Temp Memory Manager
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
                dir = LBOOL
                dir += self.lBoolCount
                if dir < LBOOL or dir >= LINT:
                    print("no local memory for bool temps available")
                    sys.exit()
                else:
                    self.lBoolCount += 1

            elif tempType == "int":
                dir = LINT
                dir += self.lIntCount
                if dir < LINT or dir >= LFLOAT:
                    print("no local memory for int temps available")
                    sys.exit()
                else:
                    self.lIntCount += 1

            elif tempType == "float":
                dir = LFLOAT
                dir += self.lFloatCount
                if dir < LFLOAT or dir >= LCHAR:
                    print("no local memory for float temps available")
                    sys.exit()

                else:
                    self.lFloatCount += 1

            elif tempType == "char":
                dir = LCHAR
                dir += self.lCharCount
                if dir < LCHAR or dir >= LSTRING:
                    print("no local memory for char temps available")
                    sys.exit()

                else:
                    self.lCharCount += 1

            else:
                dir = LSTRING
                dir += self.lStringCount
                if dir < LSTRING or dir >= LLIM:
                    print("no local memory for string temps available")
                    sys.exit()

                else:
                    self.lStringCount += 1

        # global temps
        else:
            if tempType == "bool":
                dir = GBOOL
                dir += self.gBoolCount
                if dir < GBOOL or dir >= GINT:
                    print("no global memory for bool temps available")
                    sys.exit()
                else:
                    self.gBoolCount += 1
                    self.gBoolList.append(True)

            elif tempType == "int":
                dir = GINT
                dir += self.gIntCount
                if dir < GINT or dir >= GFLOAT:
                    print("no global memory for int temps available")
                    sys.exit()
                else:
                    self.gIntCount += 1
                    self.gIntList.append(0)

            elif tempType == "float":
                dir = GFLOAT
                dir += self.gFloatCount
                if dir < GFLOAT or dir >= GCHAR:
                    print("no global memory for float temps available")
                    sys.exit()

                else:
                    self.gFloatCount += 1
                    self.gFloatList.append(0.0)

            elif tempType == "char":
                dir = GCHAR
                dir += self.gCharCount
                if dir < GCHAR or dir >= GSTRING:
                    print("no global memory for char temps available")
                    sys.exit()

                else:
                    self.gCharCount += 1
                    self.gCharList.append(" ")

            else:
                dir = GSTRING
                dir += self.gStringCount
                if dir < GSTRING or dir >= GLIM:
                    print("no global memory for string temps available")
                    sys.exit()

                else:
                    self.gStringCount += 1
                    self.gStringList.append(" ")
        return dir

    # Save required memory for local temps, and reset for next function
    def clear(self):
        reqMem = {
            "bool": self.lBoolCount,
            "int": self.lIntCount,
            "float": self.lFloatCount,
            "char": self.lCharCount,
            "string": self.lStringCount,
        }

        self.lBoolCount = 0
        self.lIntCount = 0
        self.lFloatCount = 0
        self.lCharCount = 0
        self.lStringCount = 0
        return reqMem

    # Assign space and initialize local temps
    def era(self, reqMem):
        bools = reqMem.get("bool")
        self.lBoolCount += bools
        ints = reqMem.get("int")
        self.lIntCount += ints
        floats = reqMem.get("float")
        self.lFloatCount += floats
        chars = reqMem.get("char")
        self.lCharCount += chars
        strings = reqMem.get("string")
        self.lStringCount += strings

        # evaluate if there is enough space available, initialize and make space for function.
        if self.lBoolCount >= LINT:
            print("no local memory for bool temps available")
            sys.exit()
        else:
            for i in range(bools):
                self.lBoolList.append(True)

        if self.lIntCount >= LFLOAT:
            print("no local memory for int temps available")
            sys.exit()
        else:
            for i in range(bools):
                self.lIntList.append(0)

        if self.lFloatCount >= LCHAR:
            print("no local memory for float temps available")
            sys.exit()
        else:
            for i in range(bools):
                self.lFloatList.append(0.0)

        if self.lCharCount >= LSTRING:
            print("no local memory for char temps available")
            sys.exit()
        else:
            for i in range(bools):
                self.lCharList.append(" ")

        if self.lStringCount >= LLIM:
            print("no local memory for string temps available")
            sys.exit()
        else:
            for i in range(bools):
                self.lStringList.append(" ")

    def getValue(self, dir):
        if dir < LLIM:
            if dir < LBOOL:
                print("Invalid direction for temp")
                sys.exit()

            elif dir < LINT:
                return self.lBoolList[dir - LBOOL]

            elif dir < LFLOAT:
                return self.lIntList[dir - LINT]

            elif dir < LCHAR:
                return self.lFloatList[dir - LFLOAT]

            elif dir < LSTRING:
                return self.lCharList[dir - LCHAR]

            elif dir < LLIM:
                return self.lStringList[dir - LSTRING]

        else:
            if dir < GBOOL or dir >= GLIM:
                print("Invalid direction for temp")
                sys.exit()

            elif dir < GINT:
                return self.gBoolList[dir - GBOOL]

            elif dir < GFLOAT:
                return self.gIntList[dir - GINT]

            elif dir < GCHAR:
                return self.gFloatList[dir - GFLOAT]

            elif dir < GSTRING:
                return self.gCharList[dir - GCHAR]

            elif dir < GLIM:
                return self.gStringList[dir - GSTRING]

    def saveValue(self, dir, value):
        if dir < LLIM:
            if dir < LBOOL:
                print("Invalid direction for temp")
                sys.exit()

            elif dir < LINT:
                self.lBoolList[dir - LBOOL] = value

            elif dir < LFLOAT:
                self.lIntList[dir - LINT] = value

            elif dir < LCHAR:
                self.lFloatList[dir - LFLOAT] = value

            elif dir < LSTRING:
                self.lCharList[dir - LCHAR] = value

            elif dir < LLIM:
                self.lStringList[dir - LSTRING] = value

        else:
            if dir < GBOOL or dir >= GLIM:
                print("Invalid direction for temp")
                sys.exit()

            elif dir < GINT:
                self.gBoolList[dir - GBOOL] = value

            elif dir < GFLOAT:
                self.gIntList[dir - GINT] = value

            elif dir < GCHAR:
                self.gFloatList[dir - GFLOAT] = value

            elif dir < GSTRING:
                self.gCharList[dir - GCHAR] = value

            elif dir < GLIM:
                self.gStringList[dir - GSTRING] = value
