class Processor:
    def __init__(self):
        self.pc = 0
        self.RD1 = ''
        self.RD2 = ''
        self.aluSrc1 = ''
        self.aluSrc2 = ''
        self.aluCtrl = ''
        self.aluRes = ''
    def run(self):
        while True:

            # Instruction fetch phase
            self.instruction = i.fetch()[::-1]
            self.pc += 4

            

            # Control signals
            opcode = []
            for i in range(31, 25, -1):
                opcode.append(int(self.instruction[i], 2)) 
            self.regDST = NOT(opcode[3]) & NOT(opcode[4]) & NOT(opcode[5])
            self.regWR = (opcode[0] & NOT(opcode[1]) & NOT(opcode[2])) | (NOT(opcode[3]) & NOT(opcode[4]) & NOT(opcode[5]))
            self.aluSrc = opcode[0] & NOT(opcode[1])
            self.memRd = opcode[0] & NOT(opcode[1]) & NOT(opcode[2])
            self.memReg = opcode[0] & NOT(opcode[1]) & NOT(opcode[2])
            self.memWr = opcode[0] & NOT(opcode[1]) & opcode[2]
            self.jmp = NOT(opcode[0]) & NOT(opcode[1]) & NOT(opcode[2]) & NOT(opcode[3]) & opcode[4] & NOT(opcode[5])
            self.branch = opcode[3] & NOT(opcode[4]) & NOT(opcode[5])
            self.aluOp1 = NOT(opcode[3]) & NOT(opcode[4]) & NOT(opcode[5])
            self.aluOp0 = opcode[3] & NOT(opcode[4]) & NOT(opcode[5])
            
            # Instruction decode and reg read phase
            self.A1 = self.instruction[21:25+1][::-1]
            self.A2 = self.instruction[16:20+1][::-1]
            if self.regDST:
                self.A3 = self.instruction[11:15+1][::-1]
            else:
                self.A3 = self.instruction[16:20+1][::-1]
            
            r.regRead()
            
            temp = self.signExtend(self.instruction[0:15+1][::-1])

            # ALU control unit
            if self.instruction[26:][::-1] == '001000' or self.instruction[26:][::-1] == '101011':
                self.aluCtrl = '000'
            elif self.instruction[26:][::-1] == '000100':
                self.aluCtrl = '001'
            elif self.instruction[26:][::-1] == '011100':
                self.aluCtrl = '010'
            elif self.instruction[26:][::-1] == '000000':
                self.aluCtrl = '011'
            elif self.instruction[26:][::-1] == '001100':
                self.aluCtrl = '100'    
                
            # Execute phase
            self.aluSrc1 = self.RD1
            if self.aluSrc:
                self.aluSrc2 = temp
            else:
                self.aluSrc2 = self.RD2
            a.execute()
    def signExtend(self, s):
        return '0'*(32-len(s)) + s
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
    def fetch(self):
        s = ''
        for j in range(4):
           s += self.instMem[self.pc+j]
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
            self.t[A3%8] = WD3 # WD3 is a binary string
        else:
            self.s[A3%16] = WD3
class ALU(Processor):
    def __init__(self):
        super().__init__()
    def execute(self):
        if self.aluCtrl == '000':
            temp = bin(int(self.aluSrc1, 2) + int(self.aluSrc2, 2))[2:]
            self.aluRes = self.signExtend(temp)
        elif self.aluCtrl == '001':
            temp = bin(int(self.aluSrc1, 2) - int(self.aluSrc2, 2))[2:]
            self.aluRes = self.signExtend(temp)
        elif self.aluCtrl == '010':
            temp = bin(int(self.aluSrc1, 2) * int(self.aluSrc2, 2))[2:]
            self.aluRes = self.signExtend(temp)
        elif self.aluCtrl == '011':
            temp = bin(int(self.aluSrc1, 2) >> int(self.aluSrc2, 2))[2:]
            self.aluRes = self.signExtend(temp)
        elif self.aluCtrl == '100':
            temp = bin(int(self.aluSrc1, 2) & int(self.aluSrc2, 2))[2:]
            self.aluRes = self.signExtend(temp)
if __name__ == '__main__':
    def NOT(num):
        return 0 if (num) else 1
    i = instructionMemory()
    d = dataMemory()
    r = regFile()
    a = ALU()
    p = Processor()