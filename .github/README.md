# Brainfuck
Brainfuck is an esoteric programming language created in 1993 by Urban Müller. Notable for its extreme minimalism, the language consists of only eight simple commands, a data pointer and an instruction pointer. While it is fully Turing complete, it is not intended for practical use, but to challenge and amuse programmers. 

One of the first hackathons I ever took part in requires us to code a Brainfuck interpreter in less than 1h. While my team failed, I felt we did come up with a good solution to it. Rather than dealing with the problem via a series of `if` statements, given the predictable nature of Brainfuck we decided to use a dictionary that maps the various commands to a series of functions.

## Language design
The language itself consists of only eight commands, listed below. A brainfuck program is a sequence of these characters, sometimes interspersed with other characters uses as comments (these are ignored when running the program). The commands are executed sequanttially. The language uses a simple machine model consisting of the program instruction pointer as well as a one-dimensional array of 30000B all of which init to `0`, a data pointer which ints to the left-most bite, and two streams of bytes for input and output (the output being in ASCII).

### Commands
The eight commands consist of a single character
| Char | Meaning |
|----|----|
| `>` | Increment the data pointer |
| `<` | Decrement the data pointer |
| `+` | Increment the byte at the data pointer |
| `-` | Decrement the byte at the data pointer |
| `.` | Output the byte at the data pointer |
| `,` | Accepts one byte of input, storing its value at the data pointer |
| `[` | If the byte at the data pointer is zero, skip ahead to the byte after the corresponding `]` |
| `]` | If the byte at the data pointer is non-zero, skip back to the byte after the corresponding `[` |


## Usage
```brainfuck HelloWorld.bf```
