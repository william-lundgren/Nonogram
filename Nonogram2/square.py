import pygame as pg
import random


class Square:
    side = None
    color = None
    game_display = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.toggled = False

        # 1 == Blå
        # 0 == Tom
        # -1 == Kryss
        self.true_state = random.randint(0, 1)
        self.shown_state = 0

    @staticmethod
    def set_side(s):
        Square.side = s
 
    @staticmethod
    def set_color(col):
        Square.color = col

    @staticmethod
    def set_display(disp):
        Square.game_display = disp

    def draw(self):
        offset = 0.25
        if self.shown_state == -1:
            pg.draw.line(Square.game_display, Square.color, (self.x + Square.side * offset, self.y + Square.side * offset),
                         (self.x + Square.side - Square.side * offset, self.y + Square.side - Square.side * offset), 4)
            pg.draw.line(Square.game_display, Square.color, (self.x + Square.side * offset, self.y + Square.side - Square.side * offset),
                         (self.x + Square.side - Square.side * offset, self.y + Square.side * offset), 4)

        elif self.shown_state == 1:
            pg.draw.rect(Square.game_display, Square.color, (self.x + 2, self.y + 2, Square.side - 3, Square.side - 3))

    def put_cross(self):
        self.shown_state = -1

    def fill(self):
        self.shown_state = 1

    def reset(self):
        self.shown_state = 0

    def get_shown_state(self):
        return self.shown_state

    def get_true_state(self):
        return self.true_state

    def set_shown_state(self, state):
        self.shown_state = state
