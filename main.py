import sys


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

    mem, codeptr, memptr = [0], 0, 0

    while codeptr < len(code):
        command = code[codeptr]
        print(command)

        if command == ">":
            memptr += 1
            if memptr == len(mem):
                mem.append(0)

        if command == "<":
            memptr = 0 if memptr <= 0 else memptr - 1

        if command == "+":
            mem[memptr] = mem[memptr] + 1 if mem[memptr] < 255 else 0

        if command == "-":
            mem[memptr] = mem[memptr] - 1 if mem[memptr] > 0 else 255

        if command == "[" and mem[memptr] == 0:
            codeptr = loop_map[codeptr]

        if command == "]" and mem[memptr] != 0:
            codeptr = loop_map[codeptr]

        if command == ".":
            raw_output = mem[memptr]
            output.append(chr(mem[memptr]))

        if command == ",":
            i = input("PLEASE INSERT CHARCTER YOU WANT TO INSERT INTO MEMORY -")
            mem[memptr] = int(i)

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
