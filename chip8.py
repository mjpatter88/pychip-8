DEBUG = False

class Chip8:
    def __init__(self, rom_file="ZeroDemo_zeroZshadow_2007.ch8"):
        # 0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
        # 0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
        # 0x200-0xFFF - Program ROM and work RAM
        self.memory = [0] * 4096

        # Black and white display. 64 x 32 pixels (2048 total)
        # 0 - off
        # 1 - on
        self.video_memory = [0] * 2048
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
        pass


    def decode(self, opcode):
        if opcode == 0x00E0:
            return self.disp_clear
        elif (opcode & 0xF000) == 0x6000:
            return self.set_register_const
        elif (opcode & 0xF000) == 0xA000:
            return self.set_index
        else:
            return self.not_implemented_instr

    def disp_clear(self, _):
        print("Clear Display")
        self.video_memory = [0] * 2048
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

    def set_index(self, opcode):
        print("Set Index")
        const = opcode & 0x0FFF
        self.index = const
        self.pc += 2

        if DEBUG:
            print(format(opcode, '02x'))
            print(f"Constant Value: {const}")

    def not_implemented_instr(self, opcode):
        print(f"Not implemented opcode: {format(opcode, '02x')}")
        self.pc += 2

