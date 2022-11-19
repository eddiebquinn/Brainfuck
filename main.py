import sys


class MemoryBuffer:

    def __init__(self, size: int = 30000):
        self.pool = [0] * size
        self.ptr = 0

    def increment_ptr(self):
        # Potential error point if ptr goes beyond array
        self.ptr += 1

    def decrement_ptr(self):
        self.ptr = 0 if self.ptr <= 0 else self.ptr - 1

    def increment(self):
        self.pool[self.ptr] = self.pool[self.ptr] + \
            1 if self.pool[self.ptr] < 255 else 0

    def decrement(self):
        self.pool[self.ptr] = self.pool[self.ptr] - \
            1 if self.pool[self.ptr] > 0 else 255

    def current(self) -> int:
        return self.pool[self.ptr]

    def store(self, val: int):
        self.pool[self.ptr] = val

    def __str__(self) -> str:
        return f"ptr: {self.ptr}, Value:{self.current()}"


class Program:

    def __init__(self, program: str):
        self.program = self.__extract_code(program)
        self.pos = 0
        self.loop_map = self.__build_loop_map()

    def __extract_code(self, file) -> str:
        f = open(file, "r")
        code = "".join(x for x in f.read() if x in [
            '.', ',', '[', ']', '<', '>', '+', '-'])
        f.close()
        return code

    def __build_loop_map(self) -> dict:
        # This is also a error point because it doesnt know how to cope with nested loops
        temp_loopstack, loopmap = [], {}
        for position, command in enumerate(self.program):
            if command == "[":
                temp_loopstack.append(position)
            if command == "]":
                start = temp_loopstack.pop()
                loopmap[start] = position
                loopmap[position] = start
        return loopmap

    def advance(self, n=1):
        self.pos += n

    def current(self) -> str:
        return self.program[self.pos]

    def eof(self) -> bool:
        return self.pos == len(self.program)

    def __str__(self) -> str:
        return f"position: {self.pos}, Command: {self.current()}"


class Interpreter:

    def __init__(self, program: Program, buffer: MemoryBuffer):
        self.program = program
        self.mem = buffer

        self.output = []

    def __inc_ptr(self):
        self.mem.increment_ptr()

    def __dec_ptr(self):
        self.mem.decrement_ptr()

    def __inc_byte(self):
        self.mem.increment()

    def __dec_byte(self):
        self.mem.decrement()

    def __jump_forward(self):
        if self.mem.current() == 0:
            self.program.pos = self.program.loop_map[self.program.pos]

    def __jump_backward(self):
        if self.mem.current() != 0:
            self.program.pos = self.program.loop_map[self.program.pos]

    def __output_byte(self):
        self.output.append(chr(self.mem.current()))

    def __input_byte(self):
        i = input("PLEASE INSERT CHARCTER YOU WANT TO INSERT INTO MEMORY -")
        self.mem.store(i)

    def evaluate(self) -> list:
        cmd_dict = {
            ">": self.__inc_ptr,
            "<": self.__dec_ptr,
            "+": self.__inc_byte,
            "-": self.__dec_byte,
            ".": self.__output_byte,
            ",": self.__input_byte,
            "[": self.__jump_forward,
            "]": self.__jump_backward
        }

        while not self.program.eof():
            cmd = cmd_dict.get(self.program.current())
            if cmd:
                cmd()
            self.program.advance()

        return "".join(x for x in self.output)


def main():
    if len(sys.argv) <= 1:
        print("Please provide file ending with .bf to evaluate")
        return

    program = Program(sys.argv[1])
    buffer = MemoryBuffer(30000)
    interpreter = Interpreter(program=program, buffer=buffer)
    output = interpreter.evaluate()

    print(output)


if __name__ == "__main__":
    main()
