from typing import List

def simple_assembler(program:List[str]):
    registers = {}
    i = 0
    while i < len(program):
        instruction, *operands = program[i].split(' ')[:3]
        if instruction == 'mov':
            registers[operands[0]] = registers[operands[1]] if operands[1] in registers else int(operands[1])
        elif instruction == 'inc':
            registers[operands[0]] += 1
        elif instruction == 'dec':
            registers[operands[0]] -= 1
        elif instruction == 'jnz' and (registers[operands[0]] if operands[0] in registers else int(operands[0])):
            i += int(operands[1])-1
        i += 1
    return registers

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