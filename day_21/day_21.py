import sys
sys.path.append("../")
from int_code_machine import IntCodeMachine as ICM

ASCII = ICM()

springcode = """

// Note: J and T both start as F

OR A T
AND B T
AND C T
// T == (A and B and C)

NOT D J
// J == !D

OR T J
// J == !D or (A and B and C)

NOT J J
// J = !!D and !(A and B and C)
// J = D and (!A or !B or !C)

WALK

"""

springcode_b = """

OR A T
AND B T
AND C T
// T == (A and B and C)

NOT T T
// T == !(A and B and C)

OR H J
OR E J
// J == E or H 

AND D J
// J == D and (E or H)

AND T J
// J = !(A and B and C) and D and (E or H)

RUN

"""

for program in [springcode, springcode_b]:
    ASCII.reset()
    ASCII.run()
    for l in program.split('\n'):
        l = l.strip()
        if len(l) and not l.startswith('/'):
            ASCII.input_ascii(l)

    try:
        while c := ASCII.output_ascii():
            print(c, end='')
    except:
        pass
    print()