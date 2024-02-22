class Processor:
    def __init__(self):
        self.pc = 0
        self.RD1 = ''
        self.RD2 = ''
        self.alu1 = ''
        self.alu2 = ''
    def run(self):
        while True:

            # Instruction fetch phase
            self.instruction = i.fetch(self.pc)[::-1]
            self.pc += 4

            

            # Control signals
            arr = []
            for i in range(26,32):
                arr.append(int(self.instruction[i], 2)) 
            self.regDST = NOT(arr[3]) & NOT(arr[4]) & NOT(arr[5])
            self.regWR = (arr[0] & NOT(arr[1]) & NOT(arr[2])) | (NOT(arr[3]) & NOT(arr[4]) & NOT(arr[5]))
            self.aluSrc = arr[0] & NOT(arr[1])
            self.memRd = arr[0] & NOT(arr[1]) & NOT(arr[2])
            self.memReg = arr[0] & NOT(arr[1]) & NOT(arr[2])
            self.memWr = arr[0] & NOT(arr[1]) & arr[2]
            self.jmp = NOT(arr[0]) & NOT(arr[1]) & NOT(arr[2]) & NOT(arr[3]) & arr[4] & NOT(arr[5])
            self.branch = arr[3] & NOT(arr[4]) & NOT(arr[5])
            self.aluOp1 = NOT(arr[3]) & NOT(arr[4]) & NOT(arr[5])
            self.aluOp0 = arr[3] & NOT(arr[4]) & NOT(arr[5])
            
            # Instruction decode and reg read phase
            self.A1 = self.instruction[21:25+1]
            self.A2 = self.instruction[16:20+1]
            if self.regDST:
                self.A3 = self.instruction[11:15+1]
            else:
                self.A3 = self.instruction[16:20+1]
            
            r.regRead()
            
            temp = self.signExtend(self.instruction[0:15+1])



            # Execute phase
            self.alu1 = self.RD1
            if self.aluSrc:
                self.alu2 = temp
            else:
                self.alu2 = self.RD2
    def signExtend(self, s):
        return '0'*16 + s
class instructionMemory(Processor):
    def __init__(self):
        super().__init__()
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
        # pc = int(pc, 2)
        s = ''
        for j in range(4):
           s += self.instMem[pc+j]
        return s
class dataMemory(Processor):
    def __init__(self):
        super().__init__()
        self.dataMem = {}
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
class regFile(Processor):
    def __init__(self):
        super().__init__()
        self.zero = 0
        self.t = [0]*7
        self.s = [0]*7
    def regRead(self): # Requires the 5bit binary register numbers of A1 and A2 to read from.
        A1 = int(self.A1, 2)
        A2 = int(self.A2, 2)
        res = []
        if A1 == 0:
            self.RD1 = 0
        if A2 == 0:
            self.RD2 = 0
        if (A1 > 7 and A1 < 16):
            self.RD1 = self.t[A1%8]
        else:
            self.RD1 = self.s[A1%16]
        if (A2 > 7 and A2 < 16):
            self.RD2 = self.t[A2%8]
        else:
            self.RD2 = self.s[A2%16]
    def regWrite(self, WD3): # Requires the 5bit binary register number of A3 to write the data WD3
        A3 = int(self.A3, 2)
        if (A3 > 7 and A3 < 16):
            self.t[A3%8] = WD3
        else:
            self.s[A3%16] = WD3
class ALU(Processor):
    pass

if __name__ == '__main__':
    def NOT(num):
        return 0 if (num) else 1
    i = instructionMemory()
    d = dataMemory()
    r = regFile()
    p = Processor()