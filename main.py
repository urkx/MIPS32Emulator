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

def ex(inst):
    if inst[0] == 'move':
        param1 = inst[1].replace('$','').replace(',','')
        param2 = inst[2].replace('$','').replace(',','')
        REGS[REGS_DICT[param1]] = REGS[REGS_DICT[param2]]
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
            print('Program starts')
            prgmStart = True
        elif prgmStart is True:
            inst = x.split()
            IM.append(inst)
             


if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    print('Loading program in memory...')
    dump(f)
    start()
