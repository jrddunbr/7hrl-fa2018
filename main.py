#!/usr/bin/python3

import pyxel, enum

#
# rect: (x1, y1, x2, y2, color) draws filled rectangle
# rectb: (x1, y1, x2, y2, color) draws border of rectangle
# text: (x, y, text, color) draws text to screen
#

class Color(enum.IntEnum):
    BLACK = 0
    DARK_BLUE = 1
    DARK_PURPLE = 2
    TURQOISE = 3
    BROWN = 4
    DARK_GRAY = 5
    LIGHT_GRAY = 6
    WHITE = 7
    RED = 8
    ORANGE = 9
    YELLOW = 10
    GREEN = 11
    LIGHT_BLUE = 12
    LIGHT_PURPLE = 13
    PINK = 14
    TAN = 15

class Gui:
    def __init__(self):
        pass

    # render a chatbox to the screen
    def chatbox(self, x, y, text, carrot=False):
        # border size, text height, line height
        border = 2
        textHeight = 5
        textLength = 4
        lineHeight = 1

        lowest = y
        for num in range(len(text.split("\n"))):
            line = text.split("\n")[num].strip()
            # math
            xl = x
            yl = y + (textHeight + lineHeight) * num
            xr = x + (border) + len(line) * textLength
            yr = y + (2 * border) + textHeight * (num + 1) + lineHeight * num -1
            if yr > lowest:
                lowest = yr
            # render
            pyxel.rect(xl, yl, xr, yr, Color.WHITE)
        for num in range(len(text.split("\n"))):
            line = text.split("\n")[num].strip()
            # math
            xl = x + border
            yl = y + border + (textHeight + lineHeight) * num
            # render
            pyxel.text(xl, yl, line, Color.DARK_GRAY)

        if carrot:
            # Draw the text carrot
            pyxel.pix(x + 2, lowest + 1, Color.WHITE)
            pyxel.pix(x + 3, lowest + 1, Color.WHITE)
            pyxel.pix(x + 4, lowest + 1, Color.WHITE)
            pyxel.pix(x + 3, lowest + 2, Color.WHITE)

        return x + 3, lowest + 4 # two pixels drectly below text area carrot


class Game:
    def __init__(self):
        pyxel.init(200, 160)
        pyxel.mouse(True)
        self.gui = Gui()
        pyxel.run(self.update, self.draw)

    def update(self):
        # do game updates
        pass

    def draw(self):
        # clear the screen
        pyxel.cls(0)
        # draw things
        self.gui.chatbox(20, 20, "hello, welcome to HVAC")
        self.gui.chatbox(20, 40, "hello,\nwelcome to HVAC")
        self.gui.chatbox(20, 60, "hello,\nwelcome to hvac,\nglad you could make it")
        x, y = self.gui.chatbox(20, 85, "1\n 2 \n 3\n4", carrot=True)
        pyxel.pix(x, y, Color.GREEN)

Game()
