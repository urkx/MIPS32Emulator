import numpy as np
import sys

'''
 REGISTERS
-----------
0  - zero -> Always equal to zero
1  - at   -> Assembler temporary

2  - v0 |
3  - v1 | -> Return value from a function call 

4  - a0 |
5  - a1 | -> First four parameters for a function call
6  - a2 |
7  - a4 |

8  - t0 |
9  - t1 |
10 - t2 |
11 - t3 | -> Temporary variables
12 - t4 |
13 - t5 |
14 - t6 |
15 - t7 |

16 - s0 |
17 - s1 |
18 - s2 |
19 - s3 |
20 - s4 | -> Function variables
21 - s5 |
22 - s6 |
23 - s7 |

24 - t8 |
25 - t9 | -> Temporary variables

26 - k0 |
27 - k1 | -> Kernel use registers

28 - gp   -> Global pointer
29 - sp   -> Stack pointer
30 - fp/s8 -> Stack frame pointer or subrutine variable
31 - ra -> Return address

'''
REGS = np.zeros(32)

REGS_DICT = {
    'zero': 0,
    'at': 1,
    'v0': 2,
    'v1': 3,
    'a0': 4,
    'a1': 5,
    'a2': 6,
    'a3': 7,
    't0': 8,
    't1': 9,
    't2': 10,
    't3': 11,
    't4': 12,
    't5': 13,
    't6': 14,
    't7': 15,
    's0': 16,
    's1': 17,
    's2': 18,
    's3': 19,
    's4': 20,
    's5': 21,
    's6': 22,
    's7': 23,
    't8': 24,
    't9': 25,
    'k0': 26,
    'k1': 27,
    'gp': 28,
    'sp': 29,
    'fp/s8': 30,
    'ra': 31
}

# Program counter 
PC = 0

# Instructions memory
IM = [] 

def decRegs(inst):
    code = inst[0]
    params = []
    for i in range(1, len(inst)):
        reg = inst[i].replace('$','').replace(',','')
        params.append(reg)
    return code, params

def ex(inst):
    global PC
    code, params = decRegs(inst)
    if code[-1] == ':':
        REGS[REGS_DICT['ra']] = PC
    elif code == 'add' or code == 'addu':
        # TODO: overflow and signed/unsigned
        REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]] + REGS[REGS_DICT[params[2]]]
    elif code == 'addi' or code == 'addiu': 
        REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]] + int(params[2])
    elif code == 'clo':
        aux = "{:032b}".format(int(REGS[REGS_DICT[params[1]]]))
        count = 0
        for x in aux:
            if x == '1':
                count += 1
        REGS[REGS_DICT[params[0]]] = count
    elif code == 'clz':
        aux = "{:032b}".format(int(REGS[REGS_DICT[params[1]]]))
        count = 0
        for x in aux:
            if x == '0':
                count += 1
        REGS[REGS_DICT[params[0]]] = count
    elif code == 'la':
        # TODO: how tf can I implement addresses
        pass
    elif code == 'li':
        REGS[REGS_DICT[params[0]]] = int(params[1])
    elif code == 'lui':
        REGS[REGS_DICT[params[0]]] = int(params[1]) << 16
    elif code == 'move':
        REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]]
    elif code == 'negu':
        REGS[REGS_DICT[params[0]]] = int(REGS[REGS_DICT[params[1]]]) * -1
    elif code == 'seb':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'seh':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'sub' or code == 'subu':
        # TODO: overflow and signed/unsigned
        REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]] - REGS[REGS_DICT[params[2]]]
    elif code == 'rotr':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'rotrv':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'sll':
        REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]] << int(params[2])
    elif code == 'sllv':
        aux = "{:032b}".format(int(REGS[REGS_DICT[params[2]]]))
        shift = int(aux[len(aux)-5:len(aux)], 2)
        REGS[REGS_DICT[params[0]]] = int(REGS[REGS_DICT[params[1]]]) << shift
    elif code == 'sra' or code == 'srl':
        # TODO: signed/unsigned
        REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]] >> int(params[2])
    elif code == 'srav' or code == 'srlv':
        # TODO: signed/unsigned
        aux = "{:032b}".format(int(REGS[REGS_DICT[params[2]]]))
        shift = int(aux[len(aux)-5:len(aux)], 2)
        REGS[REGS_DICT[params[0]]] = int(REGS[REGS_DICT[params[1]]]) >> shift
    elif code == 'and':
        REGS[REGS_DICT[params[0]]] = int(REGS[REGS_DICT[params[1]]]) & int(REGS[REGS_DICT[params[2]]])
    elif code == 'andi':
        REGS[REGS_DICT[params[0]]] = int(REGS[REGS_DICT[params[1]]]) & int(params[2])
    elif code == 'ext':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'ins':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'nor':
        REGS[REGS_DICT[params[0]]] = (~int(REGS[REGS_DICT[params[1]]]) | ~int(REGS[REGS_DICT[params[2]]])) 
    elif code == 'not':
        REGS[REGS_DICT[params[0]]] = ~int(REGS[REGS_DICT[params[1]]])
    elif code == 'or':
        REGS[REGS_DICT[params[0]]] = (int(REGS[REGS_DICT[params[1]]]) | int(REGS[REGS_DICT[params[2]]]))
    elif code == 'ori':
        REGS[REGS_DICT[params[0]]] = (int(REGS[REGS_DICT[params[1]]]) | int(params[2])) 
    elif code == 'wsbh':
        # MIPS32 Release 2 instruction
        pass
    elif code == 'xor':
        REGS[REGS_DICT[params[0]]] = (int(REGS[REGS_DICT[params[1]]]) ^ int(REGS[REGS_DICT[params[2]]]))
    elif code == 'xori':
        REGS[REGS_DICT[params[0]]] = (int(REGS[REGS_DICT[params[1]]]) ^ int(params[2])) 
    elif code == 'movn':
        if REGS[REGS_DICT[params[2]]] != 0:
            REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]]
    elif code == 'movz':
        if REGS[REGS_DICT[params[2]]] == 0:
            REGS[REGS_DICT[params[0]]] = REGS[REGS_DICT[params[1]]]
    elif code == 'slt' or code == 'sltu':
        # TODO: signed/unsigned
        if REGS[REGS_DICT[params[1]]] < REGS[REGS_DICT[params[2]]]:
            REGS[REGS_DICT[params[0]]] = 1
            PC+=1
        else:
            REGS[REGS_DICT[params[0]]] = 0
    elif code == 'slti' or code == 'sltiu':
        # TODO: signed/unsigned
        if REGS[REGS_DICT[params[1]]] < int(params[2]):
            REGS[REGS_DICT[params[0]]] = 1
            PC+=1
        else:
            REGS[REGS_DICT[params[0]]] = 0
    elif code == 'jr':
        PC = int(REGS[REGS_DICT['ra']])
    else:
        pass

def start():
    global PC
    while PC < len(IM):
        inst = IM[PC]
        ex(inst)
        PC+=1

def dump(f):
    
    prgmStart = False

    for x in f:
        if x == '\t.text\n':
            print('Program started')
            prgmStart = True
        elif prgmStart is True:
            inst = x.split()
            IM.append(inst)
             


if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    print('Loading program in memory...')
    
    dump(f)
    start()
    print('Program finished\n')
    print('-----------------------------------')
    print('-----------REGISTERS---------------')
    print('-----------------------------------')
    regs_dict_list = [x[0] for x in list(REGS_DICT.items())]
    for i in range(32):
        print(f"{regs_dict_list[i]}: {REGS[i]}")
