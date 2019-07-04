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
    def __init__(self):
        self.chip = Chip8()
        self.paused = False

        pyxel.init(64, 64, fps=100, scale=10)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnr(pyxel.KEY_P):
            if self.paused:
                print("Unpaused.")
                self.paused = False
            else:
                print("Paused.")
                self.paused = True

        if not self.paused:
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

App()
