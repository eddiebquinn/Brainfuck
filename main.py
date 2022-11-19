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


def execute(file):
    f = open(file, "r")
    output = evaluate(f.read())
    f.close()

    output = "".join(x for x in output)
    print(output)


def evaluate(code):
    code = cleanup(list(code))
    loop_map = build_loopMap(code)
    output = []

    mem, codeptr, = MemoryBuffer(), 0

    while codeptr < len(code):
        command = code[codeptr]
        print(command)

        if command == ">":
            mem.increment_ptr()

        if command == "<":
            mem.decrement_ptr()

        if command == "+":
            mem.increment()

        if command == "-":
            mem.decrement()

        if command == "[" and mem.current() == 0:
            codeptr = loop_map[codeptr]

        if command == "]" and mem.current() != 0:
            codeptr = loop_map[codeptr]

        if command == ".":
            output.append(chr(mem.current()))

        if command == ",":
            i = input("PLEASE INSERT CHARCTER YOU WANT TO INSERT INTO MEMORY -")
            mem.store(i)

        codeptr += 1

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
