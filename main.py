import pyxel
from chip8 import Chip8

class App:
    def __init__(self):
        self.chip = Chip8()

        pyxel.init(160, 120)
        pyxel.run(self.update, self.draw)

    def update(self):
        # input handling goes here.

        self.chip.step()

    def draw(self):
        if self.chip.should_draw:
            pass

App()
