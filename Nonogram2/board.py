from square import Square
import pygame as pg


class Board:
    def __init__(self, x, y, cols, rows, side, disp, col, col_2):
        self.x = x
        self.y = y
        self.cols = cols
        self.rows = rows
        # Grid consists of lists which consists of squares
        self.grid = []
        self.square_side = side
        self.disp = disp
        self.col = col
        self.col_2 = col_2
        self.filled = 0

    def draw_squares(self):
        for row in self.grid:
            for s in row:
                s.draw()

    # Draw outline for board
    def draw_board(self):
        for i in range(self.rows + 1):
            if i % 5 == 0:
                pg.draw.line(self.disp, self.col_2, (self.x, self.y + i * self.square_side),
                             (self.x + self.square_side * self.cols, self.y + i * self.square_side))
            else:
                pg.draw.line(self.disp, self.col, (self.x, self.y + i * self.square_side),
                         (self.x + self.square_side * self.cols, self.y + i * self.square_side))

        for i in range(self.cols + 1):
            if i % 5 == 0:
                pg.draw.line(self.disp, self.col_2, (self.x + i * self.square_side, self.y),
                             (self.x + i * self.square_side, self.y + self.square_side * self.rows))
            else:
                pg.draw.line(self.disp, self.col, (self.x + i * self.square_side, self.y),
                             (self.x + i * self.square_side, self.y + self.square_side * self.rows))

    # Check every row and col if they are correct and filled
    def check_win(self):
        for i in range(self.rows):
            if not self.check_row(i):
                return False
        return True

    # Generate board with square objects
    def generate_board(self):
        Square.set_side(self.square_side)
        Square.set_color(self.col)
        Square.set_display(self.disp)

        for r in range(self.rows):
            temp = []
            for c in range(self.cols):
                temp.append(Square(self.x + c * Square.side, self.y + r * Square.side))
            self.grid.append(temp)

    # Count amount of active squares in row num
    def count_row(self, num):
        count = 0
        for s in self.grid[num]:
            if s.get_true_state() == 1:
                count += 1
        return count

    # Count amount of active squares in col num
    def count_col(self, num):
        count = 0
        for i in range(self.rows):
            if self.grid[i][num].get_true_state() == 1:
                count += 1
        return count

    # Return number outside of grid for col c
    def get_col_nums(self, num):
        counting = False
        count = 0
        nums = []
        for i in range(self.rows):
            if counting:
                if self.grid[i][num].get_true_state() == 1:
                    count += 1
                elif self.grid[i][num].get_true_state() == 0:
                    nums.append(count)
                    count = 0
                    counting = False
            else:
                if self.grid[i][num].get_true_state() == 0 and count != 0:
                    nums.append(count)
                    count = 0
                    counting = False
                elif self.grid[i][num].get_true_state() == 1:
                    counting = True
                    count += 1
        if counting:
            nums.append(count)

        return nums

    # Return number outside of grid for row r
    def get_row_nums(self, num):
        counting = False
        count = 0
        nums = []
        for s in self.grid[num]:
            if counting:
                if s.get_true_state() == 1:
                    count += 1
                elif s.get_true_state() == 0:
                    nums.append(count)
                    count = 0
                    counting = False
            else:
                if s.get_true_state() == 0 and count != 0:
                    nums.append(count)
                    count = 0
                    counting = False
                elif s.get_true_state() == 1:
                    counting = True
                    count += 1
        if counting:
            nums.append(count)

        return nums

    # Return row num
    def get_row(self, num):
        return self.grid[num]

    # Return col num
    def get_col(self, num):
        col = []
        for i in range(self.rows):
            col.append(self.grid[i][num])
        return col

    # Check if row is filled and correct
    def check_row(self, num):
        for s in self.grid[num]:
            # If a blue square isnt marked as blue or an empty square is marked as blue
            if (s.get_true_state() != s.get_shown_state() and s.get_true_state() == 1) \
                    or (s.get_true_state() == 0 and s.get_shown_state() == 1):
                return False
        return True

    # Check if col is filled and correct
    def check_col(self, num):
        for s in self.get_col(num):
            # If a blue square isnt marked as blue or an empty square is marked as blue
            if (s.get_true_state() != s.get_shown_state() and s.get_true_state() == 1) \
                    or (s.get_true_state() == 0 and s.get_shown_state() != 1):
                return False
        return True

    # Return square at row r and col c
    def get_square(self, c, r):
        return self.grid[r][c]

    def find_square(self, x, y):
        col = (x - self.x) // self.square_side
        row = (y - self.y) // self.square_side
        return self.grid[int(row)][int(col)]

    def find_row(self, y):
        return int((y - self.y) // self.square_side)

    def find_col(self, x):
        return int((x - self.x) // self.square_side)

    def find_x(self, col):
        return col * self.square_side + self.square_side / 2

    def find_y(self, row):
        return row * self.square_side + self.square_side / 2

    def in_box(self, x, y):
        return x >= self.x and x <= self.x + self.square_side * self.cols and y >= self.y and y <= self.y + self.square_side * self.rows

    def row_side_nums(self, num):
        nums = self.get_row_nums(num)
        nums_str = ""
        for i in nums:
            nums_str += str(i) + " "
        nums_str = nums_str[:-1]
        return nums_str

    def col_side_nums(self, num):
        nums = self.get_col_nums(num)
        nums_str = ""
        for i in nums:
            nums_str += str(i) + " "
        nums_str = nums_str[:-1]
        return nums_str

    def show_solution(self):
        for r in self.grid:
            for s in r:
                if (s.get_true_state() == 1 and s.get_shown_state() != 1):
                    s.set_shown_state(1)
                    self.filled += 1
                elif s.get_true_state() == 0 and s.get_shown_state() == 1:
                    s.set_shown_state(0)
                    self.filled -= 1

    def clear(self):
        for r in self.grid:
            for s in r:
                if s.get_shown_state() == 1:
                    s.set_shown_state(0)
                    self.filled -= 1
