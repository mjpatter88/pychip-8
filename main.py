import pyxel
from chip8 import Chip8

class App:
    def __init__(self):
        self.chip = Chip8()

        pyxel.init(64, 32)
        pyxel.run(self.update, self.draw)

    def update(self):
        # input handling goes here.

        self.chip.step()

    def draw(self):
        if self.chip.should_draw:
            pyxel.cls(0)
            for y, row in enumerate(self.chip.video_memory):
                for x, col in enumerate(row):
                    if col:
                        pyxel.pix(x, y, 11)

App()
