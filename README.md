![Chip 8](images/ch8.jpg?raw=true "Chip 8")
![Zero](images/zero.jpg?raw=true "Zero")
![Logo Drawing](images/ibm-logo.jpg?raw=true "IBM Logo")
![Triangles](images/tri.jpg?raw=true "Triangles")
![Square Root](images/sqrt.jpg?raw=true "Square Root")


* Install `pyxel` dependencies - [https://github.com/kitao/pyxel#how-to-install]
* Install project dependencies - `pipenv install` or `pip install pyxel`
* Start emulating: `python main.py`
* Use `p` to pause, `n` to enable manual stepping, and `m` to step once.

View a rom in hex - `xxd file_name.ch8`


Useful resources:
* https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
* http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
* https://github.com/dmatlack/chip8/tree/master/roms
* https://github.com/mattmikolay/chip-8/
* https://rawgit.com/alexanderdickson/Chip-8-Emulator/master/index.html
* http://mattmik.com/files/chip8/mastering/chip8.html
* https://github.com/mattmikolay/chip-8/wiki/CHIP%E2%80%908-Technical-Reference
* https://github.com/mattmikolay/chip-8/wiki/CHIP%E2%80%908-Instruction-Set
* https://github.com/dmatlack/chip8/tree/master/roms
* http://www.cs.columbia.edu/~sedwards/classes/2016/4840-spring/designs/Chip8.pdf

Major Steps:
1. Basic execution loop
2. Read from rom into memory
3. Fetch/Decode/Execute
4. Draw video memory to screen
5. Basic logic instructions
6. Draw sprite instructions
7. Flow control instructions
8. Timers
9. Input
10. Font related instructions

Instructions:
* 0NNN
* 00E0 - DONE
* 00EE - DONE
* 1NNN - DONE
* 2NNN - DONE
* 3XNN - DONE
* 4XNN - DONE
* 5XY0 - DONE
* 6XNN - DONE
* 7XNN - DONE
* 8XY0 - DONE
* 8XY1 - DONE
* 8XY2 - DONE
* 8XY3 - DONE
* 8XY4 - DONE
* 8XY5 - DONE
* 8XY6 - DONE
* 8XY7
* 8XYE - DONE
* 9XY0 - DONE
* ANNN - DONE
* BNNN
* CXNN - DONE
* DXYN - DONE
* EX9E - DONE
* EXA1 - DONE
* FX07 - DONE
* FX0A
* FX15 - DONE
* FX18
* FX1E - DONE
* FX29 - DONE
* FX33 - DONE
* FX55 - DONE
* FX65 - DONE
