import pyxel
from chip8 import Chip8

# Pyxel has minimum screen height of 64. Chip-8 display is 32, so draw it in the middle.
Y_OFFSET = 16

class App:
    def __init__(self):
        self.chip = Chip8()

        pyxel.init(64, 64)
        pyxel.run(self.update, self.draw)

    def update(self):
        # input handling goes here.

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
