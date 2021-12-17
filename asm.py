from enum import Enum
from typing import List

# Extended Dictionary class to reach dictionary elements by '.' notation
class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
# Enum for the different types of instructions
class InstructionType(Enum):
    MOV = 1
    mov = 1
    
    INC = 2
    inc = 2
    
    DEC = 3
    dec = 3
    
    JNZ = 4
    jnz = 4

# Node class for the assembly instructions
class instructionNode:
    def __init__(self, instructionType: InstructionType, **kwargs):
        # There are two kinds of instructions witch takes one or two operands
        # One operand instructions are: INC, DEC
        # Two operand instructions are: MOV, JNZ
        if instructionType in [InstructionType.INC, InstructionType.DEC]:
            self.instructionType = instructionType
            self.operand = kwargs['operand']
        else:
            self.instructionType = instructionType
            self.operand1 = kwargs['operand1']
            self.operand2 = kwargs['operand2']
            
    def __str__(self):
        if self.instructionType in [InstructionType.INC, InstructionType.DEC]:
            return str(self.instructionType.name) + " " + str(self.operand)
        else:
            return str(self.instructionType.name) + " " + str(self.operand1) + " " + str(self.operand2)

# Execution List
executionList:List[instructionNode] = []

# Register dictionary
registers = DotDict()

def assemblyParser(code_lines:List[str]):
    for line in code_lines:
        operands = line.split(' ')
        if len(operands) == 2:
            executionList.append(instructionNode(InstructionType[operands[0]], operand=operands[1]))
        elif len(operands) == 3:
            executionList.append(instructionNode(InstructionType[operands[0]], operand1=operands[1], operand2=operands[2]))
            
def executeInstructions():
    pc = 0
    while pc < len(executionList):
        instruction = executionList[pc]
        if instruction.instructionType == InstructionType.INC:
            registers[instruction.operand] += 1
        elif instruction.instructionType == InstructionType.DEC:
            registers[instruction.operand] -= 1
        elif instruction.instructionType == InstructionType.MOV:
            reg = instruction.operand1
            if reg not in registers:
                registers[reg] = 0
            src:str = instruction.operand2
            registers[instruction.operand1] = registers[src] if src.isalpha() else int(src)
        elif instruction.instructionType == InstructionType.JNZ:
            src = instruction.operand1
            if src.isalpha() and registers[src] != 0:
                pc += int(instruction.operand2)
                continue
            elif src.isnumeric() and int(src) != 0:
                pc += int(instruction.operand2)
                continue
        pc += 1

def simple_assembler(program):
    assemblyParser(program)
    executeInstructions()
    return registers
    
if __name__ == "__main__":
    code = '''\
mov c 12
mov b 0
mov a 200
dec a
inc b
jnz a -2
dec c
mov a b
jnz c -5
jnz 0 1
mov c a'''
    print(simple_assembler(code.split('\n')))