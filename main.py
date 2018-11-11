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
    def __init__(self, game):
        self.game = game

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

    def renderCursor(self, design=0, color=Color.LIGHT_GRAY):
        if design == 1:
            pyxel.pix(pyxel.mouse_x - 1, pyxel.mouse_y, color)
            pyxel.pix(pyxel.mouse_x + 1, pyxel.mouse_y, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y - 1, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y + 1, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y, color)
            self.chatbox(pyxel.mouse_x + 2, pyxel.mouse_y + 2, "({},{})".format(pyxel.mouse_x, pyxel.mouse_y))
        else:
            pyxel.pix(pyxel.mouse_x - 1, pyxel.mouse_y, color)
            pyxel.pix(pyxel.mouse_x + 1, pyxel.mouse_y, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y - 1, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y + 1, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y, color)

    def drawGrid(self, color=Color.LIGHT_GRAY):
        # draw tiles
        for x in range(self.game.tileX):
            pyxel.line((x * self.game.TILESIZE), 0, self.game.TILESIZE * x, self.game.TILESIZE * self.game.tileY, Color.DARK_GRAY)
        for y in range(self.game.tileY):
            pyxel.line(0, (y * self.game.TILESIZE), self.game.TILESIZE * self.game.tileY, self.game.TILESIZE * y, Color.DARK_GRAY)


class Game:
    def __init__(self):

        self.TILESIZE = 16

        self.tileX = 15
        self.tileY = 15

        pyxel.init(self.TILESIZE * self.tileX, self.TILESIZE * self.tileY)
        #pyxel.mouse(True)
        self.gui = Gui(self)
        self.renderGrid = True
        pyxel.run(self.update, self.draw)

    def update(self):
        # do game updates
        self.renderGrid = not self.renderGrid

    def draw(self):
        # clear the screen
        pyxel.cls(0)

        # draw things

        # draw 16x16 square for reference
        pyxel.rect(16, 16, 31, 31, Color.LIGHT_PURPLE)

        # some test chatboxes
        self.gui.chatbox(20, 20, "hello, welcome to HVAC")
        self.gui.chatbox(20, 40, "hello,\nwelcome to HVAC")
        self.gui.chatbox(20, 60, "hello,\nwelcome to hvac,\nglad you could make it")
        x, y = self.gui.chatbox(20, 85, "1\n 2 \n 3\n4", carrot=True)
        pyxel.pix(x, y, Color.GREEN)

        # render mouse cursor
        self.gui.renderCursor(design=1)


Game()
