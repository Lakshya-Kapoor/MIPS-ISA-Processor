global instructionObj, DataObj, RegFileObj, AluObj, ProcessorObj
class Processor:
    def __init__(self):
        self.pc = '00000000010000000000000000000000'
        self.RD1 = ''
        self.RD2 = ''
        self.aluSrc1 = ''
        self.aluSrc2 = ''
        self.aluCtrl = ''
        self.aluRes = ''
    def run(self):
        while True:
            # Instruction fetch phase
            self.instruction = instructionObj.fetch()[::-1]
            if self.instruction == '':
                break
            self.pc = '0'*9 + bin(int(self.pc, 2) + 4)[2:] 
            
            # Control signals
            opcode = []
            for j in range(31, 25, -1):
                opcode.append(int(self.instruction[j], 2)) 
            self.regDST = NOT(opcode[3]) & NOT(opcode[4]) & NOT(opcode[5])
            self.regWR = (opcode[0] & NOT(opcode[1]) & NOT(opcode[2])) | (NOT(opcode[3]) & NOT(opcode[4]) & NOT(opcode[5]))
            self.aluSrc = opcode[0] & NOT(opcode[1])
            self.memRd = opcode[0] & NOT(opcode[1]) & NOT(opcode[2])
            self.memReg = opcode[0] & NOT(opcode[1]) & NOT(opcode[2])
            self.memWr = opcode[0] & NOT(opcode[1]) & opcode[2]
            self.jmp = NOT(opcode[0]) & NOT(opcode[1]) & NOT(opcode[2]) & NOT(opcode[3]) & opcode[4] & NOT(opcode[5])
            self.branch = opcode[3] & NOT(opcode[4]) & NOT(opcode[5])
            if self.instruction[26:][::-1] == "001000" or self.instruction[26:][::-1] == "001100": # for addi / andi
                self.regDST = 0
                self.regWR = 1
                self.aluSrc = 1
                self.memRd = 0
                self.memReg = 0
                self.memWr = 0
                self.branch = 0
                self.jmp = 0
            elif self.instruction[26:][::-1] == "011100": # for mul
                self.regDST = 1
                self.regWR = 1
                self.aluSrc = 0
                self.memRd = 0
                self.memReg = 0
                self.memWr = 0
                self.branch = 0
                self.jmp = 0
            # Instruction decode and reg read phase
            
            self.A1 = self.instruction[21:25+1][::-1]
            self.A2 = self.instruction[16:20+1][::-1]
            if self.regDST:
                self.A3 = self.instruction[11:15+1][::-1]
            else:
                self.A3 = self.instruction[16:20+1][::-1]
            
            if self.instruction[0:5+1][::-1] == '000010' and self.instruction[26:][::-1] == '000000':
                self.aluSrc = 2
                self.A1 = self.A2
            RegFileObj.regRead()
            

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
            temp = self.signExtend(self.instruction[0:15+1][::-1])
            self.aluSrc1 = self.RD1
            if self.aluSrc == 1:
                self.aluSrc2 = temp
            elif self.aluSrc == 2:
                self.aluSrc2 = self.instruction[6:10+1][::-1]
            else:
                self.aluSrc2 = self.RD2
            
            AluObj.execute()
            
            if self.jmp:
                self.pc = '0'*4 + self.instruction[:25+1][::-1] + '0'*2

            if self.branch and int(self.aluRes, 2) == 0:
                self.pc = '0'*9 + (bin(int(self.pc, 2) + (int(temp, 2) << 2)))[2:]
            # Memory access stage
            self.A = self.aluRes
            self.WD = self.RD2

            if self.memWr:
                DataObj.memWrite()
            else:
                self.RD = DataObj.memRead()
            
            if self.memReg:
                self.WD3 = self.RD
            else:
                self.WD3 = self.aluRes
            
            # Register writeback stage
            if self.regWR:
                RegFileObj.regWrite()
                
    def signExtend(self, s):
        return '0'*(32-len(s)) + s
