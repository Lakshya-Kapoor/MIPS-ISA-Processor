class Processor:
    pass
class instructionMemory(Processor):
    def __init__(self):
        # super().__init__()
        self.instMem = ['']*1000
        with open("factorial.txt", "r") as file:
            line = file.readlines()
            p = 0
            for i in line:
                i.replace('\n', '')
                for j in range(0, 32, 8):
                    self.instMem[p] = i[j:j+8]
                    p += 1
    def fetch(self, pc):
        s = ''
        for j in range(4):
           s += self.instMem[pc+j][:]
        return s
class dataMemory(Processor):
    def __init__(self):
        # super().__init__()
        self.dataMem = ['']*1000
    def memWrite(self, WD, A):
        A = int(A, 2)
        p = 0
        for i in range(4):
            self.dataMem[A+i] = WD[p:p+8]
            p += 8
    def memRead(self, A):
        A = int(A, 2)
        s = '' 
        for i in range(4):
            s += self.dataMem[A+i]
        return s
i = instructionMemory()
d = dataMemory()