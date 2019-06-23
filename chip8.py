from utils import byte_to_bits
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32
DEBUG = False

ibm = "ibm-logo.ch8"
ch8 = "chip8-logo.ch8"
zero = "ZeroDemo_zeroZshadow_2007.ch8"
tetris = "tetris.ch8"

class Chip8:
    def __init__(self, rom_file=tetris):
        # 0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
        # 0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
        # 0x200-0xFFF - Program ROM and work RAM
        self.memory = [0] * 4096

        # Black and white display. 64 x 32 pixels (2048 total)
        # 0 - off
        # 1 - on
        self.video_memory = self.gen_blank_video_memory()
        self.should_draw = False

        # V0, V1,,, VE
        self.registers = [0] * 16

        # I
        self.index = 0

        # Both timers count down to 0 at 60Hz.
        self.delay_timer = 0
        self.sound_timer = 0

        self.opcode = None
        self.pc = 0x200 # Program rom gets loaded into memory starting at 0x200

        # It is important to know that the Chip 8 instruction set has opcodes that allow the program to jump to a certain address or call a subroutine.
        # While the specification don’t mention a stack, you will need to implement one as part of the interpreter yourself.
        # The stack is used to remember the current location before a jump is performed.
        # So anytime you perform a jump or call a subroutine, store the program counter in the stack before proceeding.
        # The system has 16 levels of stack and in order to remember which level of the stack is used, you need to implement a stack pointer (sp).
        self.stack = [0] * 16
        self.stack_pointer = 0

        # Hex based keypad.
        # Store the state of each key
        self.keys = [0] * 16

        self.load_rom(rom_file)

    def load_rom(self, file_name):
        file = f"roms/{file_name}"
        with open(file, "rb") as rom:
            mem_index = 0x200 # Program rom gets loaded into memory starting at 0x200
            for byte in rom.read():
                self.memory[mem_index] = byte
                mem_index += 1

    def dump_memory(self):
        # Words are 16 bits each.
        # Print in hex
        mem_index = 0
        while mem_index < 4096:
            value = self.memory[mem_index] << 8 | self.memory[mem_index + 1]
            print(format(value, '02x'), end=',')
            mem_index += 2
        print()

    def step(self):
        print(f"PC: {self.pc}", end=" ")
        # Fetch opcode
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]

        # Decode opcode
        instr = self.decode(self.opcode)

        # Execute opcode
        self.should_draw = False # default to false, specific opcodes can override this
        instr(self.opcode)

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1


    def decode(self, opcode):
        if opcode == 0x00E0:
            return self.disp_clear
        elif opcode == 0x00EE:
            return self.return_from_subroutine
        elif (opcode & 0xF000) == 0x1000:
            return self.jump_to_constant
        elif (opcode & 0xF000) == 0x2000:
            return self.call_subroutine
        elif (opcode & 0xF000) == 0x3000:
            return self.skip_if_equal
        elif (opcode & 0xF000) == 0x4000:
            return self.skip_if_not_equal
        elif (opcode & 0xF000) == 0x6000:
            return self.set_register_const
        elif (opcode & 0xF000) == 0x7000:
            return self.add_register_const
        elif (opcode & 0xF000) == 0xA000:
            return self.set_index
        elif (opcode & 0xF000) == 0xD000:
            return self.draw_sprite
        elif (opcode & 0xF0FF) == 0xF015:
            return self.set_delay_timer
        elif (opcode & 0xF0FF) == 0xF01E:
            return self.add_index
        else:
            return self.not_implemented_instr

    def disp_clear(self, _):
        print("Clear Display")
        self.video_memory = self.gen_blank_video_memory()
        self.should_draw = True
        self.pc += 2

    def set_register_const(self, opcode):
        print("Set Register to Constant")
        reg_index = (opcode & 0x0F00) >> 8
        const = opcode & 0x00FF
        self.registers[reg_index] = const
        self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Register Index: {reg_index}")
            print(f"Constant Value: {const}")
            print()

    def add_register_const(self, opcode):
        print("Add Constant to Register")
        reg_index = (opcode & 0x0F00) >> 8
        const = opcode & 0x00FF
        result = self.registers[reg_index] + const
        # Silently overflow per the spec.
        self.registers[reg_index] = result % (2**8)
        self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Register Index: {reg_index}")
            print(f"Constant Value: {const}")
            print()

    def set_index(self, opcode):
        print("Set Index")
        const = opcode & 0x0FFF
        self.index = const
        self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Constant Value: {const}")
            print()

    def add_index(self, opcode):
        print("Add to Index")
        reg_index = (opcode & 0x0F00) >> 8
        value = self.registers[reg_index]
        result = self.index + value
        # The index register is 16 bits.
        self.index = result % (2 ** 16)
        # Set overflow if it occured, clear overflow otherwise
        if result >= 2**16:
            self.registers[15] = 1
        else:
            self.registers[15] = 0

        self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Register Index: {reg_index}")
            print()

    def call_subroutine(self, opcode):
        print("Call Subroutine")
        addr = opcode & 0x0FFF
        self.stack[self.stack_pointer] = self.pc
        self.stack_pointer += 1
        self.pc = addr

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Address: {addr}")
            print()

    def jump_to_constant(self, opcode):
        print("Jump To Constant")
        const = opcode & 0x0FFF
        self.pc = const

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Address: {const}")
            print()

    def return_from_subroutine(self, opcode):
        print("Return From Subroutine")

        # value stored on stack is the calling address, we want the instruction after that so we add 2. 
        # stack pointer points to next open spot, so we subtract 1 to get last item on stack.
        addr = self.stack[self.stack_pointer - 1] + 2
        self.stack_pointer -= 1
        self.pc = addr

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Address: {addr}")
            print()

    def set_delay_timer(self, opcode):
        print("Set Delay Timer")
        reg_index = (opcode & 0x0F00) >> 8
        value = self.registers[reg_index]

        self.delay_timer = value
        self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Register: {reg_index}")
            print(f"Value: {value}")
            print()

    def skip_if_equal(self, opcode):
        print("Skip If Equal")
        reg_index = (opcode & 0x0F00) >> 8
        value = self.registers[reg_index]
        const = opcode & 0x00FF

        if const == value:
            self.pc += 4
        else:
            self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Register: {reg_index}")
            print(f"Value: {value}")
            print(f"Const: {const}")
            print()

    def skip_if_not_equal(self, opcode):
        print("Skip If Not Equal")
        reg_index = (opcode & 0x0F00) >> 8
        value = self.registers[reg_index]
        const = opcode & 0x00FF

        if const != value:
            self.pc += 4
        else:
            self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Register: {reg_index}")
            print(f"Value: {value}")
            print(f"Const: {const}")
            print()

    def draw_sprite(self, opcode):
        print("Draw Sprite")
        x = self.registers[(opcode & 0x0F00) >> 8]
        y = self.registers[(opcode & 0x00F0) >> 4]
        height = opcode & 0x000F
        if DEBUG:
            print(format(opcode, '02x'))
            print(f"X: {x}")
            print(f"Y: {y}")
            print(f"Height: {height}")
            print()

        for sprite_row in range(height):
            sprite_line = self.memory[self.index + sprite_row]
            bits = byte_to_bits(sprite_line)
            for ind, bit in enumerate(bits):
                row = y + sprite_row
                col = x + ind
                if bit:
                    if self.video_memory[row][col]:
                        self.video_memory[row][col] = 0
                        self.registers[0xF] = 1
                    else:
                        self.video_memory[row][col] = 1

        self.should_draw = True
        self.pc += 2


    def not_implemented_instr(self, opcode):
        print(f"Not implemented opcode: {format(opcode, '02x')}")
        self.pc += 2

    def gen_blank_video_memory(self):
        video_memory = []
        for row in range(DISPLAY_HEIGHT):
            video_memory.append([0] * DISPLAY_WIDTH)
        return video_memory
