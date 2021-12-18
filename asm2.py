from typing import List

def get_int(registers:dict, register:str):  # sourcery skip: default-get
    register = register.replace(',','')
    return registers[register] if register in registers else int(register)

def get_label(labels:dict, label:str):
    return labels[label] if label in labels else 0

def comment_label(program:List[str]):
    labels = {}
    i = 0
    while i < len(program):
        if program[i] == '':
            program.pop(i)
            continue
        # Replace multiple whitespaces with one
        program[i] = ' '.join(program[i].split())
        # Find and remove comment lines
        if program[i].startswith(';'):
            program.pop(i)
            continue
        # Find and remove inline comments
        if ';' in program[i]:
            program[i] = program[i].split(';')[0]
        # Find label lines and store them into labels dict
        if len(program[i].split(' ')) == 1 and program[i].endswith(':'):
            labels[program[i][:-1]] = i
        i += 1
    return (labels,program)

def simple_assembler(program:List[str]):
    registers = {}
    labels,program = comment_label(program)
    stack = []
    i = 0
    last_compare = 0
    message = ""
    while i < len(program):
        instruction, *operands = program[i].split(' ')
        if instruction == 'mov':
            register = operands[0].replace(',','')
            registers[register] = get_int(registers, operands[1]) #registers[operands[1]] if operands[1] in registers else int(operands[1])
        elif instruction == 'inc':
            registers[operands[0]] += 1
        elif instruction == 'dec':
            registers[operands[0]] -= 1
        elif instruction == 'add':
            register = operands[0].replace(',','')
            registers[register] += get_int(registers, operands[1])
        elif instruction == 'sub':
            register = operands[0].replace(',','')
            registers[register] -= get_int(registers, operands[1])
        elif instruction == 'mul':
            register = operands[0].replace(',','')
            registers[register] *= get_int(registers, operands[1])
        elif instruction == 'div':
            register = operands[0].replace(',','')
            registers[register] //= get_int(registers, operands[1])
        elif instruction == 'jmp':
            i += get_label(labels, operands[0]) - 1
        elif instruction == 'cmp':
            x = get_int(registers, operands[0])
            y = get_int(registers, operands[1])
            if x == y:
                last_compare = 0
            elif x<y:
                last_compare = -1
            else:
                last_compare = 1
        elif instruction == 'jne':
            if last_compare != 0:
                i += get_label(labels, operands[0]) - 1
        elif instruction == 'je':
            if last_compare == 0:
                i += get_label(labels, operands[0]) - 1
        elif instruction == 'jge':
            if last_compare >= 0:
                i += get_label(labels, operands[0]) - 1
        elif instruction == 'jg':
            if last_compare > 0:
                i += get_label(labels, operands[0]) - 1
        elif instruction == 'jle':
            if last_compare <= 0:
                i += get_label(labels, operands[0]) - 1
        elif instruction == 'jl':
            if last_compare < 0:
                i += get_label(labels, operands[0]) - 1
        elif instruction == 'call':
            stack.append(i + 1)
            i = get_label(labels, operands[0])
        elif instruction == 'ret':
            i = stack.pop() - 1
        elif instruction == 'msg':
            message = "".join(operands)
        elif instruction == 'end':
            if message:
                return message
            else:
                return register
        elif instruction == 'jnz' and get_int(registers, operands[0]): #(registers[operands[0]] if operands[0] in registers else int(operands[0])):
            i += int(operands[1])-1
        i += 1
    return -1

code = """
; My first program
mov  a, 5
inc  a
call function
msg  '(5+1)/2 = ', a    ; output message
end

function:
    div  a, 2
    ret
"""

print(simple_assembler(code.split('\n')))