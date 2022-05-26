import math

import pygame as pg
from board import Board
from square import Square


def text(screen, x, y, txt, size, color):
    font = pg.font.Font(pg.font.get_default_font(), size)
    text_surface = font.render(txt, True, color)
    screen.blit(text_surface, (x - text_surface.get_rect().width/2, y - text_surface.get_rect().height/2))


def text_right(screen, x, y, txt, size, color):
    font = pg.font.Font(pg.font.get_default_font(), size)
    text_surface = font.render(txt, True, color)
    screen.blit(text_surface, (x - text_surface.get_rect().width - 10, y - text_surface.get_rect().height/2))


def vert_text(screen, x, y, txt, size, color):
    font = pg.font.Font(pg.font.get_default_font(), size)
    nums = txt.split()
    for i, ele in enumerate(reversed(nums)):
        text_surface = font.render(ele, True, color)
        screen.blit(text_surface, (x - text_surface.get_rect().width / 2,
                    y - text_surface.get_rect().height - 3 - text_surface.get_rect().height * i))


def button(screen, x, y, color, color2, color3, length, r, mode):
    offset = 0.75
    offset_s = 0.60
    pg.draw.rect(screen, color, (x - length / 2, y - r, length, 2 * r))
    if mode == "fill":
        pg.draw.circle(screen, color2, (x + length / 2, y), r)
        pg.draw.circle(screen, color, (x - length / 2, y), r)
    if mode == "cross":
        pg.draw.circle(screen, color, (x + length / 2, y), r)
        pg.draw.circle(screen, color2, (x - length / 2, y), r)

    delta = int(round((r*offset)/math.sqrt(2)))

    x1 = x - length/2 - delta
    x2 = x - length/2 + delta
    y1 = y - delta
    y2 = y + delta

    # Draw cross
    # Negative slope line
    pg.draw.line(Square.game_display, color3, (x1, y1), (x2, y2), 4)
    # Positive slope line
    pg.draw.line(Square.game_display, color3, (x1, y2), (x2, y1), 4)

    pg.draw.rect(Square.game_display, color3, (x + length/ 2 - r*offset_s, y - r*offset_s, 2*r*offset_s, 2*r*offset_s))


def main():
    black = (4, 7, 41)
    white = (255, 255, 255)
    blue = (66, 74, 189)
    grey = (30, 30, 33)
    light_blue = (102, 102, 255)
    purp_blue = (168, 168, 255)

    pg.init()
    pg.display.set_caption("Nonogram")
    WIDTH, HEIGHT = 900, 900
    game_display = pg.display.set_mode((WIDTH, HEIGHT))
    game_exit = False
    clock = pg.time.Clock()

    x_off, y_off = WIDTH/4.5, HEIGHT/4.5
    cols, rows = 15, 15
    side = WIDTH/cols*2/3

    b = Board(x_off, y_off, cols, rows, side, game_display, blue, purp_blue)
    b.generate_board()

    mode = "fill"
    toggled_squares = []

    # Which states to toggle when dragging
    swipe_toggle = None

    # How many have been turned on

    # Total amount of squares
    total = 0

    button_height = int(2 * HEIGHT / 45)
    button_width = 2*button_height + 3

    for i in range(b.rows):
        total += b.count_row(i)

    row = -1
    col = -1

    while not game_exit:

        game_display.fill(grey)

        button(game_display, WIDTH / 2, 0.945 * HEIGHT, blue, light_blue, grey, button_width, button_height, mode)

        b.draw_board()
        b.draw_squares()

        text(game_display, WIDTH / 2, 0.05 * HEIGHT, str(b.filled) + "/" + str(total), int(29*WIDTH/900), light_blue)

        for i in range(b.rows):
            text_right(game_display, x_off, y_off + side / 2 + i * side, b.row_side_nums(i), int(24*WIDTH/900), light_blue)
            vert_text(game_display, x_off + i * side + side/2, y_off, b.col_side_nums(i), int(24*WIDTH/900), light_blue)

        if b.check_win():
            clock.tick(60)
            pg.display.update()
            print("You won!")
            ''' inp = False
            while not inp:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            inp = True

            main()'''

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and mode == "fill":
                    mode = "cross"
                elif event.key == pg.K_SPACE and mode == "cross":
                    mode = "fill"
                elif event.key == pg.K_s:
                    b.show_solution()
                elif event.key == pg.K_c:
                    b.clear()

            if event.type == pg.MOUSEBUTTONUP:
                for s in toggled_squares:
                    s.toggled = False
                swipe_toggle = None
                col = -1
                row = -1

            x, y = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and b.in_box(x, y):
                try:
                    s = b.find_square(x, y)
                    if mode == "fill" and s.get_shown_state() != 1 and not s.toggled:
                        if swipe_toggle is None or swipe_toggle == 1:
                            if col == -1 and row == -1:
                                swipe_toggle = 1
                                s.fill()
                                s.toggled = True
                                toggled_squares.append(s)
                                b.filled += 1
                                col = b.find_col(x)
                                row = b.find_row(y)
                            else:
                                if col == b.find_col(x):
                                    swipe_toggle = 1
                                    s.fill()
                                    s.toggled = True
                                    toggled_squares.append(s)
                                    b.filled += 1
                                    row = -1
                                elif row == b.find_row(y):
                                    swipe_toggle = 1
                                    s.fill()
                                    s.toggled = True
                                    toggled_squares.append(s)
                                    b.filled += 1
                                    col = -1

                    elif mode == "cross" and s.get_shown_state() != -1 and not s.toggled:
                        if swipe_toggle is None or swipe_toggle == -1:
                            if col == -1 and row == -1:
                                swipe_toggle = -1
                                if s.shown_state == 1:
                                    b.filled -= 1
                                s.put_cross()
                                s.toggled = True
                                toggled_squares.append(s)
                                col = b.find_col(x)
                                row = b.find_row(y)
                            else:
                                if col == b.find_col(x):
                                    swipe_toggle = -1
                                    if s.shown_state == 1:
                                        b.filled -= 1
                                    s.put_cross()
                                    s.toggled = True
                                    toggled_squares.append(s)
                                    row = -1
                                elif row == b.find_row(y):
                                    swipe_toggle = -1
                                    if s.shown_state == 1:
                                        b.filled -= 1
                                    s.put_cross()
                                    s.toggled = True
                                    toggled_squares.append(s)
                                    col = -1

                    elif ((mode == "fill" and s.get_shown_state() == 1) or
                          (mode == "cross" and s.get_shown_state() == -1)) and (not s.toggled):
                        if swipe_toggle is None or swipe_toggle == 0:
                            if col == -1 and row == -1:
                                swipe_toggle = 0
                                s.reset()
                                s.toggled = True
                                toggled_squares.append(s)
                                if mode == "fill":
                                    b.filled -= 1
                                col = b.find_col(x)
                                row = b.find_row(y)
                            else:
                                if b.find_row(y) == row:
                                    swipe_toggle = 0
                                    s.reset()
                                    s.toggled = True
                                    toggled_squares.append(s)
                                    col = -1
                                    if mode == "fill":
                                        b.filled -= 1
                                elif b.find_col(x) == col:
                                    swipe_toggle = 0
                                    s.reset()
                                    s.toggled = True
                                    toggled_squares.append(s)
                                    row = -1
                                    if mode == "fill":
                                        b.filled -= 1
                except Exception:
                    pass

        clock.tick(60)
        pg.display.update()


if __name__ == "__main__":
    main()
