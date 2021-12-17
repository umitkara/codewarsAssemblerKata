from enum import Enum
from typing import List
    
# Enum for the different types of instructions
class InstructionType(Enum):
    MOV = mov = 1
    INC = inc = 2
    DEC = dec = 3
    JNZ = jnz = 4

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
registers = {}

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
            registers[instruction.operand1] = registers[instruction.operand2] if instruction.operand2.isalpha() else int(instruction.operand2)
        elif instruction.instructionType == InstructionType.JNZ:
            if instruction.operand1.isalpha() and registers[instruction.operand1] != 0:
                pc += int(instruction.operand2)
                continue
            elif instruction.operand1.isnumeric() and int(instruction.operand1) != 0:
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