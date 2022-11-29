import sys


class MemoryBuffer:

    def __init__(self, size: int = 30000):
        self.pool = [0] * size
        self.ptr = 0

    def increment_ptr(self):
        self.ptr = len(self.pool) if self.ptr >= len(
            self.pool) else self.ptr + 1

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

    def __extract_code(self, file) -> str:
        f = open(file, "r")
        code = "".join(x for x in f.read() if x in [
            '.', ',', '[', ']', '<', '>', '+', '-'])
        f.close()
        return code

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
        # The jump forward and backward method can be improved, these two methods
        # are simmilar enough they can become one method
        val = self.mem.current()
        if val == 0:
            count = 1
            while count:
                self.program.advance()
                if self.program.current() == "[":
                    count += 1
                if self.program.current() == "]":
                    count -= 1

    def __jump_backward(self):
        if self.mem.current() != 0:
            count = 1
            while count:
                self.program.advance(-1)
                if self.program.current() == "]":
                    count += 1
                if self.program.current() == "[":
                    count -= 1

    def __output_byte(self):
        self.output.append(chr(self.mem.current()))

    def __input_byte(self):
        i = input("PLEASE INSERT CHARCTER YOU WANT TO INSERT INTO MEMORY -")
        self.mem.store(i)

    def evaluate(self) -> str:
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