class instructionMemory(Processor):
    def __init__(self):
        super().__init__()
        self.instMem = {}
        with open("pow.txt", "r") as file:
            line = file.readlines()
            l = '00000000010000000000000000000000'
            for k in line:
                k.replace('\n', '')
                for j in range(0, 32, 8):
                    self.instMem[l] = k[j:j+8]
                    l = '0'*9 + bin(int(l, 2) + 1)[2:]
            for k in range(4):
                self.instMem[l] = ''
                l = '0'*9 + bin(int(l, 2) + 1)[2:]
    def fetch(self):
        s = ''
        for j in range(4):
            s += self.instMem['0'*9 + bin(int(ProcessorObj.pc, 2)+j)[2:]]
        return s
class dataMemory(Processor):
    def __init__(self):
        super().__init__()
        self.dataMem = ['0']*1000
    def memWrite(self):
        A = int(ProcessorObj.A, 2)
        k = 0
        for j in range(4):
            self.dataMem[A+j] = ProcessorObj.WD[k:k+8]
            k += 8
    def memRead(self):
        A = int(ProcessorObj.A, 2)
        s = '' 
        for j in range(4):
            s += self.dataMem[A+j]
        return s
class regFile(Processor):
    def __init__(self):
        super().__init__()
        self.zero = 0
        self.t = ['0']*7
        self.s = ['0']*7
    def regRead(self):
        A1 = int(ProcessorObj.A1, 2)
        A2 = int(ProcessorObj.A2, 2)
        if A1 == 0:
            ProcessorObj.RD1 = '0'
        elif (A1 > 7 and A1 < 16):
            ProcessorObj.RD1 = self.t[A1%8]
        else:
            ProcessorObj.RD1 = self.s[A1%16]
        if A2 == 0:
            ProcessorObj.RD2 = '0'
        elif (A2 > 7 and A2 < 16):
            ProcessorObj.RD2 = self.t[A2%8]
        else:
            ProcessorObj.RD2 = self.s[A2%16]
    def regWrite(self):
        A3 = int(ProcessorObj.A3, 2)
        if (A3 > 7 and A3 < 16):
            self.t[A3%8] = ProcessorObj.WD3 # WD3 is AluObj binary string
        else:
            self.s[A3%16] = ProcessorObj.WD3
class ALU(Processor):
    def __init__(self):
        super().__init__()
    def execute(self):
        if ProcessorObj.aluCtrl == '000':
            temp = bin(int(ProcessorObj.aluSrc1, 2) + int(ProcessorObj.aluSrc2, 2))[2:]
            ProcessorObj.aluRes = ProcessorObj.signExtend(temp)
        elif ProcessorObj.aluCtrl == '001':
            temp = bin(int(ProcessorObj.aluSrc1, 2) - int(ProcessorObj.aluSrc2, 2))[2:]
            ProcessorObj.aluRes = ProcessorObj.signExtend(temp)
        elif ProcessorObj.aluCtrl == '010':
            temp = bin(int(ProcessorObj.aluSrc1, 2) * int(ProcessorObj.aluSrc2, 2))[2:]
            ProcessorObj.aluRes = ProcessorObj.signExtend(temp)
        elif ProcessorObj.aluCtrl == '011':
            temp = bin(int(ProcessorObj.aluSrc1, 2) >> int(ProcessorObj.aluSrc2, 2))[2:]
            ProcessorObj.aluRes = ProcessorObj.signExtend(temp)
        elif ProcessorObj.aluCtrl == '100':
            temp = bin(int(ProcessorObj.aluSrc1, 2) & int(ProcessorObj.aluSrc2, 2))[2:]
            ProcessorObj.aluRes = ProcessorObj.signExtend(temp)
if __name__ == '__main__':
    def NOT(num):
        return 0 if (num) else 1
    instructionObj = instructionMemory()
    DataObj = dataMemory()
    RegFileObj = regFile()
    AluObj = ALU()
    ProcessorObj = Processor()
    ProcessorObj.run()
    print(int(DataObj.dataMem[256]+DataObj.dataMem[257]+DataObj.dataMem[258]+DataObj.dataMem[259], 2))