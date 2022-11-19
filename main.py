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

    def dump(self, start, end) -> list:
        return self.pool[start:end]

    def __str__(self):
        return f"ptr: {self.ptr}, Value:{self.current()}"


class Program:

    def __init__(self, program: str):
        self.program = program
        self.pos = 0

    def advance(self, n=1):
        self.pos += n

    def current(self) -> str:
        return self.program[self.pos]

    def eof(self) -> bool:
        return self.pos == len(self.program)

    def __str__(self):
        return f"position: {self.pos}, Command: {self.current()}"


class Interpreter:

    def __init__(self, program: Program, buffer: MemoryBuffer, loop_map: dict):
        self.program = program
        self.mem = buffer
        self.loop_map = loop_map

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
            self.program.pos = self.loop_map[self.program.pos]

    def __jump_backward(self):
        if self.mem.current() != 0:
            self.program.pos = self.loop_map[self.program.pos]

    def __output_byte(self):
        self.output.append(chr(self.mem.current()))

    def __input_byte(self):
        i = input("PLEASE INSERT CHARCTER YOU WANT TO INSERT INTO MEMORY -")
        self.mem.store(i)

    def evaluate(self):
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

        return self.output


def execute(file):
    f = open(file, "r")
    output = evaluate(f.read())
    f.close()

    output = "".join(x for x in output)
    print(output)


def evaluate(code):
    code = cleanup(list(code))
    loop_map = build_loopMap(code)

    program = Program(code)
    buffer = MemoryBuffer(30000)
    interpreter = Interpreter(
        program=program, buffer=buffer, loop_map=loop_map)
    output = interpreter.evaluate()

    return output


def cleanup(raw_code):
    clean_code = "".join(x for x in raw_code if x in [
        '.', ',', '[', ']', '<', '>', '+', '-'])
    return clean_code


def build_loopMap(code):
    temp_loopstack, loopmap = [], {}
    for position, command in enumerate(code):
        if command == "[":
            temp_loopstack.append(position)
        if command == "]":
            start = temp_loopstack.pop()
            loopmap[start] = position
            loopmap[position] = start
    return loopmap


def main():
    if len(sys.argv) <= 1:
        print("Please provide file ending with .bf to evaluate")
        return
    execute(sys.argv[1])


if __name__ == "__main__":
    main()
