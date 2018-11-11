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
        if design == 2:
            pyxel.pix(pyxel.mouse_x - 1, pyxel.mouse_y, color)
            pyxel.pix(pyxel.mouse_x + 1, pyxel.mouse_y, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y - 1, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y + 1, color)
            pyxel.pix(pyxel.mouse_x, pyxel.mouse_y, color)
            self.chatbox(pyxel.mouse_x + 2, pyxel.mouse_y + 2, "({},{})\n{},{}".format(pyxel.mouse_x, pyxel.mouse_y, self.game.tx, self.game.ty))
        elif design == 1:
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

class Entity:
    def __init__(self, game):
        self.game = game

    def drawPlayer(self):
        # render player location
        pyxel.rect(self.game.tx * self.game.TILESIZE, self.game.ty * self.game.TILESIZE, self.game.tx * self.game.TILESIZE + 15, self.game.ty * self.game.TILESIZE + 15, Color.LIGHT_BLUE)

class Thing:
    def __init__(self, game, x, y, thing):
        self.game = game
        self.solid = True
        self.tx = x
        self.ty = y
        self.thing = thing

    def isSolid(self):
        return self.solid

    def setSolid(self, solid = True):
        self.solid = solid

    def drawThing(self):
        pyxel.blt(self.tx * self.game.TILESIZE, self.ty * self.game.TILESIZE, 1, 0, 0, self.game.TILESIZE, self.game.TILESIZE)

class Game:
    def __init__(self):

        self.TILESIZE = 16

        self.tileX = 15
        self.tileY = 15

        pyxel.init(self.TILESIZE * self.tileX, self.TILESIZE * self.tileY)
        #pyxel.mouse(True)
        self.gui = Gui(self)
        self.entity = Entity(self)

        pyxel.image(1).load(0, 0, "assets/wall.png")
        pyxel.image(0).load(0, 0, "assets/mainTile.png")

        self.renderGrid = True

        self.tx = 2
        self.ty = 2

        self.vx = 0
        self.vy = 0

        self.things = []
        self.things.append(Thing(self, 1, 1, "wall"))
        self.things.append(Thing(self, 2, 1, "wall"))
        self.things.append(Thing(self, 3, 1, "wall"))
        self.things.append(Thing(self, 4, 1, "wall"))

        pyxel.run(self.update, self.draw)

    def update(self):
        # do game updates
        self.renderGrid = not self.renderGrid

        # handle player movements
        self.tx += self.vx
        self.ty += self.vy
        self.vx = 0
        self.vy = 0

    def draw(self):
        # clear the screen
        pyxel.cls(Color.BLACK)

        # draw tile background
        for x in range(self.tileX):
            for y in range(self.tileY):
                pyxel.blt(x * self.TILESIZE, y * self.TILESIZE, 0, 0, 0, self.TILESIZE, self.TILESIZE)

        # draw "things"
        for thing in self.things:
            thing.drawThing()

        # motion handling stuff
        if pyxel.btn(pyxel.KEY_W):
            print("W pressed")
            if self.ty != 0:
                self.vy = -1

        if pyxel.btn(pyxel.KEY_A):
            print("A pressed")
            if self.tx != 0:
                self.vx = -1

        if pyxel.btn(pyxel.KEY_S):
            print("S pressed")
            if self.ty != self.tileY - 1:
                self.vy = 1

        if pyxel.btn(pyxel.KEY_D):
            print("D pressed")
            if self.tx!= self.tileX - 1:
                self.vx = 1

        # draw player
        self.entity.drawPlayer()

        # render mouse cursor
        self.gui.renderCursor(design=1)

Game()
