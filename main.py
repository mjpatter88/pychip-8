import pyxel
from chip8 import Chip8

# Pyxel has minimum screen height of 64. Chip-8 display is 32, so draw it in the middle.
Y_OFFSET = 16

# The Chip 8 has a hex keyboard, so we need to translate the left hand side of a modern keyboard to the right keys.
# ╔═══╦═══╦═══╦═══╗
# ║ 1 ║ 2 ║ 3 ║ C ║
# ╠═══╬═══╬═══╬═══╣
# ║ 4 ║ 5 ║ 6 ║ D ║
# ╠═══╬═══╬═══╬═══╣
# ║ 7 ║ 8 ║ 9 ║ E ║
# ╠═══╬═══╬═══╬═══╣
# ║ A ║ 0 ║ B ║ F ║
# ╚═══╩═══╩═══╩═══╝
KEY_MAP = {
    pyxel.KEY_1: 1, pyxel.KEY_2: 2, pyxel.KEY_3: 3, pyxel.KEY_4: 0xC,
    pyxel.KEY_Q: 4, pyxel.KEY_W: 5, pyxel.KEY_E: 6, pyxel.KEY_R: 0xD,
    pyxel.KEY_A: 7, pyxel.KEY_S: 8, pyxel.KEY_D: 9, pyxel.KEY_F: 0xE,
    pyxel.KEY_Z: 0xA, pyxel.KEY_X: 0, pyxel.KEY_C: 0xB, pyxel.KEY_V: 0xF,
}

class App:
    def __init__(self, rom_file):
        self.chip = Chip8(rom_file)
        self.paused = False
        self.manual_step_mode = False
        self.should_step = False

        pyxel.init(64, 64, fps=200, scale=10)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnr(pyxel.KEY_P):
            if self.paused:
                print("Unpaused.")
                self.paused = False
            else:
                print("Paused.")
                self.paused = True

        # Use "n" to activate manual step mode
        if pyxel.btnr(pyxel.KEY_N):
            self.manual_step_mode = not self.manual_step_mode
        # Step once per "m" key press
        if pyxel.btnr(pyxel.KEY_M):
            self.should_step = True
        else:
            self.should_step = False

        if not self.paused and (self.should_step or not self.manual_step_mode):
            for key_in, chip8_key in KEY_MAP.items():
                if pyxel.btnr(key_in):
                    self.chip.set_key(chip8_key)
            self.chip.step()

    def draw(self):
        if self.chip.should_draw:
            pyxel.cls(6)
            for y, row in enumerate(self.chip.video_memory):
                for x, col in enumerate(row):
                    if col:
                        pyxel.pix(x, y+Y_OFFSET, 7)
                    else:
                        pyxel.pix(x, y+Y_OFFSET, 0)


def get_rom_filename(default=None):
    """
    Get a rom filename using the following priority:
    1. Default passed to this function.
    2. Filename passed as command line arg
    3. Display a file picker window for user input
    """
    import sys

    if default:
        return default
    elif len(sys.argv) > 1:
        return sys.argv[1]
    else:
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        # prevent the root window from appearing
        Tk().withdraw()
        filename = askopenfilename()
        return filename


# Working roms
ibm = "roms/ibm-logo.ch8"
ch8 = "roms/chip8-logo.ch8"
zero = "roms/ZeroDemo_zeroZshadow_2007.ch8"
test = "roms/test_opcode.ch8"

# Not yet working roms
triange = "roms/Sierpinski.ch8"
tetris = "roms/tetris.ch8"
sqrt = "roms/SqrtTest.ch8"
airplane = "rom-lib/games/Airplane.ch8"

if __name__ == "__main__":
    rom_file = get_rom_filename(triange)
    print(rom_file)
    App(rom_file)
