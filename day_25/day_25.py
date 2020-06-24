import sys

sys.path.append("../")
from int_code_machine import IntCodeMachine as ICM


ZORK = ICM()
ZORK.run()

while True:
    try:
        while c := ZORK.output_ascii():
            print(c, end="")
    except:
        pass
    if ZORK.state == ICM.INPUT:
        i = input()
        ZORK.input_ascii(i)
