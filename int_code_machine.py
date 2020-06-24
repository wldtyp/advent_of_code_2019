import fileinput
from itertools import zip_longest

class IntCodeMachine(object):
    """docstring for IntCodeMachine"""
    
    HALT = 'HALT'
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    RUN = 'RUN'

    def __init__(self, data=None):
        super(IntCodeMachine, self).__init__()
        if data is None:
            contents = next(fileinput.input())
            data = [int(x) for x in contents.split(",")]
        self._inital_data = data + [0] * 10000
        self.reset()

        self.ops = {
            1: AddOP(self),
            2: MultiplyOP(self),
            3: InputOP(self),
            4: OutputOP(self),
            5: JumpTrueOP(self),
            6: JumpFalseOP(self),
            7: LessThanOP(self),
            8: EqualOP(self),
            9: RelativeBaseOP(self),
            99: HaltOP(self)
        }

    def get_op_code(self):
        op_code = str(self.data[self.head])
        new_op_code = int(op_code[-2:])
        return new_op_code
        
    def input(self, x):
        if isinstance(x,list):
            self.inputs.extend(x)
        else:
            self.inputs.append(x)
        self.run()

    def input_ascii(self, x):
        ascii_input = [ord(c) for c in x]
        self.input(ascii_input + [10])
        # self.input(10) # newline

    def output(self):
        try:
            out = self.outputs.pop(0)
            self.run()
            return out
        except IndexError:
            return None

    def output_ascii(self):
        o = self.output()
        return chr(o) if o and o < 126 else o

    def run(self):
        self.state = 'RUN'
        while self.state == IntCodeMachine.RUN:
            op_code = self.get_op_code()    
            op = self.ops[op_code]
            self.head, self.state = op.apply(self.head, self.data)
        return self.outputs

    def reset(self):
        self.data = self._inital_data.copy()
        self.inputs = []
        self.outputs = []
        self.head = 0
        self.state = IntCodeMachine.RUN
        self.relative_base = 0

class Op(object):

    def __init__(self, machine):
        super(Op, self).__init__()
        self.machine = machine
        self.name = 'OP'
        self.parameters = []
        self.parameter_types = ''
        self.state = IntCodeMachine.RUN
        self.next_instruction = None
        self.result = None

    @property
    def instruction_length(self):
        return len(self.parameter_types) + 1

    def apply(self, head, data):
        self.next_instruction = head + self.instruction_length
        self.state = IntCodeMachine.RUN
        self.read_parameters(head, data)
        # self.debug()
        self.resolve_addresses(data)
        self.op(data)
        self.write_result()
        # self.debug()
        return self.next_instruction, self.state

    def read_parameters(self, head, data):
        instruction = str(data[head])
        self.modes = [int(x) for x in reversed(instruction[:-2])]
        self.parameters = data[head + 1:head + self.instruction_length]

    def resolve_addresses(self, data):
        for i, ptype, mode, value in zip_longest(range(len(self.parameter_types)), self.parameter_types, self.modes, self.parameters):
            if mode in [0, 2, None]:
                if mode == 2:
                    value += self.machine.relative_base
                if ptype == 'r':
                    self.parameters[i] = data[value]
                elif ptype == 'w':
                    self.parameters[i] = value

    def write_result(self):
        pass

    def debug(self):
        print(f"{self.machine.head} {self.name} {self.modes} {self.parameters}")


class AddOP(Op):
    
    def __init__(self, machine):
        super(AddOP, self).__init__(machine)
        self.name = 'ADD'
        self.parameter_types = 'rrw'

    def op(self, data):
        a, b, address = self.parameters
        data[address] = a + b


class MultiplyOP(Op):

    def __init__(self, machine):
        super(MultiplyOP, self).__init__(machine)
        self.name = 'MUL'
        self.parameter_types = 'rrw'

    def op(self, data):
        a, b, address = self.parameters
        data[address] = a * b


class EqualOP(Op):

    def __init__(self, machine):
        super(EqualOP, self).__init__(machine)
        self.name = 'EQ'
        self.parameter_types = 'rrw'

    def op(self, data):
        a, b, address = self.parameters
        data[address] = 1 if a == b else 0


class LessThanOP(Op):

    def __init__(self, machine):
        super(LessThanOP, self).__init__(machine)
        self.name = 'LESS'
        self.parameter_types = 'rrw'

    def op(self, data):
        a, b, address = self.parameters
        data[address] = 1 if a < b else 0


class HaltOP(Op):

    def __init__(self, machine):
        super(HaltOP, self).__init__(machine)
        self.name = 'HALT'
        self.parameter_types = 'r'

    def apply(self, head, data):
        return head, IntCodeMachine.HALT


class JumpTrueOP(Op):

    def __init__(self, machine):
        super(JumpTrueOP, self).__init__(machine)
        self.name = 'JMPT'
        self.parameter_types = 'rr'

    def op(self, data):
        a, b = self.parameters
        if a != 0:
            self.next_instruction = b


class JumpFalseOP(Op):

    def __init__(self, machine):
        super(JumpFalseOP, self).__init__(machine)
        self.name = 'JMPF'
        self.parameter_types = 'rr'

    def op(self, data):
        a, b = self.parameters
        if a == 0:
            self.next_instruction = b


class InputOP(Op):

    def __init__(self, machine):
        super(InputOP, self).__init__(machine)
        self.name = 'INPUT'
        self.parameter_types = 'w'

    def op(self, data):
        self.state = 'RUN'
        a = self.parameters[0]
        try:
            data[a] = self.machine.inputs.pop(0)
        except:
            self.next_instruction = self.machine.head
            self.state = IntCodeMachine.INPUT


class OutputOP(Op):

    def __init__(self, machine):
        super(OutputOP, self).__init__(machine)
        self.name = 'OUTPUT'
        self.parameter_types = 'r'

    def op(self, data):
        output = self.parameters[0]
        self.machine.outputs.append(output)
        self.state = IntCodeMachine.OUTPUT


class RelativeBaseOP(Op):

    def __init__(self, machine):
        super(RelativeBaseOP, self).__init__(machine)
        self.name = 'REBASE'
        self.parameter_types = 'r'

    def op(self, data):
        self.machine.relative_base += self.parameters[0]
